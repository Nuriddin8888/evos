from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('', home_page, name='home'),
    path('cart/', get_cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-quantity/<int:item_id>/', update_quantity, name='update_quantity'),

    path('cart/add/<int:product_id>/', add_to_cart_ajax, name='add_to_cart_ajax'),
    path('cart/submit/', submit_order, name="submit_order"),

    path('cart/fragment/', cart_fragment, name='cart_fragment'),


    path('cart/update/<int:item_id>/<str:action>/', update_cart_quantity, name='update_cart_quantity'),
    path('cart/delete/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('cart/partial/', get_cart_partial, name='get_cart_partial'),  

]