# AWS Deployment Setup Guide

## Changes Made for AWS Hosting

This document outlines the changes made to prepare the Marketing Tracker project for AWS hosting.

### 1. Image Field Migration (FilePathField → ImageField)

**Problem:** FilePathField was hardcoded to a local Windows path, which is not portable or suitable for cloud hosting.

**Solution:** Converted to ImageField with proper upload handling.

**Files Modified:**
- `posts/models.py` - Changed `image` field from FilePathField to ImageField
- `posts/forms.py` - Updated widget from TextInput to FileInput with image acceptance
- `posts/views.py` - Added `request.FILES` to form handling
- `layout/templates/posts/create_ad.html` - Added `enctype="multipart/form-data"` to form

**Migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Media Files Configuration

**Added to `marketing_tracker/settings.py`:**

```python
# Media files (User-uploaded content)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**Added to `marketing_tracker/urls.py`:**

```python
from django.conf import settings
from django.conf.urls.static import static

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3. Directory Structure

The following directories will be created automatically:
- `media/` - User-uploaded images (ads/)
- `staticfiles/` - Collected static files for production

### 4. AWS S3 Integration (Next Steps)

For production AWS hosting, you'll need to:

1. **Install boto3 and django-storages:**
   ```bash
   pip install boto3 django-storages
   ```

2. **Update settings.py for S3:**
   ```python
   if not DEBUG:
       # AWS S3 Configuration
       AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
       AWS_S3_REGION_NAME = 'us-east-1'
       AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
       
       STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
       MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
       
       STORAGES = {
           'default': {
               'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
           },
           'staticfiles': {
               'BACKEND': 'storages.backends.s3boto3.S3StaticStorage',
           },
       }
   ```

3. **Set AWS credentials as environment variables:**
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

### 5. Testing

All 33 tests pass with the new ImageField configuration:
```bash
python manage.py test
# Result: OK (33 tests)
```

### 6. Local Development

Images are stored in `media/ads/` directory locally. This directory should be:
- Added to `.gitignore` (don't commit user uploads)
- Created automatically when first image is uploaded

### 7. Production Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure AWS S3 bucket
- [ ] Set AWS credentials as environment variables
- [ ] Run `python manage.py collectstatic` for static files
- [ ] Update database to production (RDS)
- [ ] Set `SECRET_KEY` as environment variable
- [ ] Enable HTTPS/SSL
- [ ] Configure CloudFront CDN for static/media files


