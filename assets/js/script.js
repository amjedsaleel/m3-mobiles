function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})

const csrftoken = getCookie('csrftoken');

function addToCart(e, id) {
    e.preventDefault()
    $.ajax({
        type: 'POST',
        url: id,
        data: {
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (data) {
            document.getElementById("cart-count").innerHTML =  data.cart_count;
            toast('success', 'product added to cart')
        }
    })
}

function toast(icon, title) {
    Toast.fire({
        icon: icon,
        title: title
    })
}

