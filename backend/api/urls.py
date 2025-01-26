from django.urls import path
from api import views  # Import from api instead of .

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('process-prompt/', views.process_prompt, name='process-prompt'),
]
