import os
from app.main import app  # Import the existing FastAPI app

# For Hugging Face Spaces, we can directly expose the FastAPI app instance
# Hugging Face will automatically handle the server setup

# The app instance from app.main is what gets served
# Make sure to use the PORT environment variable that Hugging Face provides
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=port,
        reload=False  # Disable reload in production
    )