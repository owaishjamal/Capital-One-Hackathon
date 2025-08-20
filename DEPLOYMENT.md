# Deployment Guide for Render

## ⚠️ IMPORTANT: Database Configuration Fix

**Your current setup is using SQLite, but for production on Render, you MUST use PostgreSQL.**

### Quick Fix Steps:

1. **Verify your settings.py has the correct database configuration** (already done)
2. **Ensure these environment variables are set in Render:**
   ```
   DATABASE_URL=postgresql://username:password@host:port/database
   ```
3. **The build script will automatically detect and confirm PostgreSQL usage**

### Pre-Deployment Checklist:
- ✅ PostgreSQL database created in Render
- ✅ DATABASE_URL environment variable set
- ✅ All required packages in requirements.txt
- ✅ Build script updated to verify database connection

## Step-by-Step Deployment

### 1. Prepare your repository
1. Push your code to GitHub
2. Make sure all the configuration files are included:
   - `requirements.txt`
   - `build.sh`
   - `Procfile`
   - `gunicorn.conf.py`
   - `.gitignore`

### 2. Create a Render Web Service
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: kisan-ai (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn bitnbuild.wsgi:application`

### 3. Set Environment Variables
In the Render dashboard, add these environment variables:

#### Required Variables:
- `SECRET_KEY`: Generate a new Django secret key
- `DEBUG`: `False`
- `DATABASE_URL`: (Will be auto-populated if using Render PostgreSQL)
- `GOOGLE_API_KEY`: Your Google AI API key
- `PYTHON_VERSION`: `3.11.0`

#### Optional Variables (if using features):
- `GOOGLE_OAUTH2_KEY`: Your Google OAuth2 client ID
- `GOOGLE_OAUTH2_SECRET`: Your Google OAuth2 client secret
- `TWILIO_ACCOUNT_SID`: Your Twilio account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio auth token
- `ADMIN_PASSWORD`: Password for the auto-created admin user

### 4. Create a PostgreSQL Database (REQUIRED for Production)
1. In Render dashboard, click "New +" → "PostgreSQL"
2. Configure the database:
   - **Name**: `kisan-ai-database`
   - **Database**: `kisan_ai`
   - **User**: `kisan_ai_user`
   - **Region**: Same as your web service
   - **Plan**: Free (or upgrade as needed)
3. Once created, copy the "External Database URL"
4. **IMPORTANT**: This URL will be automatically set as `DATABASE_URL` environment variable

### 5. Deploy Web Service
1. In Render dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `kisan-ai`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn bitnbuild.wsgi:application`
   - **Plan**: Free (minimum recommended for ML apps)
   
**IMPORTANT**: Make sure to connect the PostgreSQL database to your web service:
- In the web service settings, go to "Environment"
- Render should automatically add `DATABASE_URL` when you connect the database
- If not, manually add it using the External Database URL from step 4

### 6. Post-Deployment Steps
1. Your app will be available at: `https://your-app-name.onrender.com`
2. Access the admin panel at: `https://your-app-name.onrender.com/admin`
3. Default admin credentials: `admin` / `admin123` (change immediately!)

## Important Notes

### File Storage
- Render's filesystem is ephemeral
- Uploaded media files will be lost on restart
- Consider using cloud storage (AWS S3, Cloudinary) for production

### Model Files
- Large model files (yolov8n.pt) should be downloaded during build
- Consider hosting them on cloud storage and downloading in build script

### Environment Variables Security
- Never commit sensitive keys to Git
- Use Render's environment variables for all secrets
- Regenerate all keys for production use

### Performance Considerations
- Free tier has limitations (will sleep after 15 minutes of inactivity)
- Consider upgrading to paid plan for production use
- Monitor memory usage as ML models can be memory-intensive

## Troubleshooting

### Common Issues:
1. **Build fails**: Check build logs, ensure all dependencies are in requirements.txt
2. **Static files not loading**: Verify STATIC_ROOT and whitenoise configuration
3. **Database errors**: Ensure migrations are run in build script
4. **Memory errors**: ML models might exceed free tier memory limits

### Debugging:
- Check build logs in Render dashboard
- Use `DEBUG=True` temporarily to see detailed error messages
- Monitor application logs in Render dashboard
