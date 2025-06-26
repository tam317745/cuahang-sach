document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const bookId = this.getAttribute('data-book-id');
        const quantity = this.querySelector('input[name="quantity"]').value || 1;
        const csrfToken = this.querySelector('[name="csrfmiddlewaretoken"]').value;

        fetch(`/add-to-cart/${bookId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ quantity: quantity })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                document.querySelector('.cart-count').textContent = data.cart_count;
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

document.querySelectorAll('.form-cart-action').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const url = this.getAttribute('action');
        const csrfToken = this.querySelector('[name="csrfmiddlewaretoken"]').value;
        const formData = new FormData(this);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                document.querySelector('.cart-count').textContent = data.cart_count;
                if (url.includes('place-order')) {
                    window.location.href = '/';
                } else {
                    location.reload();
                }
            }
        })
        .catch(error => console.error('Error:', error));
    });
});



