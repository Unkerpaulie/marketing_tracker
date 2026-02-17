# Quick Reference Card

## Environment Setup

### Local Development (DEV)
```bash
# .env file
ENVIRONMENT=DEV
DEBUG=True
SECRET_KEY=your-dev-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### AWS Production
```bash
# Environment variables
ENVIRONMENT=AWS
DEBUG=False
SECRET_KEY=your-production-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@rds-host:5432/dbname
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Optional (if not using IAM role)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

---

## Common Commands

### Local Development
```bash
# Setup
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8008

# Collect static files
python manage.py collectstatic
```

### AWS EC2 Deployment
```bash
# On EC2 instance
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn marketing_tracker.wsgi:application --bind 0.0.0.0:8000

# Systemd service
sudo systemctl start marketing-tracker
sudo systemctl status marketing-tracker
sudo systemctl restart marketing-tracker
sudo journalctl -u marketing-tracker -f
```

### Elastic Beanstalk
```bash
# Initialize
eb init

# Create environment
eb create

# Deploy
eb deploy

# Open in browser
eb open

# View logs
eb logs

# SSH to instance
eb ssh
```

---

## What Runs Where?

| Component | DEV | AWS |
|-----------|-----|-----|
| **Database** | SQLite (`db.sqlite3`) | PostgreSQL (RDS) |
| **Static Files** | Local (`staticfiles/`) | S3 (`bucket/static/`) |
| **Media Files** | Local (`media/`) | S3 (`bucket/media/`) |
| **Web Server** | Django dev server | Gunicorn + Nginx |
| **AWS Credentials** | Not needed | Optional (IAM role) |

---

## File Structure

```
marketing_tracker/
├── .env                          # Your local environment variables (not in git)
├── .env.example                  # Template for environment variables
├── .ebextensions/                # Elastic Beanstalk configuration (preserved)
│   ├── 01_django.config
│   └── 02_python.config
├── marketing_tracker/
│   └── settings.py               # Environment-aware settings
├── ENVIRONMENT_SETUP_README.md   # Quick start guide
├── DEPLOYMENT_CHECKLIST.md       # Deployment checklist
├── QUICK_REFERENCE.md            # This file
└── setup_docs/
    ├── ENVIRONMENT_CONFIGURATION.md
    ├── EC2_DEPLOYMENT_GUIDE.md
    ├── DEPLOYMENT_OPTIONS_COMPARISON.md
    └── CONFIGURATION_CHANGES_SUMMARY.md
```

---

## Troubleshooting

### Application won't start
```bash
# Check environment variable
echo $ENVIRONMENT  # Should be DEV or AWS

# Check Django settings
python manage.py check

# View detailed errors
python manage.py runserver --traceback
```

### Database connection error
```bash
# DEV: Should use SQLite automatically
ls -la db.sqlite3

# AWS: Test PostgreSQL connection
psql -h your-rds-endpoint -U dbadmin -d postgres
```

### Static files not loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# DEV: Check local directory
ls -la staticfiles/

# AWS: Check S3 bucket
aws s3 ls s3://your-bucket-name/static/
```

### S3 access denied
```bash
# Check IAM role (on EC2)
aws sts get-caller-identity

# Test S3 access
aws s3 ls s3://your-bucket-name/

# Check environment variables
echo $AWS_STORAGE_BUCKET_NAME
echo $AWS_S3_REGION_NAME
```

---

## Environment Variables Explained

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENVIRONMENT` | Yes | `DEV` | `DEV` or `AWS` |
| `DEBUG` | Yes | `False` | Django debug mode |
| `SECRET_KEY` | Yes | (insecure default) | Django secret key |
| `ALLOWED_HOSTS` | No | `localhost,127.0.0.1` | Allowed hostnames |
| `DATABASE_URL` | AWS only | None | PostgreSQL connection string |
| `AWS_STORAGE_BUCKET_NAME` | AWS only | None | S3 bucket name |
| `AWS_S3_REGION_NAME` | AWS only | `us-east-1` | AWS region |
| `AWS_ACCESS_KEY_ID` | Optional | None | AWS access key (or use IAM role) |
| `AWS_SECRET_ACCESS_KEY` | Optional | None | AWS secret key (or use IAM role) |

---

## Deployment Options Comparison

| Option | Cost/Month | Complexity | Best For |
|--------|------------|------------|----------|
| **EC2 + Services** | ~$25-30 | Medium | Full control, learning |
| **Elastic Beanstalk** | ~$50-60 | Low | Quick deployment |
| **ECS/Fargate** | ~$35-40 | Medium-High | Containers, microservices |
| **Lambda** | ~$20-25 | High | Low traffic, serverless |

---

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` (50+ random characters)
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] Database credentials secure
- [ ] AWS credentials secure (or using IAM role)
- [ ] `.env` file in `.gitignore`
- [ ] HTTPS enabled (recommended)
- [ ] S3 bucket permissions configured correctly

---

## Next Steps

### For Local Development
1. `cp .env.example .env`
2. Edit `.env` and set `ENVIRONMENT=DEV`
3. `python manage.py migrate`
4. `python manage.py runserver 8008`

### For AWS Deployment
1. Choose deployment method (EC2 or EB)
2. Create AWS resources (RDS, S3)
3. Set environment variables
4. Follow deployment guide
5. Test thoroughly

---

## Documentation Links

- **Quick Start**: `ENVIRONMENT_SETUP_README.md`
- **Detailed Config**: `setup_docs/ENVIRONMENT_CONFIGURATION.md`
- **EC2 Guide**: `setup_docs/EC2_DEPLOYMENT_GUIDE.md`
- **Deployment Options**: `setup_docs/DEPLOYMENT_OPTIONS_COMPARISON.md`
- **Changes Summary**: `setup_docs/CONFIGURATION_CHANGES_SUMMARY.md`
- **Deployment Checklist**: `DEPLOYMENT_CHECKLIST.md`

---

## Support

### Common Issues

**"ENVIRONMENT variable not set"**
→ Add `ENVIRONMENT=DEV` to `.env` file

**"AWS_STORAGE_BUCKET_NAME is required"**
→ Set when `ENVIRONMENT=AWS`

**"DATABASE_URL not found"**
→ Required when `ENVIRONMENT=AWS`

**Static files not loading**
→ Run `python manage.py collectstatic`

**S3 access denied**
→ Check IAM role or AWS credentials

---

## Summary

✅ **Two environments**: DEV (local) and AWS (production)
✅ **Simple setup**: Just set `ENVIRONMENT` variable
✅ **Flexible**: Works with EC2, EB, ECS, Lambda
✅ **Secure**: IAM role support, no credentials needed
✅ **Well-documented**: Multiple guides available

**Get Started**: Copy `.env.example` to `.env` and set `ENVIRONMENT=DEV`

