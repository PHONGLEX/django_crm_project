from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect("accounts:dashboard")
		return view_func(request, *args, **kwargs)
	return wrapper


def allow_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
				
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			return HttpResponse("You're not authorized to view this page")
		return wrapper
	return decorator


def admin_only(view_func):
	def wrapper(request, *args, **kwargs):
		group = None
		if request.user.is_authenticated:
			group = request.user.groups.all()[0].name

		if group == "customer":
			return redirect("accounts:user-info")

		return view_func(request, *args, **kwargs)
	return wrapper