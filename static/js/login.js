
document.addEventListener('DOMContentLoaded', function () {
    // Telefon raqam formati
    const phoneInput = document.getElementById('phone');
    phoneInput.addEventListener('input', function (e) {
        let x = e.target.value.replace(/\D/g, '').match(/(\d{0, 3})(\d{0, 2})(\d{0, 3})(\d{0, 2})(\d{0, 2})/);
        e.target.value = !x[2] ? '+998' + x[1] : '+998 ' + x[1] + ' ' + x[2] + (x[3] ? ' ' + x[3] : '') + (x[4] ? ' ' + x[4] : '');
    });

    const recoveryForm = document.getElementById('recoveryForm');
    recoveryForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const phone = document.getElementById('phone').value;

        console.log('Parolni tiklash uchun telefon raqam:', phone);

        alert('Tasdiqlash kodi telefon raqamingizga yuborildi!');
        window.location.href = 'reset-password.html';
    });
});
