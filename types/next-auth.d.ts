import "next-auth"
import "next-auth/jwt"

declare module "next-auth" {
  interface Session {
    user: {
      id: string
      name?: string | null
      email?: string | null
      image?: string | null
      role?: string
      isAdmin?: boolean
      provider?: string
      createdAt?: string
    }
  }

  interface User {
    id: string
    role?: string
    isAdmin?: boolean
    provider?: string
    createdAt?: string
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    role?: string
    isAdmin?: boolean
    provider?: string
    createdAt?: string
  }
}
