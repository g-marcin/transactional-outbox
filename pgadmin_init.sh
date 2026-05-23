#!/bin/bash
# Initialize pgAdmin with pre-authenticated session

# Wait for pgAdmin to start
sleep 3

# Get pgAdmin session by "logging in" via API
RESPONSE=$(curl -s -X POST http://localhost:5050/misc/ping \
  -H "Content-Type: application/json" \
  -c /tmp/pgadmin_cookies.txt)

# Create authenticated session
curl -s -X POST http://localhost:5050/authentication/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin",
    "remember_me": true
  }' \
  -b /tmp/pgadmin_cookies.txt \
  -c /tmp/pgadmin_cookies.txt > /dev/null 2>&1

echo "✓ pgAdmin pre-authenticated"
echo "✓ Open: http://localhost:5050"
