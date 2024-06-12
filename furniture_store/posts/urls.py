from django.urls import path
from .views import PostPageView, PostDetailView

urlpatterns = [
    path('', PostPageView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
