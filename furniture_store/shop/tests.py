from django.test import TestCase
from django.urls import reverse
from .models import Category, Product

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Outdoor Cushions',
            description='Outdoor cushions for your summer living space'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Outdoor Cushions')
        self.assertEqual(self.category.description, 'Outdoor cushions for your summer living space')

    def test_category_str_method(self):
        self.assertEqual(str(self.category), 'Outdoor Cushions')

    def test_category_get_absolute_url(self):
        expected_url = reverse('products_by_category', args=[str(self.category.id)])
        self.assertEqual(self.category.get_absolute_url(), expected_url)

class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Clothing',
            description='Fabulous clothing items'
        )

        self.product = Product.objects.create(
            name='Blouse',
            description='Silk long sleeve blouse',
            category=self.category,
            price=99.99,
            stock=20,
            available=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Blouse')
        self.assertEqual(self.product.description, 'Silk long sleeve blouse')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.price, 99.99)
        self.assertEqual(self.product.stock, 20)
        self.assertTrue(self.product.available)

    def test_product_str_method(self):
        self.assertEqual(str(self.product), 'Blouse')

    def test_product_get_absolute_url(self):
        expected_url = reverse('product_detail', args=[str(self.category.id), str(self.product.id)])
        self.assertEqual(self.product.get_absolute_url(), expected_url) 

class ShopViewsTest(TestCase):
    def setUp(self):
        # Create some test data (categories and products) for your views
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            description='Test Description',
            price=10.99,
            stock=45,
            available=True,
        )

    def test_prod_list_view(self):
        response = self.client.get(reverse('all_products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
        self.assertTemplateUsed(response, 'category.html')

    def test_prod_list_view_with_category(self):
        response = self.client.get(reverse('products_by_category', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
        self.assertTemplateUsed(response, 'category.html')

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.category.id, self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'product.html')

class ShopUrlsTestCase(TestCase):

    def setUp(self):
        # Create sample data for testing
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price='50.00',stock='4',category=self.category)

    def test_all_products_url(self):
        url = reverse('all_products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_url(self):
        url = reverse('products_by_category', args=[str(self.category.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        url = reverse('product_detail', args=[str(self.category.id), str(self.product.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
