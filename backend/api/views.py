from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserPortfolioSerializer
from .models import UserPortfolio

import sys
import os
from django.conf import settings

# Better way to handle the NLP import
try:
    sys.path.append(os.path.join(settings.BASE_DIR, '..'))
    from NlP.nlp import main
except ImportError as e:
    print(f"Error importing NLP module: {e}")
    # Fallback function in case import fails
    def main(portfolio, prompt):
        return "NLP module not available"

@api_view(['POST'])
def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'},
                          status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            })
        return Response({'error': 'Invalid credentials'},
                       status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def portfolio(request):
    try:
        portfolio = UserPortfolio.objects.get(user=request.user)
    except UserPortfolio.DoesNotExist:
        if request.method == 'GET':
            return Response({'error': 'Portfolio not found'},
                          status=status.HTTP_404_NOT_FOUND)
        portfolio = None

    if request.method == 'GET':
        serializer = UserPortfolioSerializer(portfolio)
        return Response(serializer.data)

    elif request.method == 'PUT':
        try:
            if portfolio is None:
                serializer = UserPortfolioSerializer(data=request.data,
                                                   context={'request': request})
            else:
                serializer = UserPortfolioSerializer(portfolio,
                                                   data=request.data,
                                                   context={'request': request},
                                                   partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_prompt(request):
    try:
        prompt = request.data.get('prompt')
        if not prompt:
            return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            portfolio = UserPortfolio.objects.get(user=request.user)
            # Convert portfolio data to string format
            portfolio_data = {
                'username': portfolio.username,
                'year': portfolio.year,
                'branch': portfolio.branch,
                'skills': [skill.name for skill in portfolio.skills.all()]
            }
            # Convert to string or format as needed
            portfolio_string = str(portfolio_data)

            response = main(prompt, portfolio_string)  # Pass the string version
            return Response({'response': response})
        except UserPortfolio.DoesNotExist:
            return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
