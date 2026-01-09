# Frontend Development - Next.js 16 App

## Project Overview

This is the frontend component of the Todo App built with Next.js 16 using the App Router.

## Tech Stack

- Next.js 16 with App Router
- TypeScript
- Tailwind CSS
- Better Auth for authentication
- React Server Components and Client Components

## Project Structure

- /src/app - Next.js App Router pages and layouts (with /src directory)
- /src/components - Reusable UI components
- /src/lib - Utility functions and auth integration
- /public - Static assets
- /src/styles - Global styles and Tailwind configuration

## Development Workflow

1. Install dependencies: `npm install`
2. Run development server: `npm run dev`
3. Add new pages to the `/app` directory
4. Create reusable components in `/components`

## Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production build
- `npm run lint` - Run ESLint to check for code issues

## Integration Points

- Connects to backend API at `/api` routes
- Uses Better Auth for authentication
- Follows branding guidelines from @specs/branding.md
- Uses TypeScript path aliases with "@/*" pointing to src/ directory
- Integrates Tailwind CSS for styling via globals.css