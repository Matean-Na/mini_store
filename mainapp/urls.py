from django.urls import path, include
from .views import ProductListView, ProductCategoryListView, ProductDetailView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path('<slug:url>/', ProductCategoryListView.as_view(), name='product_category_list'),
    path('account/', include("account.urls")),
]
