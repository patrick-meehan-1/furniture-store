from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    # path('', HomePageView.as_view(), name='home'),
    path('', views.prod_list, name='all_products'),
    path('<uuid:category_id>/', views.prod_list, name='products_by_category'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('<uuid:category_id>/<uuid:product_id>/<slug:slug>', views.product_detail, name = 'product_detail'),
    path('search/', SearchProductsListView.as_view(), name='searchResult'),
    path('adv_search/', views.filterview, name='filter_search'),
    path('new/', ProductCreateView.as_view(), name='product_create'),

]