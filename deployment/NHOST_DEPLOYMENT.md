# Nhost Deployment Guide for Budge-IT

This guide will help you deploy your Budge-IT Flask application to Nhost.

## Prerequisites

1. **Nhost Account**: Sign up at [nhost.io](https://nhost.io)
2. **Nhost CLI**: Install the Nhost CLI
   ```bash
   npm install -g nhost
   ```
3. **Docker**: Ensure Docker is installed on your system

## Step 1: Initialize Nhost Project

1. **Login to Nhost CLI**:
   ```bash
   nhost login
   ```

2. **Create a new project**:
   ```bash
   nhost init budge-it
   cd budge-it
   ```

3. **Link your existing code**:
   ```bash
   # Copy your Flask app files to the project directory
   cp -r /path/to/your/flask/app/* .
   ```

## Step 2: Configure Environment Variables

1. **Copy the environment template**:
   ```bash
   cp deployment/nhost.env.example .env
   ```

2. **Edit the .env file** with your actual values:
   ```bash
   # Generate a secure secret key
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Set up your database URL**:
   - Use the Nhost PostgreSQL connection string
   - Format: `postgresql://nhost:password@localhost:5432/budge_it`

## Step 3: Database Setup

1. **Run the database schema**:
   ```bash
   # Connect to Nhost PostgreSQL
   nhost db connect
   
   # Run the schema file
   psql -f deployment/supabase_schema.sql
   ```

2. **Initialize the database**:
   ```bash
   python -c "from app import create_app; from app.utils.database import initialize_database; app = create_app(); initialize_database(app)"
   ```

## Step 4: Deploy to Nhost

1. **Build and deploy**:
   ```bash
   nhost up
   ```

2. **Check deployment status**:
   ```bash
   nhost status
   ```

3. **View logs**:
   ```bash
   nhost logs
   ```

## Step 5: Configure Custom Domain (Optional)

1. **Add custom domain in Nhost dashboard**
2. **Update DNS records** as instructed
3. **Configure SSL certificate**

## Environment Variables Reference

### Required Variables
- `SECRET_KEY`: Flask secret key for session management
- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_ENV`: Set to 'production'
- `FLASK_APP`: Set to 'wsgi.py'

### Optional Variables
- `NHOST_BACKEND_URL`: Your Nhost backend URL
- `NHOST_GRAPHQL_URL`: GraphQL endpoint (if using)
- `NHOST_STORAGE_URL`: File storage endpoint (if using)

## Health Check

Your application includes a health check endpoint at `/health` that returns:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000000",
  "service": "budge-it"
}
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Verify `DATABASE_URL` is correct
   - Check if PostgreSQL service is running
   - Ensure database exists

2. **Import Errors**:
   - Check if all dependencies are in `requirements.txt`
   - Verify Python path is set correctly

3. **Port Conflicts**:
   - Ensure port 3000 is available
   - Check if other services are using the same port

### Useful Commands

```bash
# View application logs
nhost logs

# Restart services
nhost restart

# Check service status
nhost status

# Access database
nhost db connect

# View environment variables
nhost env list
```

## Monitoring

- **Nhost Dashboard**: Monitor your application performance
- **Logs**: View real-time application logs
- **Metrics**: Track resource usage and performance

## Security Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **Secret Key**: Use a strong, random secret key
3. **Database**: Use connection pooling for better performance
4. **HTTPS**: Always use HTTPS in production
5. **Updates**: Keep dependencies updated

## Support

- **Nhost Documentation**: [docs.nhost.io](https://docs.nhost.io)
- **Community**: [discord.nhost.io](https://discord.nhost.io)
- **GitHub Issues**: Report bugs in your repository

## Next Steps

After successful deployment:

1. **Test all features** thoroughly
2. **Set up monitoring** and alerts
3. **Configure backups** for your database
4. **Set up CI/CD** for automated deployments
5. **Document your deployment** process 