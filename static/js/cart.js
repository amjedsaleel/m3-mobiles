function IncrementCartItem(e, id, url) {
    e.preventDefault()
    console.log()
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
            document.getElementById("quantity-" + id).value = quantity;
            document.getElementById("sub_total-" + id).innerHTML = "₹" + sub_total;
            document.getElementById("total-price").innerHTML = "₹" + total;
            document.getElementById("total-price").innerHTML = "₹" + total;
            document.getElementById("tax").innerHTML = "₹" + tax;
            document.getElementById("grand-total").innerHTML = "₹" + grand_total;
        }
    })
}