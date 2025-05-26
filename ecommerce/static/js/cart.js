

var updateBtn = document.getElementsByClassName('update-cart')

console.log(updateBtn.length)

for (i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function () {
        
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        console.log('User', user)
        if (user == 'AnonymousUser') {
            console.log("User is not authenticated.")
        }
        else {
            updateUser(productId , action)
        }
    })
}

function updateUser(productId , action) {

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