# Deploying TaskFlow Frontend to Vercel

This guide explains how to deploy the TaskFlow frontend to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. A deployed backend (your Hugging Face Space at https://nidatariq-hachathon2_phase3.hf.space)
3. A PostgreSQL database for Better Auth (we recommend [Neon](https://neon.tech/))

## Deployment Steps

### Option 1: Using the Vercel Dashboard (Recommended)

1. **Push your code to GitHub**
   - Make sure your frontend code is in a GitHub repository
   - The repository should contain:
     - `package.json` and `package-lock.json`
     - `next.config.ts`
     - `vercel.json` (included in this project)
     - All source code in the correct structure
     - `.env.example` file with environment variable templates

2. **Import your project to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your frontend repository
   - Vercel will automatically detect it's a Next.js project

3. **Configure the build settings**
   - Framework preset: Next.js
   - Build command: `npm run build` (should be auto-detected)
   - Output directory: `.next` (should be auto-detected)
   - Root directory: `/` (should be auto-detected)

4. **Set environment variables**
   - Click on "Environment Variables" in your project settings
   - Add the following variables:
   
   | Key | Value |
   |-----|-------|
   | `NEXT_PUBLIC_API_URL` | `https://nidatariq-hachathon2_phase3.hf.space` |
   | `BETTER_AUTH_URL` | `https://your-project-name.vercel.app` (replace with your actual Vercel domain) |
   | `BETTER_AUTH_SECRET` | `a-very-long-secret-string-at-least-32-chars-long` |
   | `DATABASE_URL` | `your-postgresql-database-url` |
   
5. **Deploy**
   - Click "Deploy" to start the deployment process
   - Monitor the build logs to ensure everything builds correctly

### Option 2: Using the Vercel CLI

1. **Install the Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to your Vercel account**
   ```bash
   vercel login
   ```

3. **Navigate to your project directory and deploy**
   ```bash
   cd your-frontend-directory
   vercel --prod
   ```

4. **Set environment variables via CLI**
   ```bash
   vercel env add NEXT_PUBLIC_API_URL
   # Enter: https://nidatariq-hachathon2_phase3.hf.space
   
   vercel env add BETTER_AUTH_URL
   # Enter: https://your-project-name.vercel.app
   
   vercel env add BETTER_AUTH_SECRET
   # Enter: your-secret-string
   
   vercel env add DATABASE_URL
   # Enter: your-postgres-database-url
   ```

## Environment Variables Explained

- `NEXT_PUBLIC_API_URL`: Points to your deployed backend API (Hugging Face Space)
- `BETTER_AUTH_URL`: The URL of your deployed frontend (Vercel domain)
- `BETTER_AUTH_SECRET`: Secret key for JWT signing (minimum 32 characters)
- `DATABASE_URL`: PostgreSQL database URL for Better Auth session management

## Configuration Details

### Vercel Configuration (vercel.json)

The project includes a `vercel.json` file with optimal settings for Next.js 16:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next",
      "config": {
        "withTurbo": true
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/"
    }
  ],
  "env": {
    "NODE_ENV": "production"
  }
}
```

### Next.js Configuration

The project uses Next.js 16 with App Router, which is fully supported by Vercel.

## Post-Deployment

Once deployed:

1. **Access your application**
   - Your app will be available at: `https://your-project-name.vercel.app`
   - Or the custom domain you've configured

2. **Verify API connectivity**
   - Log in to your application
   - Check that tasks can be loaded, created, updated, and deleted
   - Verify that API calls are being made to your Hugging Face backend

3. **Monitor logs**
   - Check the "Logs" tab in your Vercel dashboard for any runtime errors
   - Look for any environment variable issues or API connection problems

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify `NEXT_PUBLIC_API_URL` points to your working Hugging Face backend
   - Check that your backend is accessible at that URL

2. **Authentication Issues**
   - Ensure `BETTER_AUTH_SECRET` matches between frontend and backend
   - Verify `BETTER_AUTH_URL` matches your Vercel domain

3. **Database Connection Issues**
   - Make sure your `DATABASE_URL` is correct and accessible
   - Verify your PostgreSQL provider allows connections from Vercel

4. **Build Failures**
   - Check the build logs in your Vercel dashboard
   - Ensure all dependencies are properly specified in package.json

### Health Check

After deployment, verify your frontend is working by:
1. Visiting your Vercel URL
2. Checking that the login/signup pages load correctly
3. Verifying that API calls to your backend are functioning

## Updating Your Deployment

To update your deployment after making changes:

1. Push your changes to the GitHub repository
2. Vercel will automatically deploy the new version
3. Monitor the deployment logs to ensure success

## Domain Configuration

Optionally, you can configure a custom domain:
1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain and follow DNS configuration instructions

## Scaling Considerations

- Vercel automatically scales your application based on traffic
- Your backend on Hugging Face should also scale appropriately
- Monitor your database connection limits if you expect high traffic