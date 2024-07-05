from django.urls import path
from .views import *

urlpatterns = [
    path('', PostPageView.as_view(), name='posts'),
    path('post/<uuid:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_new'),
    path('post/<uuid:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<uuid:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),

]
