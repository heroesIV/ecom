import json

from .models import *

def cookieCart(request):
	try:
		cart 			= json.loads(request.COOKIES['cart'])
	except:
		cart = {}

	print('Cart: ', cart)
	items 			= []
	order 			= {'get_cart_total':0, 'get_cart_items':0}
	cartItems 		= order['get_cart_items']

	for i in cart:
		try:
			cartItems += cart[i]['quantity']

			product 	= Product.objects.get(id=i)
			total 		= (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':product.id,
				'product':{
					'id':product.id,
					'name':product.name,
					# 'description':product.description,
					'price':product.price,
				    'imageURL':product.imageURL
					},
				'quantity':cart[i]['quantity'],
				# 'digital':product.digital,
				'get_total':total,
				}

			items.append(item)
		except:
			pass

	return {
		'items' 	: items,
		'order'		: order,
		'cartItems' : cartItems,
	}

def cartData(request):
	if request.user.is_authenticated:
		customer 		= request.user.customer
		order, created 	= Order.objects.get_or_create(customer=customer, complete=False)
		items 			= order.orderitem_set.all()
		cartItems 		= order.get_cart_items
	else:
		cookieData 		= cookieCart(request)
		items 			= cookieData['items']
		order 			= cookieData['order']
		cartItems 		= cookieData['cartItems']

	return {
		'items' 	: items,
		'order'		: order,
		'cartItems' : cartItems,
	}

def guestOrder(request, data):
	name = data['form']['name']
	phone = data['form']['phone']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			phone=phone,
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
		)
		product.stock = product.stock - item['quantity']
		if product.stock == 0:
			product.availability = False
		product.save()
	return customer, order