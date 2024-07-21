from django.test import TestCase
from django.utils import timezone
from shop.models import Product, Category
from cart.models import Cart, CartItem
from django.urls import reverse
from django.test import Client
from accounts.models import CustomUser
import stripe


class CartModelsTest(TestCase):
    def setUp(self):
        self.c = Category.objects.create(name='test category')
        self.product = Product.objects.create(
            name='Test Product',
            price=10.0,
            stock = 900,
            category=self.c
        )
        self.cart = Cart.objects.create(cart_id='test_cart', date_added=timezone.now())
        self.cart_item = CartItem.objects.create(
            product=self.product,
            cart=self.cart,
            quantity=2,
            active=True
        )

    def test_cart_str_method(self):
        self.assertEqual(str(self.cart), 'test_cart')

    def test_cart_item_sub_total_method(self):
        expected_sub_total = self.product.price * self.cart_item.quantity
        self.assertEqual(self.cart_item.sub_total(), expected_sub_total)

    def test_cart_item_str_method(self):
        expected_str = str(self.product)
        self.assertEqual(str(self.cart_item.product.name), expected_str)

class CartViewTests(TestCase):
    def setUp(self):
        self.c = Category.objects.create(name='test category')
        self.product = Product.objects.create(name='Test Product',
            price=10.0,
            stock=2,
            category=self.c,
        )

    def test_add_cart(self):
        response = self.client.get(reverse('cart:add_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  
        cart = Cart.objects.get(cart_id=self.client.session.session_key)
        cart_item = CartItem.objects.get(product=self.product, cart=cart)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_cart_quantity_limit(self):
        response = self.client.get(reverse('cart:add_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  
        cart = Cart.objects.get(cart_id=self.client.session.session_key)
        cart_item = CartItem.objects.get(product=self.product, cart=cart)
        self.assertEqual(cart_item.quantity, 1)
        # Attempt to add more items than stock
        response = self.client.get(reverse('cart:add_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        cart_item.refresh_from_db()  # Refresh the cart_item instance
        self.assertEqual(cart_item.quantity, self.product.stock) 

class CartRemoveViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', description='Test description')

        # Create a product for testing 
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            category=self.category,
            price=19.99,
            stock=10
        )

    def _cart_id(self, request):
        # Your implementation of the cart ID generation function using the request
        # This can be replaced with your actual implementation
        return request.session.session_key

    def test_cart_remove_view(self):
        # Set up a request with a session
        request = self.client.request().wsgi_request
        request.session = self.client.session
        request.session.save()

        # Set the cart ID using the _cart_id function
        request.session['cart_id'] = self._cart_id(request)

        # Create a cart using the _cart_id function
        cart = Cart.objects.create(cart_id=request.session['cart_id'])
        cart_item = CartItem.objects.create(product=self.product, quantity=2, cart=cart)

        # Make a request to the cart_remove view
        response = self.client.post(reverse('cart:cart_remove', args=[self.product.id]))

        # Assert that the response has a status code of 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Assert that the cart_item quantity is reduced by 1
        updated_cart_item = CartItem.objects.get(id=cart_item.id)
        self.assertEqual(updated_cart_item.quantity, 1)

    def test_cart_full_remove_view(self):
        # Set up a request with a session
        request = self.client.request().wsgi_request
        request.session = self.client.session
        request.session.save()

        # Set the cart ID using the _cart_id function
        request.session['cart_id'] = self._cart_id(request)

        # Create a cart using the _cart_id function
        cart = Cart.objects.create(cart_id=request.session['cart_id'])
        cart_item = CartItem.objects.create(product=self.product, quantity=1, cart=cart)

        # Make a request to the cart_remove view for the last item
        response = self.client.post(reverse('cart:full_remove', args=[self.product.id]))

        # Assert that the response has a status code of 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Assert that the cart_item is deleted
        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(id=cart_item.id)

class CartDetailViewTest(TestCase):
    def setUp(self):
        # Create a client
        self.client = Client()
        self.category = Category.objects.create(name='Test Category', description='Test description')

        # Create a product for testing with a UUID and associate it with the category
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            category=self.category,
            price=19.99,
            stock=10
        )
        # Create a user for the session
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Add Stripe testing keys to your settings if not already present
        stripe.api_key = 'sk_test_51Pc6bqEFX5HYk4H3dxzR83yZlyw4jXVfvDOtUCOfW5jpEW6HFyGoeEIL3OG2TrkXMAmaouDgNqYd0cIVOIjX9wmJ00ayBvu5bt'

    def _cart_id(self, request):
        # Your implementation of the cart ID generation function using the request
        # This can be replaced with your actual implementation
        return request.session.session_key

    def test_cart_detail_view(self):
        # Set up a request with a session
        request = self.client.request().wsgi_request
        request.session = self.client.session
        request.session.save()

        # Set the cart ID using the _cart_id function
        request.session['cart_id'] = self._cart_id(request)

        # Create a cart using the _cart_id function
        cart = Cart.objects.create(cart_id=request.session['cart_id'])
        cart_item = CartItem.objects.create(product=self.product, quantity=2, cart=cart)

        # Mock the Stripe API calls using the stripe.testing library
        with self.settings(STRIPE_SECRET_KEY='sk_test_51Pc6bqEFX5HYk4H3dxzR83yZlyw4jXVfvDOtUCOfW5jpEW6HFyGoeEIL3OG2TrkXMAmaouDgNqYd0cIVOIjX9wmJ00ayBvu5bt', STRIPE_PUBLISHABLE_KEY='pk_test_51Pc6bqEFX5HYk4H3AUJu4jpzpMY4XsYSDYEFscDWaqpwTqe8hsw4oN9JkEqOqsU0k7ElbqWWfmEQMr5OcsLRxxVM006i4nNDFH'):
            with self.assertLogs('stripe', level='INFO') as stripe_logs:
                response = self.client.post(reverse('cart:cart_detail'), {
                    'stripeToken': 'tok_visa',
                    'stripeEmail': 'test@example.com',
                    'stripeBillingName': 'Test User',
                    'stripeBillingAddressLine1': '123 Main St',
                    'stripeBillingAddressCity': 'City',
                    'stripeBillingAddressCountryCode': 'US',
                    'stripeShippingName': 'Test User',
                    'stripeShippingAddressLine1': '123 Main St',
                    'stripeShippingAddressCity': 'City',
                    'stripeShippingAddressCountryCode': 'US',
                })

        # Assert that the response has a status code of 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Assert that the expected Stripe logs are present in the logs
        self.assertIn('Request to Stripe api', stripe_logs.output[0])
        self.assertIn('method=post path=https://api.stripe.com/v1/', stripe_logs.output[0])
        # Print the content of the logs for debugging
        print('\n'.join(stripe_logs.output))
