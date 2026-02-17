# Deployment Checklist

## Local Development Setup

- [ ] Copy `.env.example` to `.env`
- [ ] Set `ENVIRONMENT=DEV` in `.env`
- [ ] Set `DEBUG=True` in `.env`
- [ ] Set `SECRET_KEY` in `.env`
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py createsuperuser`
- [ ] Run `python manage.py runserver 8008`
- [ ] Test application at `http://localhost:8008`
- [ ] Verify SQLite database is created
- [ ] Test file upload (should save to `media/` folder)

---

## AWS Deployment - Pre-Deployment

### AWS Resources Setup
- [ ] Create S3 bucket for static/media files
- [ ] Configure S3 bucket CORS and permissions
- [ ] Create RDS PostgreSQL database
- [ ] Configure RDS security group
- [ ] Create IAM role with S3 and RDS permissions (if using EC2)
- [ ] Note down:
  - S3 bucket name
  - RDS endpoint
  - RDS username/password
  - AWS region

### Environment Variables Preparation
- [ ] Prepare `ENVIRONMENT=AWS`
- [ ] Prepare `DEBUG=False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Prepare `ALLOWED_HOSTS` (your domain)
- [ ] Prepare `DATABASE_URL` (PostgreSQL connection string)
- [ ] Prepare `AWS_STORAGE_BUCKET_NAME`
- [ ] Prepare `AWS_S3_REGION_NAME`
- [ ] Prepare AWS credentials (if not using IAM role)

---

## AWS Deployment - Option 1: EC2

### EC2 Instance Setup
- [ ] Launch EC2 instance (Ubuntu/Amazon Linux)
- [ ] Attach IAM role to EC2 instance
- [ ] Configure security group (ports 22, 80, 443, 8000)
- [ ] Connect to EC2 via SSH
- [ ] Update system: `sudo apt update && sudo apt upgrade -y`
- [ ] Install Python: `sudo apt install python3 python3-pip python3-venv -y`
- [ ] Install PostgreSQL client: `sudo apt install postgresql-client libpq-dev -y`
- [ ] Install Nginx: `sudo apt install nginx -y`

### Application Deployment
- [ ] Clone repository to EC2
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Create `.env` file with AWS environment variables
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Test with: `python manage.py runserver 0.0.0.0:8000`

### Production Setup
- [ ] Install Gunicorn: `pip install gunicorn`
- [ ] Create systemd service file
- [ ] Enable and start service
- [ ] Configure Nginx as reverse proxy
- [ ] Test Nginx configuration
- [ ] Restart Nginx
- [ ] Test application via domain/IP

### Verification
- [ ] Application accessible via browser
- [ ] Static files loading from S3
- [ ] File upload works (saves to S3)
- [ ] Database connection working
- [ ] Admin panel accessible
- [ ] No errors in logs

---

## AWS Deployment - Option 2: Elastic Beanstalk

### EB CLI Setup
- [ ] Install EB CLI: `pip install awsebcli`
- [ ] Verify: `eb --version`

### EB Initialization
- [ ] Run `eb init` in project directory
- [ ] Select region
- [ ] Select platform (Python 3.12)
- [ ] Configure SSH (optional)

### Environment Variables Setup
- [ ] Go to EB Console → Environment → Configuration → Software
- [ ] Add environment variables:
  - [ ] `ENVIRONMENT=AWS`
  - [ ] `DEBUG=False`
  - [ ] `SECRET_KEY=your-production-key`
  - [ ] `ALLOWED_HOSTS=your-domain.com`
  - [ ] `DATABASE_URL=postgresql://...`
  - [ ] `AWS_STORAGE_BUCKET_NAME=your-bucket`
  - [ ] `AWS_S3_REGION_NAME=us-east-1`

### Deployment
- [ ] Run `eb create` to create environment
- [ ] Wait for environment to be ready
- [ ] Run `eb deploy` to deploy application
- [ ] Run `eb open` to open in browser

### Post-Deployment
- [ ] SSH to EB instance: `eb ssh`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Collect static files: `python manage.py collectstatic --noinput`

### Verification
- [ ] Application accessible via EB URL
- [ ] Static files loading from S3
- [ ] File upload works (saves to S3)
- [ ] Database connection working
- [ ] Admin panel accessible
- [ ] Check EB logs: `eb logs`

---

## Post-Deployment Verification

### Functionality Tests
- [ ] Homepage loads correctly
- [ ] Static files (CSS, JS) loading
- [ ] Media files (images) loading
- [ ] Admin panel accessible
- [ ] Login/logout working
- [ ] Create new post
- [ ] Upload image
- [ ] Edit post
- [ ] Delete post

### Performance Tests
- [ ] Page load time acceptable
- [ ] Database queries optimized
- [ ] S3 files loading quickly
- [ ] No 500 errors

### Security Tests
- [ ] DEBUG=False in production
- [ ] SECRET_KEY is strong and unique
- [ ] ALLOWED_HOSTS configured correctly
- [ ] HTTPS enabled (if applicable)
- [ ] Database credentials secure
- [ ] AWS credentials secure (or using IAM role)

---

## Monitoring and Maintenance

### Regular Checks
- [ ] Monitor application logs
- [ ] Monitor database performance
- [ ] Monitor S3 storage usage
- [ ] Monitor EC2/EB instance health
- [ ] Check for Django security updates
- [ ] Check for dependency updates

### Backup Strategy
- [ ] Database backups configured
- [ ] S3 versioning enabled (optional)
- [ ] Code repository backed up

---

## Troubleshooting

### If application won't start:
1. Check environment variables are set correctly
2. Check Django logs
3. Verify database connection
4. Verify S3 bucket access

### If static files not loading:
1. Run `python manage.py collectstatic`
2. Check S3 bucket permissions
3. Verify `AWS_STORAGE_BUCKET_NAME` is correct
4. Check browser console for errors

### If database errors:
1. Verify `DATABASE_URL` is correct
2. Check RDS security group
3. Test database connection manually
4. Check RDS instance is running

### If S3 errors:
1. Verify S3 bucket exists
2. Check IAM role permissions
3. Check AWS credentials (if not using IAM role)
4. Verify bucket policy

---

## Quick Reference

### Environment Variables

**DEV:**
```bash
ENVIRONMENT=DEV
DEBUG=True
SECRET_KEY=your-dev-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

**AWS:**
```bash
ENVIRONMENT=AWS
DEBUG=False
SECRET_KEY=your-production-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1
```

### Useful Commands

**Local:**
```bash
python manage.py runserver 8008
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

**Production:**
```bash
gunicorn marketing_tracker.wsgi:application --bind 0.0.0.0:8000
sudo systemctl status marketing-tracker
sudo systemctl restart marketing-tracker
sudo journalctl -u marketing-tracker -f
```

**EB:**
```bash
eb init
eb create
eb deploy
eb open
eb logs
eb ssh
```

---

## Documentation

- **Quick Start**: `ENVIRONMENT_SETUP_README.md`
- **Configuration**: `setup_docs/ENVIRONMENT_CONFIGURATION.md`
- **EC2 Guide**: `setup_docs/EC2_DEPLOYMENT_GUIDE.md`
- **Deployment Options**: `setup_docs/DEPLOYMENT_OPTIONS_COMPARISON.md`
- **Changes Summary**: `setup_docs/CONFIGURATION_CHANGES_SUMMARY.md`

