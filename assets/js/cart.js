const cartCount = document.getElementById("cart-count")

function RemoveCartItem(e, id, url) {
    e.preventDefault()
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
            ).then(function () {
                $.ajax({
                    type: 'POST',
                    url: url,
                    dataType: 'json',
                    data: {
                        csrfmiddlewaretoken: csrftoken,
                    },
                    success: function (data) {
                        let tax = data.tax;
                        let total = data.total;
                        let grand_total = data.grand_total;
                        cartCount.innerHTML = data.cart_count;

                        document.getElementById("total-price").innerHTML = "₹" + total;
                        document.getElementById("tax").innerHTML = "₹" + tax;
                        document.getElementById("grand-total").innerHTML = "₹" + grand_total;
                        document.getElementById('item-row-'+id).style.display = 'none';
                    }
                })
            })
        }
    })
}


function IncrementCartItem(e, id, url) {
    e.preventDefault()

    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            console.log(data)
            let quantity = data.quantity;
            let sub_total = data.sub_total;
            let tax = data.tax;
            let total = data.total;
            let grand_total = data.grand_total;
            cartCount.innerHTML = data.cart_count;

            document.getElementById("quantity-" + id).value = quantity;
            document.getElementById("sub_total-" + id).innerHTML = "₹" + sub_total;
            document.getElementById("total-price").innerHTML = "₹" + total;
            document.getElementById("total-price").innerHTML = "₹" + total;
            document.getElementById("tax").innerHTML = "₹" + tax;
            document.getElementById("grand-total").innerHTML = "₹" + grand_total;
        }
    })
}


function DecrementCartItem(e, id, url) {
    e.preventDefault()
    let quantity = document.getElementById("quantity-" + id).value;
    let link = 'delete-cart-item/'+id+'/'
    if (quantity === '1') {
        RemoveCartItem(e, id, link)
        return
    }

    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            let quantity = data.quantity;
            let sub_total = data.sub_total;
            let tax = data.tax;
            let total = data.total;
            let grand_total = data.grand_total;
            cartCount.innerHTML = data.cart_count;

            document.getElementById("quantity-" + id).value = quantity;
            document.getElementById("sub_total-" + id).innerHTML = "₹" + sub_total;
            document.getElementById("total-price").innerHTML = "₹" + total;
            document.getElementById("tax").innerHTML = "₹" + tax;
            document.getElementById("grand-total").innerHTML = "₹" + grand_total;
        }
    })
}
