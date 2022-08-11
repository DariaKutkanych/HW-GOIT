from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('transaction/', views.transaction, name='transaction'),
    path('expense/', views.expense, name='expense'),
    path('income/', views.income, name='income'),
    path('period/', views.period, name='period'),
    path('delete/<int:entry_id>', views.delete_entry, name='delete_entry'),
    path('result/<str:start>/<str:end>', views.result, name='result'),
]