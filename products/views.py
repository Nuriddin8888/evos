from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, get_object_or_404
from .models import Product, Cart, CartItem, Category
from django.http import JsonResponse
from django.template.loader import render_to_string
import json
from bot import ADMIN_CHAT_ID, BOT_TOKEN


# Create your views here.

def home_page(request):
    all_products = Product.objects.all()
    categories = Category.objects.all()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_ordered=False).first()

        product_quantities = {}

        
        cart = Cart.objects.filter(user=request.user, is_ordered=False).first()
        if cart:
            for item in cart.items.all():
                product_quantities[item.product.id] = item.quantity

        context = {
            "all_products": all_products,
            "product_quantities": product_quantities,
            "categories": categories,
            "cart": cart
            }
        
        return render(request, "index.html", context)
    
    context = {
        "all_products": all_products,
        "categories": categories,
    }
    return render(request, "index.html", context)

def get_cart(request):
    return render(request, 'cart.html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user, is_ordered=False)

    item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        item.quantity += 1
        item.save()

    return redirect('products:home')



@login_required
def update_quantity(request, item_id):
    if request.method == "POST":
        action = request.POST.get("action") 
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user, cart__is_ordered=False)

        if action == "plus":
            item.quantity += 1
        elif action == "minus" and item.quantity > 1:
            item.quantity -= 1

        item.save()
        return JsonResponse({"quantity": item.quantity, "total": item.total_price()})

    return JsonResponse({"error": "Not allowed"}, status=400)


def update_cart_quantity(request, item_id, action):
    item = CartItem.objects.get(id=item_id, cart__user=request.user, cart__is_ordered=False)
    
    if action == "plus":
        item.quantity += 1
    elif action == "minus" and item.quantity > 1:
        item.quantity -= 1
    item.save()
    
    return JsonResponse({"success": True})


def delete_cart_item(request, item_id):
    item = CartItem.objects.get(id=item_id, cart__user=request.user, cart__is_ordered=False)
    item.delete()
    return JsonResponse({"success": True})


def get_cart_partial(request):
    cart = Cart.objects.filter(user=request.user, is_ordered=False).first()
    html = render_to_string("cart_partial.html", {"cart": cart}, request=request)
    return JsonResponse({"html": html})

def add_to_cart_ajax(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "not_authenticated"}, status=401)

    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user, is_ordered=False)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
    item.save()

    total_items = sum(i.quantity for i in cart.items.all())

    return JsonResponse({
        "success": True,
        "product_id": product.id,
        "quantity": item.quantity,
        "cart_total_items": total_items
    })



from django.http import JsonResponse
import requests



def submit_order(request):
    if request.method == "POST" and request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_ordered=False).first()

        if not cart or not cart.items.exists():
            return JsonResponse({"error": "Savat bo'sh"}, status=400)

        # 1. Telegramga xabar
        items_text = ""
        for item in cart.items.all():
            items_text += f"{item.product.title} ({item.quantity} x {item.product.price}) = {item.total_price()} so'm\n"

        total = cart.total_price()
        full_text = f"""
🛒 *Yangi buyurtma*:

👤 Foydalanuvchi: {request.user.username}
📍 Manzil: {cart.address}
📞 Telefon: {request.user.phone_number}

{items_text}

💰 Umumiy: {total} so'm

✅ Buyurtma holati: *Yangi*

👇 Tasdiqlang:
"""

        reply_markup = {
            "inline_keyboard": [[
                {
                    "text": "✅ Yetkazib berildi",
                    "callback_data": f"confirm_order_{cart.id}"
                }
            ]]
        }

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": ADMIN_CHAT_ID,
            "text": full_text,
            "parse_mode": "Markdown",
            "reply_markup": json.dumps(reply_markup)
        }

        response = requests.post(url, data=data)

        return JsonResponse({"success": True})
    



@login_required
def cart_fragment(request):
    cart = Cart.objects.filter(user=request.user, is_ordered=False).first()
    html = render_to_string('cart.html', {'cart': cart}, request=request)
    return JsonResponse({'html': html})