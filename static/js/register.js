
document.addEventListener('DOMContentLoaded', function () {
    const phoneInput = document.getElementById('phone');
    phoneInput.addEventListener('input', function (e) {
        let x = e.target.value.replace(/\D/g, '').match(/(\d{0, 3})(\d{0, 2})(\d{0, 3})(\d{0, 2})(\d{0, 2})/);
        e.target.value = !x[2] ? '+998' + x[1] : '+998 ' + x[1] + ' ' + x[2] + (x[3] ? ' ' + x[3] : '') + (x[4] ? ' ' + x[4] : '');
    });

    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const phone = document.getElementById('phone').value;
        const password = document.getElementById('password').value;

        console.log('Kirish uchun ma\'lumotlar:', { phone, password });

        alert('Muvaffaqiyatli kirildi!');
        window.location.href = 'profile.html';
    });
});
