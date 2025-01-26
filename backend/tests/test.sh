#!/bin/bash

# Base URL
BASE_URL="http://127.0.0.1:8000/api"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}1. Registering new user...${NC}"
curl -X POST $BASE_URL/register/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "testuser",
           "password": "testpass123"
         }' | python -m json.tool

echo -e "\n${GREEN}2. Logging in...${NC}"
TOKEN=$(curl -X POST $BASE_URL/login/ \
        -H "Content-Type: application/json" \
        -d '{
              "username": "testuser",
              "password": "testpass123"
            }' | python -c "import sys, json; print(json.load(sys.stdin)['token'])")

echo "Token received: $TOKEN"

echo -e "\n${GREEN}3. Updating portfolio...${NC}"
curl -X PUT $BASE_URL/portfolio/ \
     -H "Authorization: Token $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "John Doe",
           "age": 22,
           "roll_number": "CS2021001",
           "branch": "Computer Science",
           "skills": [
             {"name": "Python"},
             {"name": "JavaScript"},
             {"name": "Django"}
           ]
         }' | python -m json.tool

echo -e "\n${GREEN}4. Getting portfolio...${NC}"
curl -X GET $BASE_URL/portfolio/ \
     -H "Authorization: Token $TOKEN" | python -m json.tool

echo -e "\n${GREEN}5. Processing prompt...${NC}"
curl -X POST $BASE_URL/process-prompt/ \
     -H "Authorization: Token $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "What are my skills?"
         }' | python -m json.tool
