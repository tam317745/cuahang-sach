from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('support/', views.support, name='support'),
    path('sachthieunhi/', views.sachthieunhi, name='sachthieunhi'),
    path('sachvanhocvn/', views.sachvanhocvn, name='sachvanhocvn'),
    path('sachkinhte/', views.sachkinhte, name='sachkinhte'),
    path('sachnghethuat/', views.sachnghethuat, name='sachnghethuat'),
    path('sachtamlinh/', views.sachtamlinh, name='sachtamlinh'),
    path('sachvanhocncngoai/', views.sachvanhocncngoai, name='sachvanhocncngoai'),
    path('sachgiaoduc/', views.sachgiaoduc, name='sachgiaoduc'),
    path('sachvanhoa/', views.sachvanhoa, name='sachvanhoa'),
    path('sachlichsu/', views.sachlichsu, name='sachlichsu'),
    path('sachyhoc/', views.sachyhoc, name='sachyhoc'),
    path('sachtonghop/', views.sachtonghop, name='sachtonghop'),
    path('search/', views.search, name='search'),
    path('tusach/', views.tusach, name='tusach'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
