from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product

def home(request):
    return HttpResponse("""
        <h1>Главная</h1>
        <li><a href="/about/">Об авторе</a></li>
        <li><a href="/shop/">О магазине</a></li>
    """)

def about(request):
    return HttpResponse("Автор Носко Яна 87тп")

def shop_info(request):
    return HttpResponse("""
        Магазин масок и костюмов
        “Создание и базовая настройка приложений Django”
    """)

def product_list(request):
    
    products = Product.objects.all().order_by('price')
    return render(request, 'mask/product_list.html', {'products': products})

def product_detail(request, pk):
    
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'mask/product_detail.html', {'product': product})