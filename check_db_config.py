#!/usr/bin/env python3
"""
Database Configuration Checker
Run this script to verify your database configuration before deployment
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitnbuild.settings')
django.setup()

from django.conf import settings
from django.db import connection

def check_database_config():
    print("🔍 Checking Database Configuration...")
    print("-" * 50)
    
    # Check current database engine
    db_engine = settings.DATABASES['default']['ENGINE']
    print(f"Database Engine: {db_engine}")
    
    if 'postgresql' in db_engine:
        print("✅ PostgreSQL configured")
        db_name = settings.DATABASES['default'].get('NAME', 'Not specified')
        db_host = settings.DATABASES['default'].get('HOST', 'Not specified')
        db_port = settings.DATABASES['default'].get('PORT', 'Not specified')
        print(f"   Database: {db_name}")
        print(f"   Host: {db_host}")
        print(f"   Port: {db_port}")
    elif 'sqlite' in db_engine:
        print("⚠️  SQLite configured (OK for development, not recommended for production)")
        db_path = settings.DATABASES['default'].get('NAME', 'Not specified')
        print(f"   Database file: {db_path}")
    else:
        print(f"❌ Unknown database engine: {db_engine}")
    
    # Check environment variables
    print("\n🔧 Environment Variables:")
    print("-" * 50)
    
    env_vars = [
        'DATABASE_URL',
        'SECRET_KEY', 
        'DEBUG',
        'GOOGLE_API_KEY',
        'GOOGLE_OAUTH2_KEY',
        'GOOGLE_OAUTH2_SECRET'
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            if 'SECRET' in var or 'KEY' in var:
                print(f"✅ {var}: ***hidden***")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
    
    # Test database connection
    print("\n🔌 Testing Database Connection:")
    print("-" * 50)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Database connection successful!")
            else:
                print("❌ Database connection failed - no result")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Make sure your database is running and credentials are correct")
    
    # Check if this is production configuration
    print("\n🚀 Production Readiness:")
    print("-" * 50)
    
    debug_mode = settings.DEBUG
    if debug_mode:
        print("⚠️  DEBUG=True (OK for development)")
    else:
        print("✅ DEBUG=False (Production ready)")
    
    if 'postgresql' in db_engine and not debug_mode:
        print("✅ Ready for production deployment")
    elif 'sqlite' in db_engine and not debug_mode:
        print("⚠️  Using SQLite in production - consider PostgreSQL")
    else:
        print("ℹ️  Development configuration")

if __name__ == '__main__':
    check_database_config()
