from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit_profile/<uuid:pk>/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/<uuid:pk>/', ProfilePageView.as_view(), name='show_profile'),
]
