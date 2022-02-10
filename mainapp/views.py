from django.shortcuts import render
from django.views.generic import ListView, View, DetailView
from .models import Product, Category


class ProductListView(ListView):
    """список товаров"""
    model = Product
    context_object_name = 'products'
    template_name = 'mainapp/product/product_list.html'


class ProductDetailView(DetailView):
    """полное описание товара"""
    model = Product
    slug_field = 'url'
    context_object_name = 'products'
    template_name = 'mainapp/product/product_detail.html'


class ProductCategoryListView(View):
    """фильтрация"""

    def get(self, request, url, *args, **kwargs):
        products = Product.objects.filter(category__url=url)

        context = {
            'products': products,
        }
        return render(request, 'mainapp/product/product_list.html', context)

