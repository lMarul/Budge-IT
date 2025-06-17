#!/bin/bash

# Budge-IT Deployment Script
# This script helps with deployment and monitoring

echo "🚀 Budge-IT Deployment Helper"
echo "=============================="

# Function to check application health
check_health() {
    echo "🔍 Checking application health..."
    
    # Check basic health
    echo "Basic health check:"
    curl -s https://budge-it-j4bp.onrender.com/health | jq . 2>/dev/null || curl -s https://budge-it-j4bp.onrender.com/health
    
    echo -e "\nDatabase status:"
    curl -s https://budge-it-j4bp.onrender.com/test-db | jq . 2>/dev/null || curl -s https://budge-it-j4bp.onrender.com/test-db
    
    echo -e "\nSupabase connection:"
    curl -s https://budge-it-j4bp.onrender.com/check-supabase | jq . 2>/dev/null || curl -s https://budge-it-j4bp.onrender.com/check-supabase
}

# Function to show deployment status
show_status() {
    echo "📊 Current Deployment Status:"
    echo "=============================="
    echo "Application URL: https://budge-it-j4bp.onrender.com"
    echo "Repository: https://github.com/lMarul/Budge-IT"
    echo ""
    echo "Health Check Endpoints:"
    echo "- /health - Basic application health"
    echo "- /test-db - Database connection test"
    echo "- /check-supabase - Supabase connection status"
    echo "- /database-status - Detailed database status"
}

# Function to help with Supabase issues
supabase_help() {
    echo "🔧 Supabase Connection Issues Help"
    echo "=================================="
    echo ""
    echo "If you're seeing 'Max client connections reached':"
    echo "1. Your data is SAFE in Supabase"
    echo "2. This is a connection limit issue, not data loss"
    echo "3. Wait 15-30 minutes for limits to reset"
    echo "4. Or upgrade your Supabase plan"
    echo ""
    echo "To monitor when it's back online:"
    echo "curl https://budge-it-j4bp.onrender.com/check-supabase"
    echo ""
    echo "To check overall health:"
    echo "curl https://budge-it-j4bp.onrender.com/health"
}

# Function to show recent changes
show_changes() {
    echo "📝 Recent Deployment Changes"
    echo "============================"
    echo ""
    echo "✅ Fixed Gunicorn worker timeout issues"
    echo "✅ Added database connection pooling"
    echo "✅ Improved Supabase connection handling"
    echo "✅ Added health check endpoints"
    echo "✅ Enhanced error handling and logging"
    echo ""
    echo "Configuration updates:"
    echo "- Increased Gunicorn timeout to 120 seconds"
    echo "- Added connection pooling for Supabase"
    echo "- Implemented retry logic for database operations"
    echo "- Added comprehensive health monitoring"
}

# Main script logic
case "${1:-help}" in
    "health"|"check")
        check_health
        ;;
    "status")
        show_status
        ;;
    "supabase"|"db")
        supabase_help
        ;;
    "changes"|"updates")
        show_changes
        ;;
    "deploy"|"redeploy")
        echo "🔄 To redeploy:"
        echo "1. Push changes to GitHub:"
        echo "   git add ."
        echo "   git commit -m 'Update deployment configuration'"
        echo "   git push origin main"
        echo ""
        echo "2. Render will automatically redeploy"
        echo "3. Monitor deployment at: https://dashboard.render.com"
        echo ""
        echo "4. Check health after deployment:"
        echo "   ./deploy.sh health"
        ;;
    *)
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  health, check    - Check application health"
        echo "  status          - Show deployment status"
        echo "  supabase, db    - Help with Supabase issues"
        echo "  changes, updates - Show recent changes"
        echo "  deploy, redeploy - Instructions for redeployment"
        echo "  help            - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 health       # Check if app is working"
        echo "  $0 supabase     # Get help with database issues"
        echo "  $0 deploy       # Instructions for redeployment"
        ;;
esac 