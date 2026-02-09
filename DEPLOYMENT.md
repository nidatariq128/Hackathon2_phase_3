# 🚀 Deployment Guide

## Deploying to Vercel (Frontend)

### Quick Deploy

1. **Go to Vercel:**
   Visit: https://vercel.com

2. **Import Your Repository:**
   - Click "Add New Project"
   - Select "Import Git Repository"
   - Choose: `nidatariq128/hackathon2_phase_2`

3. **Configure Project:**
   - Framework Preset: **Next.js**
   - Root Directory: **frontend**
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

4. **Add Environment Variables:**
   Click "Environment Variables" and add:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```

   **Important:** You'll need to deploy your backend first to get this URL!

5. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete
   - Your app will be live at: `https://your-project-name.vercel.app`

---

## Backend Deployment Options

### Option 1: Railway (Recommended for FastAPI)

1. **Go to Railway:**
   Visit: https://railway.app

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose: `nidatariq128/hackathon2_phase_2`

3. **Configure Service:**
   - Root Directory: **backend**
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables:**
   ```
   DATABASE_URL=your-neon-database-url
   BETTER_AUTH_SECRET=your-secret-key
   JWT_ALGORITHM=HS256
   CORS_ORIGINS=["https://your-frontend-url.vercel.app"]
   DEBUG=false
   API_HOST=0.0.0.0
   API_PORT=8000
   ```

5. **Deploy:**
   - Railway will auto-deploy
   - Copy your backend URL (e.g., `https://your-app.railway.app`)
   - Update frontend env variable with this URL

---

### Option 2: Render (Alternative)

1. **Go to Render:**
   Visit: https://render.com

2. **Create Web Service:**
   - Click "New Web Service"
   - Connect GitHub: `nidatariq128/hackathon2_phase_2`

3. **Configure:**
   - Name: `hackathon2-todo-api`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables:**
   (Same as Railway above)

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment
   - Copy your URL

---

## Full Deployment Steps (Correct Order)

### Step 1: Deploy Backend First

1. Choose Railway or Render
2. Deploy backend with environment variables
3. Get backend URL: `https://your-backend.railway.app`
4. Test backend: Visit `https://your-backend.railway.app/health`

### Step 2: Deploy Frontend

1. Go to Vercel
2. Import repository
3. Set root directory to `frontend`
4. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   ```
5. Deploy
6. Get frontend URL: `https://your-app.vercel.app`

### Step 3: Update CORS

1. Go back to Railway/Render
2. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=["https://your-app.vercel.app"]
   ```
3. Redeploy backend

### Step 4: Test Your App

1. Visit your frontend URL
2. Sign in
3. Create a task
4. Verify it works!

---

## Environment Variables Checklist

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Backend
```bash
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
CORS_ORIGINS=["https://your-frontend-url.vercel.app"]
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000
```

---

## Troubleshooting

### Frontend Issues

**Problem:** API calls failing
- **Solution:** Check `NEXT_PUBLIC_API_URL` is correct
- **Solution:** Make sure backend is deployed and accessible

**Problem:** Build fails
- **Solution:** Run `npm install` locally first
- **Solution:** Check for TypeScript errors

### Backend Issues

**Problem:** 500 errors
- **Solution:** Check DATABASE_URL is correct
- **Solution:** Check all environment variables are set

**Problem:** CORS errors
- **Solution:** Update `CORS_ORIGINS` with your Vercel URL
- **Solution:** Make sure URL includes `https://`

**Problem:** Database connection fails
- **Solution:** Verify Neon database is active
- **Solution:** Check connection string format

---

## Custom Domain (Optional)

### Vercel
1. Go to Project Settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

### Railway
1. Go to Settings
2. Click "Networking"
3. Add custom domain
4. Update DNS records

---

## Monitoring

- **Vercel Analytics:** Built-in traffic monitoring
- **Railway Metrics:** View logs and resource usage
- **Sentry (Optional):** Add error tracking

---

## Need Help?

- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs

---

Built with ❤️ | Happy Deploying! 🚀
