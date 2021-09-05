from django.urls import path

from . import views

app_name = "accounts"


urlpatterns = [
	path('', views.home, name="dashboard"),
	path('products/', views.products, name="products"),
	path('customer/<int:pk>/', views.customer, name="customer"),
	path('create-order/<int:pk>/', views.createOrder, name="create-order"),
	path('update-order/<int:pk>/', views.updateOrder, name="update-order"),
	path('delete-order/<int:pk>/', views.deleteOrder, name="delete-order"),

	path('login/', views.login, name='login'),
	path('logout/', views.logoutUser, name='logout'),
	path('register/', views.register, name='register'),
	path('user-info/', views.userInfo, name="user-info"),
	path('user-settings/', views.account_settings, name="user-settings"),	
]