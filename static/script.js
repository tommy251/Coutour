// Show the address form and pass the product ID
function showAddressForm(productId) {
    // Convert productId to a number if it's a string
    productId = parseInt(productId, 10);
    console.log(`showAddressForm called with productId: ${productId}`);

    const optionSelect = document.querySelector(`.option-select[data-product-id="${productId}"]`);
    const selectedOption = optionSelect ? optionSelect.value : null;

    // Determine the category of the product to customize the error message
    const productCard = optionSelect ? optionSelect.closest('.product-card') : null;
    const category = productCard ? productCard.getAttribute('data-category') : '';

    // Only prompt for option if the product has an option dropdown, has more than one option, and no option is selected
    if (optionSelect && optionSelect.options.length > 1 && selectedOption === "") {
        // Remove any existing error messages
        const existingError = optionSelect.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Create and display an inline error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = category === 'wristwatches' ? 'Please select an age group before proceeding.' : 'Please select a size before proceeding.';
        optionSelect.parentElement.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 3000);
        return;
    }

    // Store product ID and option in the form
    document.getElementById('product-id').value = productId;
    document.getElementById('selected-option').value = selectedOption || '';

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
            const formError = document.createElement('div');
            formError.className = 'error-message';
            formError.textContent = `Error: ${data.error}`;
            form.appendChild(formError);
            setTimeout(() => formError.remove(), 3000);
            return;
        }

        window.location.href = data.payment_url;
    } catch (error) {
        const formError = document.createElement('div');
        formError.className = 'error-message';
        formError.textContent = 'An error occurred while processing your address. Please try again.';
        form.appendChild(formError);
        setTimeout(() => formError.remove(), 3000);
    }
}

// Show a specific section and hide others
function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'block';
    } else {
        console.error(`Section with ID ${sectionId} not found`);
    }
}

// Auto-scrolling carousel logic
document.addEventListener('DOMContentLoaded', () => {
    // Show the section based on URL hash or default to 'home'
    const hash = window.location.hash.replace('#', '');
    showSection(hash || 'home');

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

    // Add event listeners to all option select dropdowns
    const optionSelects = document.querySelectorAll('.option-select');
    optionSelects.forEach(select => {
        const productId = select.getAttribute('data-product-id');
        const buyButton = document.querySelector(`.buy-now[data-product-id="${productId}"]`);

        if (buyButton) {
            if (select.options.length > 1) {
                buyButton.disabled = true;
            } else {
                buyButton.disabled = false;
            }

            select.addEventListener('change', function() {
                console.log(`Dropdown changed for product ${productId}: Selected value = ${this.value}`);
                const existingError = this.parentElement.querySelector('.error-message');
                if (existingError) {
                    existingError.remove();
                }
                buyButton.disabled = this.value === "";
                if (!buyButton.disabled) {
                    console.log(`Buy Now button enabled for product ${productId}`);
                }
            });
        } else {
            console.error(`Buy Now button not found for product ${productId}`);
        }
    });

    // Ensure buttons for products without options are clickable
    const buyButtons = document.querySelectorAll('.buy-now');
    buyButtons.forEach(button => {
        const productId = button.getAttribute('data-product-id');
        const optionSelect = document.querySelector(`.option-select[data-product-id="${productId}"]`);
        if (!optionSelect || optionSelect.options.length <= 1) {
            button.disabled = false;
            console.log(`Buy Now button enabled for product ${productId} (no options)`);
        }
        // Fallback: Ensure the button is enabled if it has no option dropdown
        if (!optionSelect) {
            button.removeAttribute('disabled');
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