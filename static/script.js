function showAddressForm(productId) {
    const optionSelects = document.querySelectorAll(`.option-select[data-product-id="${productId}"]`);
    let allSelected = true;
    const selectedOptions = {};

    optionSelects.forEach(select => {
        const optionType = select.getAttribute('data-option-type') || 'option';
        const selectedValue = select.value;
        selectedOptions[optionType] = selectedValue;

        if (select.options.length > 1 && selectedValue === "") {
            allSelected = false;
            const existingError = select.parentElement.querySelector('.error-message');
            if (existingError) {
                existingError.remove();
            }
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = `Please select a ${optionType} before proceeding.`;
            select.parentElement.appendChild(errorDiv);
            setTimeout(() => errorDiv.remove(), 3000);
        }
    });

    if (!allSelected) {
        return;
    }

    // Store product ID and options in the form
    document.getElementById('product-id').value = productId;
    document.getElementById('selected-size').value = JSON.stringify(selectedOptions);

    showSection('address');
}