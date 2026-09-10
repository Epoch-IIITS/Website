# Club Website Backend

A comprehensive backend for a club website built with Next.js App Router, MongoDB, and NextAuth.

## Features

- **Authentication**: Google OAuth with NextAuth
- **Blog System**: Create, read, update, delete blog posts with Markdown support
- **Project Showcase**: Manage and display club projects
- **Event Management**: Create events with RSVP functionality and ticket generation
- **Gallery**: Upload and organize event photos
- **Admin Panel**: Role-based access control for content management
- **Admin Workspace**: Responsive sidebar navigation and a contact queries inbox
- **Contact Form**: Saves messages to MongoDB for admin review

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Database**: MongoDB with Mongoose ODM
- **Authentication**: NextAuth with Google Provider
- **Validation**: Zod for schema validation
- **File Upload**: Cloudinary integration ready
- **PDF Generation**: PDFKit for ticket generation
- **QR Codes**: QRCode library for ticket verification

## Getting Started

### Prerequisites

- Node.js 18+ 
- MongoDB database
- Google OAuth credentials
- Cloudinary account (optional)

### Installation

1. Clone the repository
2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

3. Set up environment variables in \`.env.local\`:
   \`\`\`env
   MONGODB_URI=your_mongodb_connection_string
   NEXTAUTH_URL=http://localhost:3000
   NEXTAUTH_SECRET=your_nextauth_secret
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   ADMIN_EMAILS=admin@example.com,admin2@example.com
   \`\`\`

4. Run the development server:
   \`\`\`bash
   npm run dev
   \`\`\`

## API Endpoints

### Public Endpoints
- \`GET /api/blogs\` - Get published blogs
- \`GET /api/blogs/[id]\` - Get specific blog
- \`GET /api/projects\` - Get all projects
- \`GET /api/events\` - Get all events
- \`GET /api/gallery\` - Get gallery items

### Protected Endpoints (Require Authentication)
- `POST /api/contact` - Submit a contact message (name, subject, message; email from the signed-in account)
- \`POST /api/rsvp\` - Create RSVP for event
- \`GET /api/rsvp\` - Get user's RSVPs
- \`GET /api/rsvp/[id]/ticket\` - Download ticket PDF

### Admin Endpoints (Require Admin Role)
- `GET /api/admin/queries?page=1` - Read contact submissions, newest first, 20 per page
- `DELETE /api/admin/queries/[id]` - Permanently delete a contact query (admin only)
- \`POST /api/blogs\` - Create blog post
- \`PUT /api/blogs/[id]\` - Update blog post
- \`DELETE /api/blogs/[id]\` - Delete blog post
- \`POST /api/projects\` - Create project
- \`POST /api/events\` - Create event
- \`POST /api/gallery\` - Create gallery
- \`GET /api/admin/stats\` - Get admin dashboard stats
- \`GET /api/admin/events/[id]/rsvps\` - Get event RSVPs

## Database Models

### User
- Email, name, image, role (admin/user)
- Google OAuth integration

### Blog
- Title, slug, content (Markdown), excerpt
- Author reference, published status, tags

### Project
- Title, description, tech stack
- GitHub/live URLs, featured status

### Event
- Title, description, date, venue
- RSVP functionality, max attendees

### RSVP
- Event and user references
- Status (attending/not_attending/maybe)
- Unique ticket ID

### Gallery
- Event name, date, images with captions
- Admin-managed photo collections

## Authentication & Authorization

- Google OAuth via NextAuth
- Role-based access (admin/user)
- Admin emails configured via environment variables
- Protected routes with middleware
- Session-based authentication

## Features

### Blog System
- Markdown content support
- SEO-friendly slugs
- Draft/published states
- Tag system

### Event Management
- RSVP system with status tracking
- PDF ticket generation with QR codes
- RSVP deadline enforcement
- Admin RSVP management

### File Upload Ready
- Cloudinary integration prepared
- Image validation and processing
- Gallery photo management

### Admin Dashboard
- Comprehensive statistics
- Content management interface
- User RSVP tracking
- Role-based permissions

## Security

- Environment variable protection
- Input validation with Zod
- Role-based route protection
- Session-based authentication
- CORS and security headers

## Deployment

Ready for deployment on Vercel, Netlify, or any Node.js hosting platform. Ensure all environment variables are configured in your deployment environment.
