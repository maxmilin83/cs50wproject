from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('generatecoins',views.generatecoins,name="generatecoins"),
    path('coin/<str:coin>',views.viewcoin,name="viewcoin"),
    path('funds',views.viewfunds,name="funds"),
    path('addfunds',views.addfunds,name="addfunds"),
     path('withdrawfunds',views.withdrawfunds,name="withdrawfunds"),

]