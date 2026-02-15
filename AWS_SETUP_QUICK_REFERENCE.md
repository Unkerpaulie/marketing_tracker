# AWS Setup - Quick Reference

## What Changed

### 1. **Ad Model Image Field**
```python
# BEFORE (FilePathField - hardcoded Windows path)
image = models.FilePathField(path="C:\\Users\\sablo\\...", blank=True, null=True)

# AFTER (ImageField - portable, cloud-ready)
image = models.ImageField(upload_to='ads/', blank=True, null=True)
```

### 2. **Settings Configuration**
Added to `marketing_tracker/settings.py`:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 3. **URL Configuration**
Added to `marketing_tracker/urls.py`:
```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 4. **Form Updates**
- Changed image widget from `TextInput` to `FileInput`
- Added `accept='image/*'` attribute
- Updated view to handle `request.FILES`

### 5. **Template Updates**
- Added `enctype="multipart/form-data"` to create_ad form

### 6. **.gitignore Updates**
Added:
```
/media/
/staticfiles/
```

## Files Modified
- ✅ `posts/models.py`
- ✅ `posts/forms.py`
- ✅ `posts/views.py`
- ✅ `marketing_tracker/settings.py`
- ✅ `marketing_tracker/urls.py`
- ✅ `layout/templates/posts/create_ad.html`
- ✅ `.gitignore`

## Migration Applied
```bash
python manage.py makemigrations  # Created 0005_alter_ad_image.py
python manage.py migrate         # Applied successfully
```

## Test Results
✅ All 33 tests passing

## Local Development
Images are stored in: `media/ads/`

## Next: AWS S3 Integration
See `AWS_DEPLOYMENT_SETUP.md` for S3 configuration steps.


