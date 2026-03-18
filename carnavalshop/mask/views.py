from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Category, Cart, CartItem

# --- ИНФОРМАЦИОННЫЕ СТРАНИЦЫ ---
def home(request):
    return HttpResponse("""
        <h1>Главная</h1>
        <li><a href="/about/">Об авторе</a></li>
        <li><a href="/shop/">О магазине</a></li>
        <li><a href="/catalog/">В каталог</a></li>
    """)

def about(request):
    return HttpResponse("Автор Носко Яна 87тп")

def shop_info(request):
    return HttpResponse("Магазин масок и костюмов")

# --- КАТАЛОГ ---
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    if query:
        # Исправлено: добавлено __icontains (два подчеркивания)
        products = products.filter(Q(nameicontains=query) | Q(descriptionicontains=query))
    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'shop/product_list.html', {'products': products, 'categories': categories})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# --- КОРЗИНА (CRUD: Read, Create, Update, Delete) ---
@login_required
def cart_view(request):
    items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'shop/cart.html', {'items': items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('mask:cart_view')

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        item.quantity = int(request.POST.get('quantity', 1))
        item.save()
    return redirect('mask:cart_view')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('mask:cart_view')

# --- ОФОРМЛЕНИЕ ЗАКАЗА (CHECKOUT) ---
@login_required
def checkout(request):
    # 1. Берем товары
    cart_items = CartItem.objects.filter(cart__user=request.user)
    
    if request.method == 'POST':
        # Считаем итог
        total = sum(i.product.price * i.quantity for i in cart_items)
        
        # Формируем текст чека
        receipt = f"\n{'='*30}\nЧЕК ЗАКАЗА\nПользователь: {request.user.username}\nИтого: {total} руб.\n{'='*30}\n"

        # ПРИНУДИТЕЛЬНАЯ ПЕЧАТЬ (это точно появится в терминале)
        print(receipt)

        # ПОПЫТКА ОТПРАВКИ EMAIL (появится, если backend настроен верно)
        try:
            send_mail(
                'Чек CarnavalShop', 
                receipt, 
                settings.EMAIL_HOST_USER, 
                [request.user.email],
                fail_silently=False, # Если будет ошибка - вы её увидите в браузере
            )
        except Exception as e:
            print(f"ОШИБКА ПОЧТЫ: {e}")

        # Очищаем корзину
        cart_items.delete()
        
        return render(request, 'shop/checkout_success.html', {'total': total})
    
    return render(request, 'shop/checkout.html')