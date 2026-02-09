# Deploying TaskFlow AI Backend to Hugging Face Spaces

This guide explains how to deploy the TaskFlow AI backend to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (sign up at [huggingface.co](https://huggingface.co))
2. A PostgreSQL database (we recommend [Neon](https://neon.tech/) for serverless PostgreSQL)
3. A secret key for JWT authentication (at least 32 characters)

## Deployment Steps

### Option 1: Using the Hugging Face Website (Recommended)

1. **Fork or create a copy of this repository**
   - Either fork this repository to your GitHub account
   - Or download the backend folder and create a new repository

2. **Create a new Space on Hugging Face**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Fill in the details:
     - Name: Choose a unique name for your space
     - License: MIT (or your preferred license)
     - SDK: Docker
     - Hardware: CPU Basic (sufficient for this application)
     - Visibility: Public or Private as per your preference

3. **Configure the repository**
   - Use the repository URL from step 1
   - The repository should contain:
     - `Dockerfile` (already included)
     - `app.py` (already included)
     - `requirements.txt` (already included)
     - `app/` folder with the application code
     - All other necessary files

4. **Set environment variables in the Space settings**
   - In your Space settings, go to the "Files" tab
   - Click on "Environment variables" or "Secrets"
   - Add the following environment variables:
     ```
     DATABASE_URL=your_postgresql_connection_string
     BETTER_AUTH_SECRET=your_jwt_secret_key_at_least_32_chars
     OPENROUTER_API_KEY=your_openrouter_api_key (optional)
     ```
   
5. **Start the build**
   - The Space will automatically start building when you save
   - Monitor the logs to ensure everything builds correctly

### Option 2: Using the Hugging Face CLI

1. **Install the Hugging Face Hub CLI**
   ```bash
   pip install huggingface_hub
   ```

2. **Login to your Hugging Face account**
   ```bash
   huggingface-cli login
   ```

3. **Create a Space repository**
   ```bash
   huggingface-cli space create-repo your-space-name --organization your-org-name
   ```

4. **Upload your files**
   ```bash
   git clone https://huggingface.co/spaces/your-org-name/your-space-name
   cd your-space-name
   # Copy all backend files here
   git add .
   git commit -m "Initial commit with TaskFlow AI backend"
   git push
   ```

5. **Set secrets via CLI**
   ```bash
   huggingface-cli space set-secrets --repo-id your-org-name/your-space-name DATABASE_URL="your_db_url"
   huggingface-cli space set-secrets --repo-id your-org-name/your-space-name BETTER_AUTH_SECRET="your_secret"
   ```

## Configuration Details

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string in the format:
  `postgresql://username:password@hostname:port/database_name`
  
- `BETTER_AUTH_SECRET`: A secret key for JWT token signing (minimum 32 characters)
  Generate one with: `openssl rand -base64 32`
  
- `OPENROUTER_API_KEY`: (Optional) API key for OpenRouter to enable AI chatbot features
  
- `CORS_ORIGINS`: (Optional) Comma-separated list of allowed origins, defaults to `["http://localhost:3000"]`
  
- `DEBUG`: (Optional) Set to `true` for debugging, defaults to `false`

### Docker Configuration

The application is configured to:
- Run on port 7860 (Hugging Face default)
- Use the `PORT` environment variable if provided
- Start with uvicorn for ASGI serving

## Post-Deployment

Once deployed:

1. **Access your API**
   - Your API will be available at: `https://your-username-huggingface-space-name.hf.space`
   - API documentation: `https://your-username-huggingface-space-name.hf.space/docs`

2. **Connect your frontend**
   - Update your frontend's `NEXT_PUBLIC_API_URL` to point to your deployed space
   - Example: `NEXT_PUBLIC_API_URL=https://your-username-huggingface-space-name.hf.space`

3. **Monitor logs**
   - Check the "Logs" tab in your Space settings for any runtime errors
   - Look for any environment variable issues or database connection problems

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify your `DATABASE_URL` is correct
   - Ensure your database provider allows connections from Hugging Face IPs

2. **Environment Variable Issues**
   - Make sure all required environment variables are set as "Secrets" in your Space
   - Secrets are not visible in the code but are available at runtime

3. **Build Failures**
   - Check the build logs for dependency installation issues
   - Ensure all required files are present in the repository

### Health Check

You can verify your deployment is working by visiting:
`https://your-username-huggingface-space-name.hf.space/health`

Expected response:
```json
{
  "status": "healthy",
  "service": "todo-api"
}
```

## Updating Your Deployment

To update your Space after making changes:

1. Push your changes to the repository
2. The Space will automatically rebuild (unless auto-rebuild is disabled)
3. Monitor the logs to ensure the update was successful

## Scaling Considerations

- For increased traffic, consider upgrading to a GPU space or Premium hardware
- Monitor your database connection limits
- Consider connection pooling for high-concurrency scenarios