from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('generatetrending', views.generatetrending, name="generatetrending"),
    path('viewtrending', views.viewtrending, name="viewtrending"),
    path('orders', views.orders, name="orders"),

    path('generatecoins',views.generatecoins,name="generatecoins"),
    path('generatechart/<str:coin>/<str:days>',views.generatechart,name="generatechart"),
    path('coin/<str:coin>',views.viewcoin,name="viewcoin"),
    path('funds',views.viewfunds,name="funds"),
    path('addfunds',views.addfunds,name="addfunds"),
    path('withdrawfunds',views.withdrawfunds,name="withdrawfunds"),

]