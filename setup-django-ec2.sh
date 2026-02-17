#!/bin/bash

# EC2 Django + RDS PostgreSQL Setup Script
# Run this script on a fresh EC2 instance (Ubuntu 20.04/22.04)
# Make executable with: chmod +x setup-django-ec2.sh
# Run with: ./setup-django-ec2.sh

set -e  # Exit on any error
set -u  # Exit on undefined variable

# Color codes for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}EC2 Django + RDS PostgreSQL Setup Script${NC}"
echo -e "${GREEN}========================================${NC}"

# ----------------------------
# COLLECT USER INPUT
# ----------------------------
echo -e "\n${YELLOW}Step 1: Gathering Configuration Information${NC}"

# Project information
read -p "Enter your Django project name (e.g., myproject): " PROJECT_NAME
read -p "Enter your GitHub repository URL (or leave blank to skip clone): " GITHUB_URL
read -p "Enter your EC2 public IP address: " EC2_IP

# RDS Connection Information
echo -e "\n${YELLOW}Enter RDS Connection Details:${NC}"
read -p "RDS Endpoint (e.g., mydb.xxxxxx.us-east-1.rds.amazonaws.com): " RDS_ENDPOINT
read -p "RDS Database Name (default: postgres): " RDS_DBNAME
RDS_DBNAME=${RDS_DBNAME:-postgres}  # Default to postgres if empty
read -p "RDS Username: " RDS_USER
read -sp "RDS Password: " RDS_PASSWORD
echo  # New line after password input
read -p "RDS Port (default: 5432): " RDS_PORT
RDS_PORT=${RDS_PORT:-5432}

# SSL certificate path (optional)
read -p "Path to SSL certificate (leave blank if not using SSL): " SSL_CERT_PATH

# ----------------------------
# SYSTEM UPDATE & PACKAGES
# ----------------------------
echo -e "\n${GREEN}Step 2: Updating system and installing packages${NC}"
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx git postgresql-client

# ----------------------------
# INSTALL & CONFIGURE GUNICORN
# ----------------------------
echo -e "\n${GREEN}Step 3: Setting up Python environment and Gunicorn${NC}"
cd /home/ubuntu

# Clone repository if provided
if [ ! -z "$GITHUB_URL" ]; then
    echo -e "${YELLOW}Cloning repository...${NC}"
    git clone "$GITHUB_URL"
    # Extract directory name from repo URL
    REPO_DIR=$(basename "$GITHUB_URL" .git)
    cd "$REPO_DIR"
else
    echo -e "${YELLOW}No repository provided. Please ensure your code is in /home/ubuntu/$PROJECT_NAME${NC}"
    mkdir -p "/home/ubuntu/$PROJECT_NAME"
    cd "/home/ubuntu/$PROJECT_NAME"
fi

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo -e "${RED}requirements.txt not found. Creating basic one...${NC}"
    pip install django gunicorn psycopg2-binary
    pip freeze > requirements.txt
fi

# Install psycopg2 if not already in requirements
pip install psycopg2-binary

# ----------------------------
# CREATE ENVIRONMENT VARIABLES SCRIPT
# ----------------------------
echo -e "\n${GREEN}Step 4: Creating environment variables${NC}"
cat > /home/ubuntu/$PROJECT_NAME/.env << EOF
# Django Settings
DJANGO_SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
DJANGO_DEBUG="False"
DJANGO_ALLOWED_HOSTS="$EC2_IP,localhost"

# RDS Database Settings
RDS_HOSTNAME="$RDS_ENDPOINT"
RDS_DB_NAME="$RDS_DBNAME"
RDS_USERNAME="$RDS_USER"
RDS_PASSWORD="$RDS_PASSWORD"
RDS_PORT="$RDS_PORT"

# Optional SSL Certificate
RDS_SSL_CERT="$SSL_CERT_PATH"
EOF

echo -e "${GREEN}✓ Environment variables created at /home/ubuntu/$PROJECT_NAME/.env${NC}"

