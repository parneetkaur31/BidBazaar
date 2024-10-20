from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'buy/', views.buy, name="buy" ),
    path(r'sell/', views.sell, name="sell" ),
    path(r'contact/', views.contact, name="contact" ),
    # path(r'signin/', views.sign, name="login"),
    path('bid/<int:list_id>', views.new_bid, name="new_bid"),
    path(r'logout/', views.signout, name="signout"),
    path(r'registered/', views.reg_form, name="reg_form"),
    path(r'register/', views.register, name="register"),
    path(r'productListed/', views.sell_form, name="sell_form"),
    path(r'login/', views.log_form, name="log_form")
]