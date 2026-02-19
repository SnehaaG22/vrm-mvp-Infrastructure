#!/usr/bin/env python
"""
Seed test users for QA testing.
Run: python manage.py shell < seed_qa_users.py
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from django.contrib.auth.models import User

# Clear existing users
User.objects.all().delete()

# Create test users
test_users = [
    {
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'testpass123',
        'is_staff': True,
        'is_superuser': True
    },
    {
        'username': 'vendor',
        'email': 'vendor@example.com',
        'password': 'testpass123',
        'is_staff': False,
        'is_superuser': False
    },
    {
        'username': 'reviewer',
        'email': 'reviewer@example.com',
        'password': 'testpass123',
        'is_staff': False,
        'is_superuser': False
    }
]

for user_data in test_users:
    pwd = user_data.pop('password')
    user = User.objects.create_user(password=pwd, **user_data)
    print(f"✓ Created: {user.username} ({user.email}) - staff:{user.is_staff}, superuser:{user.is_superuser}")

print("\nUsers ready for QA testing.")
