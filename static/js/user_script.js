document.addEventListener('DOMContentLoaded', function() {
    const orderHeaders = document.querySelectorAll('.order-header');

    orderHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const details = this.nextElementSibling;
            if (details.style.display === 'none' || details.style.display === '') {
                details.style.display = 'block';
            } else {
                details.style.display = 'none';
            }
        });
    });
});
