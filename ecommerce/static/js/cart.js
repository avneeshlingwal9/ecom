


var updateBtn = document.getElementsByClassName('update-cart')

console.log(updateBtn.length)

for (i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function () {
        
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        console.log('User', user)
        if (user == 'AnonymousUser') {
            addCookieItem(productId , action); 
        }
        else {
            updateUserOrder(productId , action)
        }
    })
}

function updateUserOrder(productId , action) {

    const url = '/update_items/'
    var data = {
        'productId': productId,
        'action': action
    }
    var fetchData = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers({ 'Content-Type': 'application/json', 'X-CSRFToken' : csrftoken})
        

    }
    fetch(url, fetchData)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            location.reload()
            console.log('DATA:', data)
        }
        );

}


function addCookieItem(productId, action){

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
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload()
}