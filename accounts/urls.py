from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('add-money/', views.AddMoneyView.as_view(), name='add_money'),
    path('borrows/', views.BorrowListView.as_view(), name='borrows'),
]
