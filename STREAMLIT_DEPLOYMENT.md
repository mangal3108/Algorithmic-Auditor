# Algorithmic Auditor - Streamlit Deployment Guide

## Local Development

### 1. Install Dependencies

```bash
pip install -r requirements-streamlit.txt
```

### 2. Run Backend (in one terminal)

```bash
cd backend
python main.py
# or
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### 3. Run Streamlit App (in another terminal)

```bash
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501`

---

## Deploy to Streamlit Cloud

### 1. Prepare Your Repository

Make sure your GitHub repository contains:
- `streamlit_app.py` - Main Streamlit application
- `requirements-streamlit.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration (optional)
- `backend/` folder with your FastAPI backend

### 2. Deploy Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Streamlit deployment"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign in with GitHub (create account if needed)
   - Click "New app"
   - Select your repository, branch, and main file (`streamlit_app.py`)

3. **Configure Backend URL**
   - If deploying backend separately, update the `BACKEND_URL` in the Streamlit app
   - Or set up environment variables for production

### 3. Backend Deployment Options

#### Option A: Deploy Backend to Heroku (deprecated)
Use `render.com` or `railway.app` instead:

```bash
# Example for Railway.app
# Push to Railway and configure environment
```

#### Option B: Deploy Backend to Hugging Face Spaces
Create a Docker container with your FastAPI backend

#### Option C: Use a cloud function (AWS Lambda, Google Cloud Function)
Wrap your FastAPI endpoints as serverless functions

#### Option D: Self-hosted server
Use `PythonAnywhere`, `DigitalOcean`, `AWS EC2`, etc.

---

## Using Secrets for Backend URL

### In Streamlit Cloud:

1. Click on your app's menu (three dots)
2. Settings → Secrets
3. Add:
   ```toml
   backend_url = "https://your-backend-url.com"
   ```

4. Update your app to use secrets:
   ```python
   import streamlit as st
   BACKEND_URL = st.secrets.get("backend_url", "http://localhost:8000")
   ```

---

## Troubleshooting

**Error: "Cannot connect to backend"**
- Ensure backend is running and accessible
- Check CORS settings in `backend/main.py`
- Verify the backend URL in the Streamlit app

**Import errors**
- Make sure all packages in `requirements-streamlit.txt` are installed
- Run `pip install -r requirements-streamlit.txt`

**File upload issues**
- Check backend file upload endpoint
- Ensure file size limits are appropriate

---

## Performance Tips

- Cache data and models using `@st.cache_data`
- Use session state to avoid re-computing
- Optimize backend responses for faster visualizations
