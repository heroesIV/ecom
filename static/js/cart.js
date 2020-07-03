var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++){
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		var price = this.dataset.price
		console.log('productId: ', productId, 'Action: ', action, 'Price: ', price)
		updateCartItems(productId, action, price)
		// console.log(location.pathname)
		console.log('USER: ', user)
		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}
		else {
			updateUserOrder(productId, action)
		}
	})
}

async function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		await fetch(url, {
			method:'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken' : csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			console.log('Data: ', data)
			// location.reload()
		});
}

async function updateCartItems(productId, action, price){
	let total = document.getElementById('cart-total')
	let cartSubtotalItems = document.getElementById('cart-subtotal-items')
	let cartSubtotal = document.getElementById('cart-subtotal')
	let prodQuan = document.querySelectorAll('#prod-quantity')

	if (action == 'delete'){
		location.reload()
	}
	prodQuan.forEach(item => {
		if (productId == item.attributes.value.textContent) {
			if (action == 'add'){
				console.log(parseInt(item.textContent)+1)
				item.textContent = parseInt(item.textContent)+1
				// prodQuan.textContent = parseInt(prodQuan.textContent)+1
			}
			if (action == 'remove'){
				console.log(parseInt(item.textContent)-1)
				item.textContent = parseInt(item.textContent)-1
				if (item.textContent==0){
					location.reload()
				}
			}
		}
	})
	// console.log(prodQuan[0])
	// total.textContent =
	console.log(productId)

	if (action == 'add'){
		// console.log(parseInt(total.textContent)+1)
		total.textContent = parseInt(total.textContent)+1
		if (cartSubtotal != null || cartSubtotal != undefined){
			cartSubtotal.textContent = parseFloat(cartSubtotal.textContent)+parseFloat(price)
		}
		if (cartSubtotalItems != null || cartSubtotalItems != undefined){
			cartSubtotalItems.textContent = parseInt(cartSubtotalItems.textContent)+1
		}
		// prodQuan.textContent = parseInt(prodQuan.textContent)+1
	}
	if (action == 'remove'){
		// console.log(parseInt(total.textContent)-1)
		total.textContent = parseInt(total.textContent)-1
		if (cartSubtotalItems != null || cartSubtotalItems != undefined){
			cartSubtotalItems.textContent = parseInt(cartSubtotalItems.textContent)-1
		}
		if (cartSubtotal != null || cartSubtotal != undefined){
			cartSubtotal.textContent = parseFloat(cartSubtotal.textContent)-parseFloat(price)
		}
	}
}

async function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}

	if (action == 'delete') {
		console.log('Item should be deleted')
			delete cart[productId];
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

	// location.reload()
}