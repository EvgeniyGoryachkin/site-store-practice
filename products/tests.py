from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class indexviewtestcase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        print(response)

class productslistviewtestcase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()
    def test_list(self):
        response = self.client.get(reverse('products:index'))
        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:2]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)
        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )
    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        context_data = response.context_data
        self.assertEqual(context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')

# Create your tests here.
