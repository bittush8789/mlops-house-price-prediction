document.addEventListener('DOMContentLoaded', () => {
    const predictionForm = document.getElementById('predictionForm');
    const resultContainer = document.getElementById('result');
    const predictedPrice = document.getElementById('predictedPrice');
    const submitBtn = document.getElementById('submitBtn');

    predictionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Initial button state
        const originalBtnContent = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span>Processing Data...</span><i class="fas fa-circle-notch fa-spin"></i>';
        submitBtn.disabled = true;
        
        // Prepare payload
        const formData = new FormData(predictionForm);
        const data = {};
        formData.forEach((value, key) => {
            if (['area_sqft', 'bedrooms', 'bathrooms', 'floors', 'parking', 'year_built'].includes(key)) {
                data[key] = parseInt(value);
            } else {
                data[key] = value;
            }
        });

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                // Add a small delay for simulation/visual effect
                setTimeout(() => {
                    // Populate results
                    predictedPrice.innerText = result.predicted_price;
                    document.getElementById('priceRange').innerText = result.price_range;
                    document.getElementById('pricePerSqft').innerText = result.price_per_sqft;
                    document.getElementById('confidenceLevel').innerText = result.confidence_level;
                    document.getElementById('marketTier').innerText = result.market_tier;
                    document.getElementById('aiFactors').innerText = result.ai_factors;
                    
                    // Animate result entrance
                    resultContainer.classList.remove('hidden');
                    
                    // Smooth scroll to the entire card
                    const mainCard = document.querySelector('.main-card');
                    mainCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    
                    // Restore button
                    submitBtn.innerHTML = originalBtnContent;
                    submitBtn.disabled = false;
                }, 800);
            } else {
                alert("Error: " + result.detail);
                submitBtn.innerHTML = originalBtnContent;
                submitBtn.disabled = false;
            }
        } catch (error) {
            console.error("Prediction failed:", error);
            alert("Something went wrong. Please try again.");
            submitBtn.innerHTML = originalBtnContent;
            submitBtn.disabled = false;
        }
    });

    // Add subtle hover effects for inputs
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.parentElement.style.transform = 'translateX(5px)';
            input.parentElement.parentElement.style.transition = '0.3s ease';
        });
        input.addEventListener('blur', () => {
            input.parentElement.parentElement.style.transform = 'translateX(0)';
        });
    });

    // Initialize sub-locations
    window.updateSubLocations();
});

const subLocations = {
    'Delhi': ['Saket', 'Dwarka', 'Rohini', 'Vasant Kunj', 'Lajpat Nagar', 'Karol Bagh'],
    'Gurgaon': ['DLF Phase 1', 'Golf Course Road', 'Sohna Road', 'Sector 56', 'New Gurgaon'],
    'Noida': ['Sector 50', 'Sector 76', 'Sector 137', 'Sector 150'],
    'Ghaziabad': ['Indirapuram', 'Vaishali', 'Raj Nagar Extension'],
    'Faridabad': ['Sector 15', 'Green Valley', 'Neharpar']
};

window.updateSubLocations = function() {
    const locationSelect = document.getElementById('location');
    const subLocationSelect = document.getElementById('sub_location');
    const selectedCity = locationSelect.value;
    
    // Clear current options
    subLocationSelect.innerHTML = '';
    
    // Add new options
    if (subLocations[selectedCity]) {
        subLocations[selectedCity].forEach(sub => {
            const option = document.createElement('option');
            option.value = sub;
            option.textContent = sub;
            subLocationSelect.appendChild(option);
        });
    }
};
