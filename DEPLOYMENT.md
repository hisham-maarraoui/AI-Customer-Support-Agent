# AI Apple Support Agent - Deployment Guide

This guide will help you deploy your AI Apple Support Agent to production.

## 🚀 Quick Deploy Options

### Option 1: Vercel + Railway (Recommended)
- **Frontend**: Vercel (free, automatic deployments)
- **Backend**: Railway (free tier, supports Python/FastAPI)

### Option 2: Netlify + Render
- **Frontend**: Netlify (free tier)
- **Backend**: Render (free tier)

### Option 3: Full Stack on Railway
- **Both frontend and backend** on Railway

---

## 📋 Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **API Keys Ready**:
   - Google Gemini API key
   - Pinecone API key
   - Vapi API key (optional)

---

## 🎯 Option 1: Vercel + Railway (Recommended)

### Step 1: Deploy Backend to Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up/Login** with GitHub
3. **Create New Project** → "Deploy from GitHub repo"
4. **Select your repository**
5. **Set the source directory** to `backend/`
6. **Add Environment Variables**:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_env
   PINECONE_INDEX_NAME=apple-support
   VAPI_API_KEY=your_vapi_key
   VAPI_PUBLIC_KEY=your_vapi_public_key
   GEMINI_MODEL=gemini-2.0-flash
   EMBEDDING_MODEL=models/embedding-001
   VECTOR_DIMENSION=768
   VECTOR_METRIC=cosine
   ```
7. **Deploy** - Railway will automatically install dependencies and start the server
8. **Copy the deployment URL** (e.g., `https://your-app.railway.app`)

### Step 2: Deploy Frontend to Vercel

1. **Go to [Vercel.com](https://vercel.com)**
2. **Sign up/Login** with GitHub
3. **Import Project** → Select your repository
4. **Configure Project**:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend/`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. **Add Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-app.railway.app
   REACT_APP_VAPI_PUBLIC_KEY=your_vapi_public_key
   ```
6. **Deploy** - Vercel will build and deploy your app

### Step 3: Update Backend CORS

After getting your Vercel URL, update the backend CORS settings:

```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",  # Add your Vercel URL
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🎯 Option 2: Netlify + Render

### Deploy Backend to Render

1. **Go to [Render.com](https://render.com)**
2. **Sign up/Login** with GitHub
3. **New Web Service** → Connect your repository
4. **Configure**:
   - **Name**: `apple-support-backend`
   - **Root Directory**: `backend/`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variables** (same as Railway)
6. **Deploy**

### Deploy Frontend to Netlify

1. **Go to [Netlify.com](https://netlify.com)**
2. **Sign up/Login** with GitHub
3. **New site from Git** → Select your repository
4. **Configure**:
   - **Base directory**: `frontend/`
   - **Build command**: `npm run build`
   - **Publish directory**: `build/`
5. **Add Environment Variables** (same as Vercel)
6. **Deploy**

---

## 🎯 Option 3: Full Stack on Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Create New Project** → "Deploy from GitHub repo"
3. **Add two services**:
   - **Backend Service**: Source directory `backend/`
   - **Frontend Service**: Source directory `frontend/`
4. **Configure environment variables** for both services
5. **Deploy both services**

---

## 🔧 Post-Deployment Setup

### 1. Index Your Data

After backend deployment, you need to populate the vector store:

```bash
# SSH into your Railway/Render instance or use their console
cd backend
python index_data.py
```

### 2. Test Your Deployment

1. **Test the backend**: Visit `https://your-backend-url/health`
2. **Test the frontend**: Visit your Vercel/Netlify URL
3. **Test the chat**: Send a message and verify it works

### 3. Set Up Custom Domain (Optional)

- **Vercel**: Add custom domain in project settings
- **Railway**: Use Railway's custom domain feature

---

## 🛠️ Troubleshooting

### Common Issues:

1. **CORS Errors**: Make sure your backend CORS includes your frontend URL
2. **API Key Issues**: Verify all environment variables are set correctly
3. **Build Failures**: Check the build logs for missing dependencies
4. **Vector Store Empty**: Run the indexing script after deployment

### Debug Commands:

```bash
# Check backend logs
railway logs

# Check frontend build
vercel logs

# Test API locally
curl https://your-backend-url/health
```

---

## 📊 Monitoring

### Railway Monitoring:
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory usage
- **Deployments**: Automatic rollbacks

### Vercel Monitoring:
- **Analytics**: Page views, performance
- **Functions**: API route monitoring
- **Deployments**: Preview deployments

---

## 🔒 Security Considerations

1. **Environment Variables**: Never commit API keys to Git
2. **CORS**: Only allow your frontend domain
3. **Rate Limiting**: Consider adding rate limiting to your API
4. **HTTPS**: All production deployments use HTTPS by default

---

## 🎉 Success!

Once deployed, your AI Apple Support Agent will be available at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-app.railway.app`

Share your app with users and start helping them with Apple support questions! 🚀 