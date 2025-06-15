# Budget Tracker System - Deployment Guide

## Overview

This guide covers deploying the Budget Tracker System to various environments, from development to production. It includes best practices for security, performance, and monitoring.

## 🚀 Quick Deployment

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd budget-tracker
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - URL: http://127.0.0.1:5001
   - Admin: Login with username `admin`

## 🔧 Production Deployment

### Prerequisites

- **Server**: Linux server (Ubuntu 20.04+ recommended)
- **Python**: Python 3.7 or higher
- **Web Server**: Nginx or Apache
- **WSGI Server**: Gunicorn or uWSGI
- **Process Manager**: systemd or Supervisor
- **Database**: SQLite (default) or PostgreSQL (recommended for production)

### Step 1: Server Setup

#### Update System
```bash
sudo apt update && sudo apt upgrade -y
```

#### Install Python and Dependencies
```bash
sudo apt install python3 python3-pip python3-venv nginx -y
```

#### Create Application User
```bash
sudo useradd -m -s /bin/bash budgettracker
sudo usermod -aG sudo budgettracker
```

### Step 2: Application Deployment

#### Clone Application
```bash
sudo -u budgettracker git clone <repository-url> /home/budgettracker/app
cd /home/budgettracker/app
```

#### Set up Virtual Environment
```bash
sudo -u budgettracker python3 -m venv venv
sudo -u budgettracker /home/budgettracker/app/venv/bin/pip install -r requirements.txt
```

#### Install Production Dependencies
```bash
sudo -u budgettracker /home/budgettracker/app/venv/bin/pip install gunicorn
```

### Step 3: Configuration

#### Environment Variables
Create `/home/budgettracker/app/.env`:
```bash
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///budget_tracker.db
DEBUG=False
HOST=0.0.0.0
PORT=5001
```

#### Application Configuration
Update `config.py` for production:
```python
class ProductionConfig(Config):
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5001))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_FILE = os.environ.get('DATABASE_FILE', 'budget_tracker.json')
```

### Step 4: WSGI Server Setup

#### Gunicorn Configuration
Create `/home/budgettracker/app/gunicorn.conf.py`:
```python
# Gunicorn configuration file
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

#### Systemd Service
Create `/etc/systemd/system/budgettracker.service`:
```ini
[Unit]
Description=Budget Tracker Gunicorn daemon
After=network.target

[Service]
User=budgettracker
Group=budgettracker
WorkingDirectory=/home/budgettracker/app
Environment="PATH=/home/budgettracker/app/venv/bin"
ExecStart=/home/budgettracker/app/venv/bin/gunicorn --config gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

#### Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable budgettracker
sudo systemctl start budgettracker
sudo systemctl status budgettracker
```

### Step 5: Nginx Configuration

#### Nginx Site Configuration
Create `/etc/nginx/sites-available/budgettracker`:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Logs
    access_log /var/log/nginx/budgettracker_access.log;
    error_log /var/log/nginx/budgettracker_error.log;

    # Static files
    location /static/ {
        alias /home/budgettracker/app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

#### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/budgettracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 6: SSL/HTTPS Setup

#### Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

#### Obtain SSL Certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### Auto-renewal
```bash
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔐 Security Configuration

### Firewall Setup
```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### File Permissions
```bash
sudo chown -R budgettracker:budgettracker /home/budgettracker/app
sudo chmod -R 755 /home/budgettracker/app
sudo chmod 600 /home/budgettracker/app/.env
```

### Database Security
- Use environment variables for database credentials
- Implement database connection pooling
- Regular database backups
- Encrypt sensitive data

## 📊 Monitoring and Logging

### Application Logs
```bash
# View application logs
sudo journalctl -u budgettracker -f

# View Nginx logs
sudo tail -f /var/log/nginx/budgettracker_access.log
sudo tail -f /var/log/nginx/budgettracker_error.log
```

### System Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Monitor system resources
htop
```

### Log Rotation
Create `/etc/logrotate.d/budgettracker`:
```
/home/budgettracker/app/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 budgettracker budgettracker
}
```

## 🔄 Backup Strategy

### Database Backup
Create backup script `/home/budgettracker/backup.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/budgettracker/backups"
mkdir -p $BACKUP_DIR

# Backup database
cp /home/budgettracker/app/budget_tracker.json $BACKUP_DIR/budget_tracker_$DATE.json

# Keep only last 30 days of backups
find $BACKUP_DIR -name "budget_tracker_*.json" -mtime +30 -delete
```

### Automated Backups
```bash
# Make script executable
chmod +x /home/budgettracker/backup.sh

# Add to crontab
sudo crontab -e
# Add this line for daily backups at 2 AM:
0 2 * * * /home/budgettracker/backup.sh
```

## 🚀 Scaling Considerations

### Load Balancing
For high traffic, consider:
- Multiple application servers
- Load balancer (HAProxy, Nginx)
- Database clustering
- CDN for static assets

### Performance Optimization
- Enable Nginx caching
- Use Redis for session storage
- Implement database indexing
- Optimize static file delivery

## 🔧 Maintenance

### Regular Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update application
cd /home/budgettracker/app
sudo -u budgettracker git pull
sudo -u budgettracker /home/budgettracker/app/venv/bin/pip install -r requirements.txt
sudo systemctl restart budgettracker
```

### Health Checks
Create health check endpoint in your application:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

## 🐛 Troubleshooting

### Common Issues

1. **Application won't start**
   ```bash
   sudo systemctl status budgettracker
   sudo journalctl -u budgettracker -n 50
   ```

2. **Nginx errors**
   ```bash
   sudo nginx -t
   sudo tail -f /var/log/nginx/budgettracker_error.log
   ```

3. **Permission issues**
   ```bash
   sudo chown -R budgettracker:budgettracker /home/budgettracker/app
   ```

4. **Port conflicts**
   ```bash
   sudo netstat -tlnp | grep :8000
   sudo lsof -i :8000
   ```

### Performance Issues
- Check system resources: `htop`, `iotop`
- Monitor application logs for slow queries
- Review Nginx access logs for high-traffic patterns
- Check database performance

## 📈 Deployment Checklist

### Pre-deployment
- [ ] Code review completed
- [ ] Tests passing
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] SSL certificates obtained
- [ ] Backup strategy in place

### Deployment
- [ ] Application deployed to server
- [ ] Services started and running
- [ ] Nginx configuration tested
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Monitoring set up

### Post-deployment
- [ ] Application accessible via HTTPS
- [ ] All features working correctly
- [ ] Performance monitoring active
- [ ] Backup system tested
- [ ] Documentation updated
- [ ] Team notified of deployment

## 🆘 Support

For deployment issues:
1. Check application logs: `sudo journalctl -u budgettracker -f`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/budgettracker_error.log`
3. Verify service status: `sudo systemctl status budgettracker`
4. Check file permissions and ownership
5. Review firewall and network configuration

---

*Last updated: December 2024* 