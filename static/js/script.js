// Flash message auto-hide
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Show prediction form
function showPredictionForm() {
    const form = document.getElementById('predictionForm');
    if (form) {
        form.style.display = 'block';
        form.scrollIntoView({ behavior: 'smooth' });
    }
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = '#dc3545';
            } else {
                field.style.borderColor = '#e9ecef';
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields.');
        }
    });
});

// Image error handling
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            if (!this.src.includes('placeholder.svg')) {
                this.src = '/placeholder.svg?height=200&width=300';
            }
        });
    });
});

// Search form enhancements
const searchForm = document.querySelector('.search-form form');
if (searchForm) {
    const brandSelect = searchForm.querySelector('select[name="brand"]');
    const modelInput = searchForm.querySelector('input[name="model"]');
    
    if (brandSelect && modelInput) {
        brandSelect.addEventListener('change', function() {
            if (this.value) {
                modelInput.placeholder = `Search ${this.value} models...`;
            } else {
                modelInput.placeholder = 'Search model...';
            }
        });
    }
}
