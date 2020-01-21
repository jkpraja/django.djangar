from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about-us/',views.about,name='about'),
    path('login/', views.login_user,name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_passwd/', views.change_passwd, name='change_passwd'),
    path('prices/', views.prices, name='prices'),
    path('add_stock.html', views.add_stock, name='add_stock'),
    path('delete/<stock_id>', views.delete_stock, name='delete_stock'),
]
