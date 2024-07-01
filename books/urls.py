from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookView.as_view(), name='books'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book'),
    path('borrow/<int:id>/', views.BorrowBookView.as_view(), name='borrow'),
    path('return/<int:id>/', views.ReturnBorrowView.as_view(), name='return'),
]
