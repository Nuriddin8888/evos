
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function refreshCart() {
    fetch("/cart/partial/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("cart-wrapper").innerHTML = data.html;
        })
        .catch(error => console.error("Xatolik:", error));
}

document.addEventListener("click", function (e) {
    const target = e.target;

    if (target.closest(".quantity-btn")) {
        const button = target.closest(".quantity-btn");
        const action = button.dataset.action;
        const cartItem = button.closest(".cart-item");
        const itemId = cartItem.dataset.id;

        fetch(`/cart/update/${itemId}/${action}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json",
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    refreshCart();
                }
            })
            .catch(error => console.error("Xatolik:", error));
    }

    if (target.closest(".remove-btn")) {
        const button = target.closest(".remove-btn");
        const cartItem = button.closest(".cart-item");
        const itemId = cartItem.dataset.id;

        fetch(`/cart/delete/${itemId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json",
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    refreshCart();
                }
            })
            .catch(error => console.error("Xatolik:", error));
    }
});

document.addEventListener('click', function (e) {
    if (e.target.classList.contains('checkout-btn') || e.target.closest('.checkout-btn')) {
        e.preventDefault();

        const csrfToken = getCookie('csrftoken');

        fetch('/cart/submit/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    alert("Buyurtma qabul qilindi! Rahmat!");
                    location.reload();
                } else {
                    alert("Xatolik: " + (data.error || "Noma'lum xatolik"));
                }
            })
            .catch(error => {
                console.error('Xatolik:', error);
                alert("Server xatosi: " + error.message);
            });
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

