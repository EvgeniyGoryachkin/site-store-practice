from django.test import TestCase
from django.urls import reverse

from products.models import Product
class indexviewtestcase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        print(response)

class productslistviewtestcase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        products = Product.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data,['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['object_list'], products[:2])
# Create your tests here.
