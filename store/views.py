from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import *
from .forms import *

# Create your views here.


def store(request):

	data = cartData(request)

	cartItems = data['cartItems']
	products 	= Product.objects.filter(availability=True).order_by('?')

	context 	= {
		'products' 	: products,
		'cartItems' : cartItems,
	}

	return render(request, 'store/store.html', context)

def cart(request):

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context 			= {
		'items' 	: items,
		'order'		: order,
		'cartItems' : cartItems,
	}

	return render(request, 'store/cart.html', context)

def checkout(request):

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context 			= {
		'items' 	: items,
		'order'		: order,
		'cartItems' : cartItems,
	}

	return render(request, 'store/checkout.html', context)

def orderPlaced(request, pk):

	amount = pk
	context = {'amount': amount}
	return render(request, 'store/order_placed.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	elif action == 'delete':
		orderItem.quantity = 0
		orderItem.delete()

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id 		= datetime.datetime.now().timestamp()
	data 				= json.loads(request.body)

	if request.user.is_authenticated:
		customer 		= request.user.customer
		order, created 	= Order.objects.get_or_create(customer=customer, complete=False)

	else:
		customer, order = guestOrder(request, data)

	total 			= float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True

	order.save()

	ShippingAddress.objects.create(
		customer=customer,
		order=order,
		flat=data['shipping']['flat'],
		apartment=data['shipping']['apartment'],
		)

	return JsonResponse('Payment Complete', safe=False)

def products(request):

	if request.user.is_authenticated:
		products 	= Product.objects.all()

		context		= {
			'products'	: products,
		}
		return render(request, 'store/products.html', context)

	else:
		return HttpResponse("Nothing to be seen here")

def addProduct(request):

	if request.user.is_authenticated:
		# product = Product.objects.get(id=pk)

		form = ProductForm()
		if request.method == 'POST':
			form = ProductForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				return redirect('/products')

		context = {'form': form}
		return render(request, 'store/product_form.html', context)
	else:
		return HttpResponse("Nothing to be seen here")



def updateProduct(request, pk):

	if request.user.is_authenticated:
		product = Product.objects.get(id=pk)

		form = ProductForm(instance=product)
		if request.method == 'POST':
			form = ProductForm(request.POST, request.FILES, instance=product)
			if form.is_valid():
				form.save()
				return redirect('/products')

		context = {'form': form}
		return render(request, 'store/product_form.html', context)
	else:
		return HttpResponse("Nothing to be seen here")


def deleteProduct(request, pk):

	if request.user.is_authenticated:

		product 	= Product.objects.get(id=pk)

		if request.method == 'POST':
			product.delete()
			return redirect('/products')

		context 	= {
			'item'	: product,
		}

		return render(request, 'store/delete.html', context)

	else:
		return HttpResponse("Nothing to be seen here")


def customers(request):

	customers 	= Customer.objects.all()

	address = []
	for customer in customers:
		address.append(list(customer.shippingaddress_set.values_list('flat','apartment')))

	# print()

	my_list = zip(customers,address)

	context		= {
		'customers'	: customers,
		'my_list' : my_list,
	}
	return render(request, 'store/customers.html', context)

def addCustomer(request):

	if request.user.is_authenticated:

		form		= CustomerForm(request.POST or None)

		if form.is_valid():
			form.save()
			# form 	= ProductForm()
			return redirect('/customers')

		context 	= {
			'form'	: form
		}

		return render(request, 'store/customer_form.html', context)

	else:
		return HttpResponse("Nothing to be seen here")

def updateCustomer(request, pk):

	if request.user.is_authenticated:
		customer 	= Customer.objects.get(id=pk)
		form 		= CustomerForm(request.POST or None, instance=customer)

		if form.is_valid():
			form.save()
			# form 	= ProductForm()
			return redirect('/customers')

		context 	= {
			'form'	: form
		}

		return render(request, 'store/customer_form.html', context)
	else:
		return HttpResponse("Nothing to be seen here")

def deleteCustomer(request, pk):

	if request.user.is_authenticated:
		customer 	= Customer.objects.get(id=pk)

		if request.method == 'POST':
			customer.delete()
			return redirect('/customers')

		context 	= {
			'item'	: customer,
		}

		return render(request, 'store/delete.html', context)
	else:
		return HttpResponse("Nothing to be seen here")

def dashboard(request):

	if request.user.is_authenticated:
		order_status = Order.objects.filter(complete=True)
		orders 		= Order.objects.filter(complete=True).exclude(status='Delivered').order_by('date_ordered')
		# customers 	= Order.customer.objects.all()
		total_orders= order_status.count()
		delivered 	= order_status.filter(status='Delivered').count()
		pending		= order_status.filter(status='Pending').count()
		ready		= order_status.filter(status='Ready').count()

		orderitems=[]
		address=[]
		for order in orders:
			orderitems.append(list(order.orderitem_set.values_list('product__name','quantity')))
			address.append(list(order.shippingaddress_set.values_list('flat','apartment')))

		my_list = zip(orders,orderitems,address)

		context = {
			'orders'		: orders,
			# 'customers'		: customers,
			'total_orders'	: total_orders,
			'delivered'		: delivered,
			'pending'		: pending,
			'ready'			: ready,
			'mylist'		: my_list,
		}

		return render(request, 'store/dashboard.html', context)
	else:
		return HttpResponse("Nothing to be seen here")

def updateOrder(request, pk):

	if request.user.is_authenticated:
		order = Order.objects.get(id=pk)

		form = OrderForm(request.POST or None, instance=order)

		if form.is_valid():
			form.save()
			# form 	= ProductForm()
			return redirect('/dashboard')

		context 	= {
			'form'	: form,
			'order' : order
		}

		return render(request, 'store/order_form.html', context)

	else:
		return HttpResponse("Nothing to be seen here")

def deleteOrder(request, pk):

	if request.user.is_authenticated:
		order 	= Order.objects.get(id=pk)

		if request.method == 'POST':
			order.delete()
			return redirect('/dashboard')

		context 	= {
			'item'	: order,
		}

		return render(request, 'store/delete.html', context)
	else:
		return HttpResponse("Nothing to be seen here")

def deliveredOrders(request):
	if request.user.is_authenticated:
		orders 		= Order.objects.filter(complete=True, status='Delivered').order_by('-date_ordered')

		orderitems=[]
		address=[]
		for order in orders:
			orderitems.append(list(order.orderitem_set.values_list('product__name','quantity')))
			address.append(list(order.shippingaddress_set.values_list('flat','apartment')))

		my_list = zip(orders,orderitems,address)

		context = {
			'mylist'		: my_list,
		}

		return render(request, 'store/delivered_orders.html', context)
	else:
		return HttpResponse("Nothing to be seen here")
