from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models.query import QuerySet

from django.views.generic import ListView
from .models import Product
from django.db.models import Q

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

class ContactPageView(TemplateView):
    template_name = 'contact.html'


def prod_list(request, category_id=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, available=True)
    
    paginator = Paginator(products, 6)
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {'category': category, 'prods': products})

def product_detail(request, category_id, product_id):
    product = get_object_or_404(Product, category_id=category_id, id=product_id)
    return render(request, 'product.html', {'product': product})

class SearchProductsListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    def get_context_data(self, **kwargs):
        context = super(SearchProductsListView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context