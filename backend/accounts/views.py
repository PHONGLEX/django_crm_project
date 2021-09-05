from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, CreateUserForm, LoginUserForm, CustomerForm
from .filters import OrderFilter	
from .decorators import unauthenticated_user, allow_users, admin_only


@unauthenticated_user
def register(request):
	
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()

			

			messages.success(request, "An account has been created")
			return redirect("accounts:login")

	context = {
		'form': form
	}
	return render(request, "accounts/register.html", context)


@unauthenticated_user
def login(request):
	
	form = LoginUserForm()
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			django_login(request, user)
			return redirect("accounts:dashboard")
		else:
			messages.warning(request, "Credentials is invalid")
			return redirect("accounts:login")
	context = {
		'form': form
	}
	return render(request, "accounts/login.html", context)


def logoutUser(request):
	logout(request)
	return redirect("accounts:login")


@login_required(login_url="accounts:login")
@allow_users(allowed_roles=['customer'])
def account_settings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
			return redirect("accounts:user-settings")

	context = {
		'form': form
	}
	return render(request, "accounts/account_settings.html", context)


@login_required(login_url="accounts:login")
@allow_users(allowed_roles=['customer'])
def userInfo(request):
	orders = request.user.customer.order_set.all()
	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = {
		'orders': orders,
		'total_order': total_order,
		'delivered': delivered,
		'pending': pending,
	}
	return render(request, "accounts/user.html", context)


@login_required(login_url="accounts:login")
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customer = customers.count()
	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = {
		'orders': orders,
		'customers': customers,
		'total_order': total_order,
		'delivered': delivered,
		'pending': pending,
	}
	return render(request, "accounts/dashboard.html", context)


@login_required(login_url="accounts:login")
@allow_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	context = {
		'products': products
	}
	return render(request, "accounts/products.html", context)


@login_required(login_url="accounts:login")
@allow_users(allowed_roles=['admin'])
def customer(request, pk):

	customer = Customer.objects.get(pk=pk)
	orders = customer.order_set.all()
	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {
		'customer': customer,
		'orders': orders,
		'myFilter': myFilter
	}
	return render(request, "accounts/customer.html", context)


@login_required(login_url="accounts:login")
@allow_users(allowed_roles=['admin'])
def createOrder(request, pk):
	customer = Customer.objects.get(pk=pk)
	OrderFormSet = inlineformset_factory(Customer, Order, fields=("product", "status"))
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

	if request.method == "POST":
		formset = OrderFormSet(request.POST, instance=customer)
		import pdb; pdb.set_trace()
		if formset.is_valid():
			formset.save()
			return redirect('accounts:customer', pk=customer.pk)

	context = {
		'formset': formset
	}
	return render(request, "accounts/order_form.html", context)


@login_required(login_url="accounts:login")
@allow_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	order = Order.objects.get(pk=pk)
	form = OrderForm(instance=order)

	if request.method == "POST":
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect("accounts:dashboard")

	context = {
		'form': form
	}
	return render(request, "accounts/order_form.html", context)


@login_required(login_url="accounts:login")
@allow_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(pk=pk)
	if request.method == "POST":
		order.delete()
		return redirect("accounts:dashboard")
	context = {
		"item": order
	}
	return render(request, "accounts/delete.html", context)
