
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';

    function compressImage(file, callback, quality = 0.7, maxWidth = 800) {
        const reader = new FileReader();
        reader.onload = function (event) {
            const img = new Image();
            img.onload = function () {
                const canvas = document.createElement('canvas');
                let width = img.width;
                let height = img.height;

                if (width > maxWidth) {
                    height = (maxWidth / width) * height;
                    width = maxWidth;
                }

                canvas.width = width;
                canvas.height = height;

                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);

                canvas.toBlob(function (blob) {
                    callback(blob);
                }, 'image/jpeg', quality);
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    }

    // Modalni ochish
    const openBtn = document.getElementById('btn-outline');
    const modal = document.getElementById('editModal');
    const closeModal = document.querySelector('.close-modal');

    openBtn.onclick = () => modal.classList.add('show');
    closeModal.onclick = () => modal.classList.remove('show');

    // Saqlash (AJAX orqali)
    document.getElementById('editForm').addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);

        const response = await fetch('/users/update-profile/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: formData
        });

        if (response.ok) {
            alert('Ma\'lumotlaringiz saqlandi!');
            modal.classList.remove('show');
            location.reload();  // O'zgartirilgan ma'lumotlarni ko'rsatish uchun
        } else {
            alert('Xatolik yuz berdi.');
        }
    });

}); // 👉 MUHIM: Bu yopuvchi qavs yetishmayotgandi