from django.urls import path
from .views import *

urlpatterns = [
    path('customers/', Customers.as_view()),
    path('customers/<int:id>/', Customers.as_view()),
    path('products/', Products.as_view()),
    path('orders/', Orders.as_view()),
    path('orders/<int:id>/', Orders.as_view())
]