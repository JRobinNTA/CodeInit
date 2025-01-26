from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserPortfolioSerializer
from .models import UserPortfolio

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def portfolio(request):
    try:
        portfolio = UserPortfolio.objects.get(user=request.user)
    except UserPortfolio.DoesNotExist:
        if request.method == 'GET':
            return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)
        portfolio = None

    if request.method == 'GET':
        serializer = UserPortfolioSerializer(portfolio)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if portfolio is None:
            # Create new portfolio
            serializer = UserPortfolioSerializer(data=request.data, context={'request': request})
        else:
            # Update existing portfolio
            serializer = UserPortfolioSerializer(portfolio, data=request.data, context={'request': request}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_prompt(request):
    prompt = request.data.get('prompt')
    if not prompt:
        return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        portfolio = UserPortfolio.objects.get(user=request.user)
        # This is where you'd call your external function
        response = process_portfolio_prompt(portfolio, prompt)
        return Response({'response': response})
    except UserPortfolio.DoesNotExist:
        return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)
