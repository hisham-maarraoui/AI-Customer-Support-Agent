# 🚀 Vercel-Only Deployment Guide

Deploy your entire AI Apple Support Agent (frontend + backend) to Vercel in one place!

## ✅ What's Included

- **Frontend**: React app with dark mode
- **Backend**: Serverless API functions
- **AI Agent**: Google Gemini integration
- **Vector Store**: Pinecone integration
- **All in one deployment!**

---

## 📋 Prerequisites

1. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository** - Your code is already on GitHub
3. **API Keys Ready**:
   - Google Gemini API key
   - Pinecone API key

---

## 🎯 Step-by-Step Deployment

### Step 1: Connect to Vercel

1. **Go to [Vercel.com](https://vercel.com)**
2. **Sign up/Login** with GitHub
3. **Click "New Project"**
4. **Import your repository**: `hisham-maarraoui/AI-Customer-Support-Agent`

### Step 2: Configure Project

1. **Framework Preset**: Select "Other"
2. **Root Directory**: Leave as `/` (root)
3. **Build Command**: `cd frontend && npm install && npm run build`
4. **Output Directory**: `frontend/build`
5. **Install Command**: Leave empty (handled in build)

### Step 3: Add Environment Variables

Click "Environment Variables" and add:

```
GOOGLE_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=apple-support
GEMINI_MODEL=gemini-2.0-flash
EMBEDDING_MODEL=models/embedding-001
VECTOR_DIMENSION=768
VECTOR_METRIC=cosine
```

### Step 4: Deploy

1. **Click "Deploy"**
2. **Wait for build to complete** (2-3 minutes)
3. **Your app will be live!** 🎉

---

## 🔧 How It Works

### Frontend

- **Location**: `frontend/` directory
- **Build**: React app builds to `frontend/build/`
- **Served**: Static files served by Vercel

### Backend (API Functions)

- **Location**: `api/` directory
- **Routes**:
  - `GET /api/health` - Health check
  - `POST /api/chat` - Chat with AI
- **Runtime**: Python 3.9 serverless functions

### File Structure

```
/
├── frontend/          # React app
├── backend/           # Backend code (imported by API functions)
├── api/              # Vercel API functions
│   ├── chat.py       # Chat endpoint
│   ├── health.py     # Health check
│   └── requirements.txt
├── data/             # Apple support data
└── vercel.json       # Vercel configuration
```

---

## 🧪 Testing Your Deployment

### 1. Health Check

Visit: `https://your-app.vercel.app/api/health`

Should return:

```json
{
  "status": "healthy",
  "message": "AI Apple Support Agent API is running",
  "version": "1.0.0"
}
```

### 2. Chat API

Test with curl:

```bash
curl -X POST https://your-app.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I reset my iPhone?"}'
```

### 3. Frontend

Visit: `https://your-app.vercel.app`

---

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Fails**

   - Check if all dependencies are in `frontend/package.json`
   - Verify Node.js version compatibility

2. **API Functions Fail**

   - Check environment variables are set correctly
   - Verify API keys are valid

3. **CORS Errors**

   - CORS is already configured in API functions
   - Frontend uses relative URLs (`/api/chat`)

4. **Vector Store Empty**
   - You'll need to populate Pinecone after deployment
   - Run indexing script locally or create a setup API endpoint

### Debug Commands:

```bash
# Check Vercel logs
vercel logs

# Test API locally
curl http://localhost:3000/api/health

# Check environment variables
vercel env ls
```

---

## 🔄 Updates and Redeployment

### Automatic Deployments

- **Every push to main branch** triggers automatic deployment
- **Preview deployments** for pull requests

### Manual Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

---

## 📊 Monitoring

### Vercel Dashboard

- **Analytics**: Page views, performance
- **Functions**: API route monitoring
- **Logs**: Real-time function logs
- **Deployments**: Automatic rollbacks

### Performance

- **Frontend**: CDN distributed globally
- **API**: Serverless functions scale automatically
- **Cold starts**: ~1-2 seconds for first request

---

## 🔒 Security

✅ **Environment Variables**: Securely stored in Vercel  
✅ **HTTPS**: Automatic SSL certificates  
✅ **CORS**: Configured for your domain  
✅ **API Keys**: Never exposed in client code

---

## 🎉 Success!

Your AI Apple Support Agent is now live at:
**`https://your-app.vercel.app`**

### Features Available:

- ✅ Chat with AI about Apple support
- ✅ Dark mode toggle
- ✅ Responsive design
- ✅ Real-time responses
- ✅ Knowledge base integration

### Next Steps:

1. **Test the chat functionality**
2. **Customize the UI** if needed
3. **Add more Apple support data** to improve responses
4. **Share your app** with users!

---

## 💡 Pro Tips

1. **Custom Domain**: Add your own domain in Vercel settings
2. **Analytics**: Enable Vercel Analytics for insights
3. **Edge Functions**: Consider using Edge Functions for faster responses
4. **Caching**: Add caching headers for better performance

**Happy deploying! 🚀**
