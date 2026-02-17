# Environment Setup - Quick Start

## Overview

The Django Marketing Tracker application supports two environments:
- **DEV**: Local development with SQLite and local file storage
- **AWS**: Production deployment with PostgreSQL (RDS) and S3 storage

The environment is controlled by the `ENVIRONMENT` variable.

---

## Quick Start

### Local Development (DEV)

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   ENVIRONMENT=DEV
   DEBUG=True
   SECRET_KEY=your-dev-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. **Run the application:**
   ```bash
   python manage.py migrate
   python manage.py runserver 8008
   ```

That's it! No AWS configuration needed for local development.

---

### AWS Deployment

#### Option 1: EC2 with Separate Services (Recommended)

1. **Set environment variables:**
   ```bash
   ENVIRONMENT=AWS
   DEBUG=False
   SECRET_KEY=your-production-key
   DATABASE_URL=postgresql://user:pass@rds-host:5432/dbname
   AWS_STORAGE_BUCKET_NAME=your-bucket-name
   AWS_S3_REGION_NAME=us-east-1
   ```

2. **Deploy:**
   - See `setup_docs/EC2_DEPLOYMENT_GUIDE.md` for detailed instructions

#### Option 2: Elastic Beanstalk

1. **Configure EB environment variables** in the console:
   - `ENVIRONMENT=AWS`
   - `DEBUG=False`
   - `SECRET_KEY=your-key`
   - `DATABASE_URL=postgresql://...`
   - `AWS_STORAGE_BUCKET_NAME=your-bucket`

2. **Deploy:**
   ```bash
   eb init
   eb create
   eb deploy
   ```

The `.ebextensions/` configuration files are preserved and ready to use.

---

## Environment Comparison

| Feature | DEV | AWS |
|---------|-----|-----|
| **Database** | SQLite | PostgreSQL (RDS) |
| **Static Files** | Local (`staticfiles/`) | S3 (`static/`) |
| **Media Files** | Local (`media/`) | S3 (`media/`) |
| **AWS Credentials** | Not needed | Optional (use IAM roles) |
| **DATABASE_URL** | Not needed | Required |
| **AWS_STORAGE_BUCKET_NAME** | Not needed | Required |

---

## Key Files

- **`.env.example`**: Template for environment variables
- **`marketing_tracker/settings.py`**: Environment-aware Django settings
- **`.ebextensions/`**: Elastic Beanstalk configuration (preserved)
- **`setup_docs/ENVIRONMENT_CONFIGURATION.md`**: Detailed configuration guide
- **`setup_docs/EC2_DEPLOYMENT_GUIDE.md`**: EC2 deployment instructions

---

## Environment Variables Reference

### Required for DEV
```bash
ENVIRONMENT=DEV
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Required for AWS
```bash
ENVIRONMENT=AWS
DEBUG=False
SECRET_KEY=your-production-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### Optional for AWS (if not using IAM roles)
```bash
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

---

## What Changed?

### Before (DEBUG-based configuration)
```python
if not DEBUG:
    # Use S3
```

### After (ENVIRONMENT-based configuration)
```python
if ENVIRONMENT == 'AWS':
    # Use S3
elif ENVIRONMENT == 'DEV':
    # Use local storage
```

### Benefits
- ✅ **Explicit**: Clear separation between environments
- ✅ **Flexible**: Can debug in AWS if needed
- ✅ **Safe**: No accidental production mode
- ✅ **IAM Role Support**: AWS credentials optional on EC2
- ✅ **EB Compatible**: Elastic Beanstalk configuration preserved

---

## Deployment Options

### 1. Elastic Beanstalk (Fully Managed)
- **Pros**: Easy deployment, auto-scaling, load balancing
- **Cons**: Less control, potentially higher cost
- **Guide**: Use `.ebextensions/` files + EB console for env vars

### 2. EC2 with Separate Services (More Control)
- **Pros**: Full control, cost-effective, flexible
- **Cons**: More setup required
- **Guide**: See `setup_docs/EC2_DEPLOYMENT_GUIDE.md`

### 3. ECS/Fargate (Containerized)
- **Pros**: Scalable, modern, container-based
- **Cons**: Requires Docker knowledge
- **Guide**: Set `ENVIRONMENT=AWS` in task definition

### 4. Lambda (Serverless)
- **Pros**: Pay per use, auto-scaling
- **Cons**: Cold starts, limited execution time
- **Guide**: Set `ENVIRONMENT=AWS` in Lambda env vars

---

## Troubleshooting

### "ENVIRONMENT variable not set"
**Solution**: Add `ENVIRONMENT=DEV` or `ENVIRONMENT=AWS` to your `.env` file or environment variables.

### "AWS_STORAGE_BUCKET_NAME is required"
**Solution**: When `ENVIRONMENT=AWS`, you must set `AWS_STORAGE_BUCKET_NAME`.

### "DATABASE_URL not found"
**Solution**: 
- DEV: No action needed (uses SQLite)
- AWS: Set `DATABASE_URL` environment variable

### Static files not loading
**DEV**: Run `python manage.py collectstatic`
**AWS**: Verify S3 bucket permissions and run `python manage.py collectstatic`

---

## Next Steps

1. **For Local Development**: 
   - Copy `.env.example` to `.env`
   - Set `ENVIRONMENT=DEV`
   - Run `python manage.py runserver 8008`

2. **For AWS Deployment**:
   - Choose deployment method (EC2 or EB)
   - Follow the appropriate guide in `setup_docs/`
   - Set `ENVIRONMENT=AWS` and required variables

3. **Read Documentation**:
   - `setup_docs/ENVIRONMENT_CONFIGURATION.md` - Detailed configuration
   - `setup_docs/EC2_DEPLOYMENT_GUIDE.md` - EC2 deployment
   - `.env.example` - All available variables

---

## Support

For issues or questions:
1. Check `setup_docs/ENVIRONMENT_CONFIGURATION.md` for detailed explanations
2. Review `.env.example` for all available variables
3. Check Django logs for error messages
4. Verify AWS credentials and permissions (for AWS environment)

---

## Summary

✅ **Two environments**: DEV (local) and AWS (production)
✅ **Environment variable**: `ENVIRONMENT=DEV` or `ENVIRONMENT=AWS`
✅ **DEV**: SQLite + local files (no AWS needed)
✅ **AWS**: PostgreSQL (RDS) + S3 storage
✅ **EB support**: Elastic Beanstalk configuration preserved
✅ **IAM roles**: AWS credentials optional on EC2
✅ **Flexible**: Works with EC2, ECS, Lambda, or EB

