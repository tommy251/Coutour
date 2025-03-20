// Show the address form and pass the product ID
function showAddressForm(productId) {
    const sizeSelect = document.querySelector(`.size-select[data-product-id="${productId}"]`);
    const selectedSize = sizeSelect ? sizeSelect.value : null;

    // Only prompt for size if the product has a size dropdown and more than one option, and no size is selected
    if (sizeSelect && sizeSelect.options.length > 1 && selectedSize === "") {
        alert('Please select a size before proceeding.');
        return;
    }

    // Store product ID and size in the form
    document.getElementById('product-id').value = productId;
    document.getElementById('selected-size').value = selectedSize || '';

    showSection('address');
}

// Handle address form submission and initiate Paystack payment
async function submitOrder(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch('/submit_address', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        // Redirect to Paystack payment URL
        window.location.href = data.payment_url;
    } catch (error) {
        console.error('Error during address submission:', error);
        alert('An error occurred while processing your address. Please try again.');
    }
}

// Show a specific section and hide others
function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

// Auto-scrolling carousel logic
document.addEventListener('DOMContentLoaded', () => {
    showSection('home');

    // Carousel setup
    const carousel = document.getElementById('product-carousel');
    const images = carousel.querySelectorAll('img');
    const indicatorsContainer = document.getElementById('carousel-indicators');
    let currentIndex = 0;

    // Create indicators
    images.forEach((_, index) => {
        const indicator = document.createElement('span');
        indicator.addEventListener('click', () => {
            currentIndex = index;
            updateCarousel();
        });
        indicatorsContainer.appendChild(indicator);
    });

    function updateCarousel() {
        carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
        const indicators = indicatorsContainer.querySelectorAll('span');
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentIndex);
        });
    }

    // Auto-scroll every 3 seconds
    setInterval(() => {
        currentIndex = (currentIndex + 1) % images.length;
        updateCarousel();
    }, 3000);

    // Initial update
    updateCarousel();

    // Add event listeners to all size select dropdowns
    const sizeSelects = document.querySelectorAll('.size-select');
    sizeSelects.forEach(select => {
        const productId = select.getAttribute('data-product-id');
        const buyButton = document.querySelector(`.buy-now[data-product-id="${productId}"]`);

        // Ensure the button is initially disabled if a size selection is required
        if (select.options.length > 1) {
            buyButton.disabled = true;
        } else {
            buyButton.disabled = false;
        }

        select.addEventListener('change', function() {
            buyButton.disabled = this.value === "";
        });
    });

    // Ensure buttons for products without sizes are clickable
    const buyButtons = document.querySelectorAll('.buy-now');
    buyButtons.forEach(button => {
        const productId = button.getAttribute('data-product-id');
        const sizeSelect = document.querySelector(`.size-select[data-product-id="${productId}"]`);
        if (!sizeSelect || sizeSelect.options.length <= 1) {
            button.disabled = false;
        }
    });

    // Toggle hamburger menu
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('open');
    });
});