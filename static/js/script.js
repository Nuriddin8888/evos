
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".add-to-cart-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            const productId = this.dataset.id;

            fetch(`/cart/add/${productId}/`)
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // Tugmadagi count ni yangilash
                        const btn = document.querySelector(`button[data-id="${data.product_id}"]`);
                        if (btn) {
                            btn.innerHTML = `Savatga qo‘shish (${data.quantity})`;
                        }

                        const cartCountEl = document.getElementById("cart-count");
                        if (cartCountEl) {
                            cartCountEl.textContent = data.cart_total_items;
                        }
                    }
                });
        });
    });
    document.getElementById("order-btn").addEventListener("click", function () {
        fetch('/cart/fragment/')
            .then(response => response.json())
            .then(data => {
                document.getElementById("cart-modal-content").innerHTML = data.html;
                document.getElementById("cart-modal").style.display = "block";
            });
    });
    window.addEventListener("click", function (event) {
        const modal = document.getElementById("cart-modal");
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });

    const categoryButtons = document.querySelectorAll('.category-btn');
    const menuItems = document.querySelectorAll('.menu-item');

    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            const selectedCategory = button.dataset.category;

            // Aktiv tugmani belgilash
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Mahsulotlarni filterlash
            menuItems.forEach(item => {
                const itemCategory = item.dataset.category;
                if (itemCategory === selectedCategory || selectedCategory === 'all') {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});
