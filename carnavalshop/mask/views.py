from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h1>Главная</h1>
        <li><a href="/about/">Об авторе</a></li>
        <li><a href="/shop/">О магазине</a></li>
    """)
def about(request):
     return HttpResponse("Автор Носко яна 87тп")
def shop_info(request):
    return HttpResponse(""""
        Магазин масок и костюмов
        “Создание и базовая настройка приложений Django”
    """)