# ----------------------------
# S3 CONFIGURATION SECTION
# ----------------------------
echo -e "\n${GREEN}Step: Configuring S3 for Static and Media Files${NC}"

# Collect S3 information
read -p "Enter your S3 bucket name (e.g., your-project-media): " S3_BUCKET
read -p "Enter your AWS Access Key ID: " AWS_ACCESS_KEY
read -sp "Enter your AWS Secret Access Key: " AWS_SECRET_KEY
echo
read -p "Enter AWS Region (default: us-east-1): " AWS_REGION
AWS_REGION=${AWS_REGION:-us-east-1}

# Add to environment variables
cat >> /home/ubuntu/$PROJECT_NAME/.env << EOF

# AWS S3 Settings
AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY="$AWS_SECRET_KEY"
AWS_STORAGE_BUCKET_NAME="$S3_BUCKET"
AWS_S3_REGION_NAME="$AWS_REGION"
EOF

# Install required packages
source /home/ubuntu/$PROJECT_NAME/venv/bin/activate
pip install boto3 django-storages

# Update settings.py - append S3 configuration
SETTINGS_FILE=$(find /home/ubuntu/$PROJECT_NAME -name "settings.py" | head -1)

cat >> "$SETTINGS_FILE" << 'EOF'

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Django Storages Configuration
INSTALLED_APPS += ['storages']

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "default_acl": AWS_DEFAULT_ACL,
            "querystring_auth": AWS_QUERYSTRING_AUTH,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "location": "static",
            "default_acl": "public-read",
            "querystring_auth": False,
        },
    },
}

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
EOF

# Run collectstatic
echo -e "${YELLOW}Running collectstatic to upload files to S3...${NC}"
cd /home/ubuntu/$PROJECT_NAME
source venv/bin/activate
export $(cat /home/ubuntu/$PROJECT_NAME/.env | xargs)
python manage.py collectstatic --noinput

echo -e "${GREEN}✓ S3 configuration complete!${NC}"
echo -e "Static files are now served from: https://$S3_BUCKET.s3.amazonaws.com/static/"

# ----------------------------
# UPDATE DJANGO SETTINGS
# ----------------------------
echo -e "\n${GREEN}Step 5: Updating Django settings${NC}"

# Find settings file
SETTINGS_FILE=$(find /home/ubuntu/$PROJECT_NAME -name "settings.py" | head -1)

if [ -f "$SETTINGS_FILE" ]; then
    # Backup original settings
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.bak"
    
    # Update DATABASES section
    cat >> "$SETTINGS_FILE" << 'EOF'

# Production Database Configuration (RDS)
import os
from pathlib import Path

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('RDS_DB_NAME'),
        'USER': os.environ.get('RDS_USERNAME'),
        'PASSWORD': os.environ.get('RDS_PASSWORD'),
        'HOST': os.environ.get('RDS_HOSTNAME'),
        'PORT': os.environ.get('RDS_PORT', '5432'),
        'CONN_MAX_AGE': 60,
    }
}

# SSL configuration for RDS
if os.environ.get('RDS_SSL_CERT'):
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'verify-full',
        'sslrootcert': os.environ.get('RDS_SSL_CERT'),
    }

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Security settings
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
EOF
    echo -e "${GREEN}✓ Django settings updated${NC}"
else
    echo -e "${RED}Could not find settings.py. Please update manually.${NC}"
fi

# ----------------------------
# DATABASE MIGRATION
# ----------------------------
echo -e "\n${GREEN}Step 6: Running database migrations${NC}"
source venv/bin/activate
export $(cat /home/ubuntu/$PROJECT_NAME/.env | xargs)

# Test database connection
echo -e "${YELLOW}Testing database connection...${NC}"
if command -v psql &> /dev/null; then
    if PGPASSWORD="$RDS_PASSWORD" psql -h "$RDS_ENDPOINT" -U "$RDS_USER" -d "$RDS_DBNAME" -p "$RDS_PORT" -c "\l" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Database connection successful${NC}"
    else
        echo -e "${RED}✗ Database connection failed. Please check your credentials.${NC}"
        echo -e "${YELLOW}Continuing anyway...${NC}"
    fi
