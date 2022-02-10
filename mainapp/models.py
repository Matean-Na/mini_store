

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """категории товаров"""
    name = models.CharField('название', max_length=50)
    url = models.SlugField(max_length=100, unique=True, verbose_name="url", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"


class Product(models.Model):
    """товар"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField('название', max_length=110)
    descriptions = models.TextField('описание')
    image = models.ImageField(upload_to='image/product_image/', verbose_name='изображение')
    numbers = models.PositiveSmallIntegerField('количество', default=0)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    url = models.SlugField(max_length=100, unique=True, verbose_name="url")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"
