#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download YOLO model if not present
if [ ! -f "yolov8n.pt" ]; then
    echo "Downloading YOLOv8 model..."
    wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
fi

# Create necessary directories
mkdir -p staticfiles
mkdir -p media
mkdir -p faiss_index

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

# Check database configuration
echo "Checking database configuration..."
python manage.py shell -c "
from django.db import connection
from django.conf import settings
print(f'Database engine: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
if 'postgresql' in settings.DATABASES['default']['ENGINE']:
    print('✓ Using PostgreSQL for production')
else:
    print('⚠ Using SQLite - this may not be suitable for production')
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print('✓ Database connection successful')
except Exception as e:
    print(f'✗ Database connection failed: {e}')
"

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
import os
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', os.environ.get('ADMIN_PASSWORD', 'admin123'))
    print('✓ Superuser created')
else:
    print('✓ Superuser already exists')
"

echo "✓ Build completed successfully!"
