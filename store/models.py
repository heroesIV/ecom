from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

	user 			= models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name 			= models.CharField(max_length=120, null=True, blank=True)
	phone 			= models.CharField(max_length=10, null=True, blank=True)
	# device			= models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		if self.name:
			return self.name
		else:
			return str(self.phone)

class Product(models.Model):

	name 			= models.CharField(max_length=200)
	description 	= models.CharField(max_length=200, null=True)
	price 			= models.DecimalField(max_digits=7, decimal_places=2)
	availability 	= models.BooleanField(default=True)
	image			= models.ImageField(default='/images/comingsoon.jpg',null=True, blank=True)

	def __str__(self):
		return self.name

	# @property
	# def imageURL(self):
	# 	try:
	# 		url 	= self.image.url
	# 	except:
	# 		url 	= '/images/comingsoon.jpg'

	# 	return url

class Order(models.Model):

	STATUS 			= (
		('Pending', 'Pending'),
		('Ready', 'Ready'),
		('Delivered', 'Delivered'),
	)

	customer 		= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	date_ordered 	= models.DateTimeField(auto_now_add=True)
	status 			= models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
	paid 			= models.BooleanField(default=False, null=True)
	complete 		= models.BooleanField(default=False)
	transaction_id 	= models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.customer)

	@property
	def get_cart_total(self):
		orderitems 	= self.orderitem_set.all()
		total 		= sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems 	= self.orderitem_set.all()
		total 		= sum([item.quantity for item in orderitems])
		return total

class OrderItem(models.Model):

	product 		= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order 			= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity 		= models.IntegerField(default=0, null=True, blank=True)

	@property
	def get_total(self):
		total 		= self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):

	customer 		= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order 			= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	flat 			= models.CharField(max_length=10, null=False)
	apartment 		= models.CharField(max_length=100, null=False)
	# street_area		= models.CharField(max_length=200, null=False)

	def __str__(self):
		return self.flat