import type { NextAuthOptions } from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import CredentialsProvider from "next-auth/providers/credentials"
import bcrypt from "bcryptjs"
import connectDB from "./mongodb"
import User from "@/models/User"

const normalizedAdminEmails = () =>
  (process.env.ADMIN_EMAILS || "")
    .split(",")
    .map((value) => value.trim().toLowerCase())
    .filter(Boolean)

const credentialsProvider = CredentialsProvider({
  name: "credentials",
  credentials: {
    email: { label: "Email", type: "email" },
    password: { label: "Password", type: "password" },
    action: { label: "Action", type: "text" },
  },
  async authorize(credentials) {
    if (process.env.NODE_ENV !== "development") {
      throw new Error("Password sign-in is only available in development")
    }
    if (!credentials?.email || !credentials?.password) {
      throw new Error("Email and password required")
    }
    if (credentials.password.length < 8) {
      throw new Error("Password must be at least 8 characters")
    }

    const email = credentials.email.trim().toLowerCase()
    await connectDB()

    if (credentials.action === "signup") {
      if (await User.findOne({ email })) {
        throw new Error("User already exists with this email")
      }

      const user = await User.create({
        email,
        name: email.split("@")[0],
        password: await bcrypt.hash(credentials.password, 12),
        role: normalizedAdminEmails().includes(email) ? "admin" : "user",
        provider: "credentials",
        providerId: email,
        lastLogin: new Date(),
      })

      return {
        id: user._id.toString(),
        email: user.email,
        name: user.name,
        role: user.role,
        isAdmin: user.role === "admin",
        provider: user.provider,
        createdAt: user.createdAt.toISOString(),
      }
    }

    const user = await User.findOne({ email })
    if (!user?.password || !(await bcrypt.compare(credentials.password, user.password))) {
      throw new Error("Invalid email or password")
    }
    user.lastLogin = new Date()
    await user.save()

    return {
      id: user._id.toString(),
      email: user.email,
      name: user.name,
      role: user.role,
      isAdmin: user.role === "admin",
      provider: user.provider,
      createdAt: user.createdAt.toISOString(),
    }
  },
})

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    ...(process.env.NODE_ENV === "development" ? [credentialsProvider] : []),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.sub = user.id
        token.role = user.role
        token.isAdmin = user.isAdmin
        token.provider = user.provider
        token.createdAt = user.createdAt
      } else if (token.sub) {
        // Re-read authorization data so a role change takes effect immediately.
        await connectDB()
        const currentUser = await User.findById(token.sub).select("role provider createdAt")
        token.role = currentUser?.role
        token.isAdmin = currentUser?.role === "admin"
        token.provider = currentUser?.provider
        token.createdAt = currentUser?.createdAt?.toISOString()
      }
      return token
    },
    async session({ session, token }) {
      session.user.id = token.sub!
      session.user.role = token.role as string
      session.user.isAdmin = token.isAdmin as boolean
      session.user.provider = token.provider
      session.user.createdAt = token.createdAt
      return session
    },
    async signIn({ user, account }) {
      if (account?.provider !== "google") return true

      try {
        await connectDB()
        const email = user.email!.trim().toLowerCase()
        const existingUser = await User.findOne({ email })

        if (existingUser) {
          existingUser.name = user.name || existingUser.name
          existingUser.image = user.image || existingUser.image
          existingUser.lastLogin = new Date()
          await existingUser.save()
          user.id = existingUser._id.toString()
          user.role = existingUser.role
          user.isAdmin = existingUser.role === "admin"
          user.provider = existingUser.provider
          user.createdAt = existingUser.createdAt.toISOString()
        } else {
          const newUser = await User.create({
            email,
            name: user.name,
            image: user.image,
            role: normalizedAdminEmails().includes(email) ? "admin" : "user",
            provider: "google",
            providerId: account.providerAccountId,
            lastLogin: new Date(),
          })
          user.id = newUser._id.toString()
          user.role = newUser.role
          user.isAdmin = newUser.role === "admin"
          user.provider = newUser.provider
          user.createdAt = newUser.createdAt.toISOString()
        }
        return true
      } catch (error) {
        console.error("Google sign in error:", error)
        return false
      }
    },
  },
  pages: {
    signIn: "/auth/signin",
    error: "/auth/error",
  },
  session: {
    strategy: "jwt",
  },
  debug: process.env.NODE_ENV === "development",
}
