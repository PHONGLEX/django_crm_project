from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICE = (
	('Pending', 'Pending'),
	('Out for delivery', 'Out for delivery'),
	('Delivered', 'Delivered')
)

CATEGORY_CHOICE = (
	('Indoor', 'Indoor'),
	('Out Door', 'Out Door'),
)


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	phone = models.CharField(max_length=50)
	email = models.EmailField()
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	avatar = models.ImageField(upload_to="images/",null=True, blank=True)

	class Meta:
		verbose_name = "Customer"
		verbose_name_plural = "Customers"

	def __str__(self):
		return self.user.username


class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	category = models.CharField(max_length=10, choices=CATEGORY_CHOICE)
	description = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField("Tag")

	class Meta:
		verbose_name = "Product"
		verbose_name_plural = "Products"

	def __str__(self):
		return self.name


class Order(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=30, choices=STATUS_CHOICE)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	note = models.TextField()

	class Meta:
		verbose_name = "Order"
		verbose_name_plural = "Orders"

	def __str__(self):
		return f"Order of {self.customer.name}"
	

class Tag(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name
	