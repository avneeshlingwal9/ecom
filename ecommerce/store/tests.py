from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem, Customer
from .forms import LoginForm

class ModelTests(TestCase):
    def setUp(self):
        # Create data for testing models
        self.customer_user = User.objects.create_user(username='testuser', password='password')
        self.customer = Customer.objects.create(user=self.customer_user, name='Test Customer', email='test@test.com')
        self.product = Product.objects.create(name='Test Product', price=10.00, digital=False)
        self.order = Order.objects.create(customer=self.customer, complete=False, transaction_id='12345')
        self.order_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=2)

    def test_product_string_representation(self):
        """Test that the product name is returned as string"""
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_img_url_property(self):
        """Test the imgURL property handles missing images gracefully"""
        # Since we didn't upload an image, it should return empty string (based on your logic in models.py)
        self.assertEqual(self.product.imgURL, '')

    def test_order_total_calculation(self):
        """Test that order_total property calculates correctly based on order items"""
        # Price 10.00 * Quantity 2 = 20.0
        self.assertEqual(self.order.order_total, 20.0)

    def test_order_shipping_logic(self):
        """Test isShipping property returns True for physical products"""
        # Product is digital=False, so shipping should be True
        self.assertTrue(self.order.isShipping) 
        
        # Change product to digital and re-test
        self.product.digital = True
        self.product.save()
        # We need to fetch fresh properties or iterate items again
        self.assertFalse(self.order.isShipping)

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewuser', password='password')
        # Create a product so the store page has content to render
        self.product = Product.objects.create(name='View Product', price=5.50)

    def test_store_view_status(self):
        """Test the main store page loads (GET request)"""
        url = reverse('store') # Corresponds to path('', views.store, name="store")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')
        # Check if product is in the context
        self.assertIn('products', response.context)

    def test_cart_view_status(self):
        """Test the cart page loads"""
        url = reverse('cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')

    def test_checkout_view_redirect_or_render(self):
        """Test checkout page loads"""
        url = reverse('checkout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/checkout.html')

class FormTests(TestCase):
    def test_login_form_valid(self):
        """Test LoginForm validation with correct data"""
        form_data = {'username': 'testuser', 'password': 'password123'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        """Test LoginForm validation fails with missing data"""
        form_data = {'username': '', 'password': 'password123'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())