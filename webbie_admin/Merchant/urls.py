from django.urls import  path
from . import views

urlpatterns = [
    
    path('markup/', views.markup_list, name='markup'),
    path('markup/add_markup', views.add_markup, name='add_markup'),
    path('markup/update/<int:id>', views.update_markup, name='update_markup'),
    path('discount/', views.discount_list, name='discount'),
    path('discount/add_discount', views.add_discount, name='add_discount'),
    path('discount/update/<int:id>', views.update_discount, name='update_discount'),
    path('transactions/',views.transaction_list,name='transactions'),
    path('transaction/update/<int:id>', views.update_transaction, name='update_transaction'),
    path('autocomplete/user/', views.autocomplete_user, name='autocomplete_user'),
    path('autocomplete/product-category/', views.autocomplete_product_category, name='autocomplete_product_category'),
    path('autocomplete/currency/', views.autocomplete_currency, name='autocomplete_currency'),
    path('autocomplete/product/', views.autocomplete_product, name='autocomplete_product'),
    path('autocomplete/markup/', views.autocomplete_markup, name='autocomplete_markup'),
    path('autocomplete/discount/', views.autocomplete_discount, name='autocomplete_discount'),
        
]
