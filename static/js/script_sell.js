document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('sellForm');
    const productDisplay = document.getElementById('productDisplay');
    const productDetailsSection = document.getElementById('product-details');
    const productSelect = document.getElementById('product');
    const otherProductDiv = document.getElementById('otherProductDiv');
    const otherProductInput = document.getElementById('otherProduct');
    const additionalImagesInput = document.getElementById('additionalImages');

    productSelect.addEventListener('change', () => {
        if (productSelect.value === 'Other') {
            otherProductDiv.style.display = 'block';
            otherProductInput.required = true;
        } else {
            otherProductDiv.style.display = 'none';
            otherProductInput.required = false;
        }
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const product = productSelect.value === 'Other' ? otherProductInput.value : productSelect.value;
        const price = document.getElementById('price').value;
        const description = document.getElementById('description').value;
        const primaryImage = document.getElementById('primaryImage').files[0];

        const promises = [];

        if (primaryImage) {
            promises.push(new Promise((resolve) => {
                const reader = new FileReader();
                reader.onload = function (event) {
                    resolve(`<img src="${event.target.result}" alt="Primary Image" style="max-width: 100%; margin: 10px 0;">`);
                };
                reader.readAsDataURL(primaryImage);
            }));
        }

        Promise.all(promises).then((imagesHTML) => {
            const imageHTML = imagesHTML[0] || '';
            productDisplay.innerHTML = `
                <div style="display: flex; flex-direction: row; justify-content: space-between;">
                    <div style="flex: 1; text-align: left;">
                        <p><strong>Seller Name:</strong></p>
                        <p><strong>Email Address:</strong></p>
                        <p><strong>Phone Number:</strong></p>
                        <p><strong>Product Name:</strong></p>
                        <p><strong>Price:</strong></p>
                        <p><strong>Description:</strong></p>
                        <p><strong>Image:</strong></p>
                    </div>
                    <div style="flex: 1; text-align: left;">
                        <p>${name}</p>
                        <p>${email}</p>
                        <p>${phone}</p>
                        <p>${product}</p>
                        <p>$${price}</p>
                        <p>${description}</p>
                        <div>${imageHTML}</div>
                    </div>
                </div>
            `;
            productDetailsSection.style.display = 'block';
        });

        form.reset();
        otherProductDiv.style.display = 'none';
    });
});
