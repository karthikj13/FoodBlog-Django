from django.urls import path

from . import views

urlpatterns = [

    path('',views.food_list, name="food_list"),
    path('detail/<str:slug>/',views.food_detail, name="food_detail"),
    
    path('share/<str:food_id>/',views.food_share, name="food_share"),
]
