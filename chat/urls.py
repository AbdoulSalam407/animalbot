from django.urls import path
from .views import ChatImageView

urlpatterns = [
    path("chat-image/", ChatImageView.as_view()),
    
]