fi

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser (optional)
echo -e "\n${YELLOW}Do you want to create a superuser? (y/n)${NC}"
read CREATE_SUPERUSER
if [ "$CREATE_SUPERUSER" = "y" ]; then
    python manage.py createsuperuser
fi

# ----------------------------
# CONFIGURE GUNICORN SERVICE
# ----------------------------
echo -e "\n${GREEN}Step 7: Configuring Gunicorn service${NC}"

# Create Gunicorn socket file
sudo bash -c "cat > /etc/systemd/system/gunicorn.socket" << EOF
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

# Create Gunicorn service file
sudo bash -c "cat > /etc/systemd/system/gunicorn.service" << EOF
[Unit]
Description=gunicorn daemon for $PROJECT_NAME
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/$PROJECT_NAME
EnvironmentFile=/home/ubuntu/$PROJECT_NAME/.env
ExecStart=/home/ubuntu/$PROJECT_NAME/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          ${PROJECT_NAME}.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start and enable Gunicorn
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Check Gunicorn status
sudo systemctl status gunicorn --no-pager

# ----------------------------
# CONFIGURE NGINX
# ----------------------------
echo -e "\n${GREEN}Step 8: Configuring Nginx${NC}"

# Create Nginx configuration
sudo bash -c "cat > /etc/nginx/sites-available/$PROJECT_NAME" << EOF
server {
    listen 80;
    server_name $EC2_IP;

    # Log files
    access_log /var/log/nginx/${PROJECT_NAME}_access.log;
    error_log /var/log/nginx/${PROJECT_NAME}_error.log;

    # Static files
    location /static/ {
        alias /home/ubuntu/$PROJECT_NAME/static/;
    }

    # Media files
    location /media/ {
        alias /home/ubuntu/$PROJECT_NAME/media/;
    }

    # Proxy requests to Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

# Enable site and remove default
sudo ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# ----------------------------
# SET PROPER PERMISSIONS
# ----------------------------
echo -e "\n${GREEN}Step 9: Setting file permissions${NC}"
sudo chown -R ubuntu:www-data /home/ubuntu/$PROJECT_NAME/static/
sudo chmod -R 755 /home/ubuntu/$PROJECT_NAME/static/
sudo chown -R ubuntu:www-data /home/ubuntu/$PROJECT_NAME/media/
sudo chmod -R 755 /home/ubuntu/$PROJECT_NAME/media/
sudo chmod 644 /home/ubuntu/$PROJECT_NAME/.env

# ----------------------------
# FINAL STATUS CHECK
# ----------------------------
echo -e "\n${GREEN}Step 10: Checking service status${NC}"
echo -e "\n${YELLOW}Gunicorn status:${NC}"
sudo systemctl status gunicorn --no-pager

echo -e "\n${YELLOW}Nginx status:${NC}"
sudo systemctl status nginx --no-pager

echo -e "\n${YELLOW}Recent logs:${NC}"
sudo journalctl -u gunicorn -n 10 --no-pager

# ----------------------------
# COMPLETION MESSAGE
# ----------------------------
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "Your Django application should be available at: ${YELLOW}http://$EC2_IP${NC}"
echo -e "\n${YELLOW}Useful commands:${NC}"
echo -e "  - View Gunicorn logs: sudo journalctl -u gunicorn -f"
echo -e "  - View Nginx logs: sudo tail -f /var/log/nginx/${PROJECT_NAME}_*.log"
echo -e "  - Restart Gunicorn: sudo systemctl restart gunicorn"
echo -e "  - Restart Nginx: sudo systemctl restart nginx"
echo -e "  - SSH into instance: ssh ubuntu@$EC2_IP"
echo -e "\n${YELLOW}Environment variables are stored in:${NC} /home/ubuntu/$PROJECT_NAME/.env"
echo -e "${GREEN}========================================${NC}"