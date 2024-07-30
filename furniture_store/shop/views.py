from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models.query import QuerySet
from django.views.generic.edit import *
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic import ListView
from .models import Product, Category
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

def product_detail(request, category_id, product_id, slug):
    product = get_object_or_404(Product, category_id=category_id, id=product_id, slug=slug)
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
    
# Advanced Search

def filterview(request):
    categories = Category.objects.all()
    qs = Product.objects.all()

    title_contains_query = request.GET.get('title_contains')

    id_exact_query = request.GET.get('id_exact')

    name_or_description_query = request.GET.get('name_or_description')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    category = request.GET.get('category')

    reviewed = request.GET.get('reviewed')
    notReviewed = request.GET.get('notReviewed')


    if title_contains_query != '' and title_contains_query is not None:
        qs = qs.filter(name__icontains=title_contains_query)
    elif id_exact_query != '' and id_exact_query is not None:
        qs = qs.filter(id=id_exact_query)
    elif name_or_description_query != '' and name_or_description_query is not None:
        qs = qs.filter(Q(name__icontains=name_or_description_query)
                       | Q(description__icontains=name_or_description_query)
                       ).distinct()
    
    if min_price != '' and min_price is not None:
        qs = qs.filter(price__gte=min_price)

    if max_price != '' and max_price is not None:
        qs = qs.filter(price__lt=max_price)

    if date_min != '' and date_min is not None:
        qs = qs.filter(created__gte=date_min)

    if date_max != '' and date_max is not None:
        qs = qs.filter(created__lt=date_max)

    if category != '' and category is not None and category != 'Choose...':
        qs = qs.filter(category__name=category)

    # not working yet, need to implement review system first
    if reviewed == 'on':
        qs = qs.filter(reviewed=True)
    elif notReviewed == 'on':
        qs = qs.filter(reviewed=False) 


    context = {
        'queryset':qs,
        'categories': categories
        }
    return render(request, 'adv_search.html', context)

# Add a new Product
class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'products.add_product'
    model = Product
    fields = ('name', 'description', 'category', 'price', 'image', 'stock', 'available')
    template_name = 'product_new.html'