// Simple HTMX-like functionality for form handling
class SimpleHTMX {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.bindEvents();
        });
    }

    bindEvents() {
        // Handle forms with hx-post attribute
        document.addEventListener('submit', (e) => {
            const form = e.target;
            const hxPost = form.getAttribute('hx-post');
            const hxTarget = form.getAttribute('hx-target');
            
            if (hxPost && hxTarget) {
                e.preventDefault();
                this.handleFormSubmit(form, hxPost, hxTarget);
            }
        });
    }

    async handleFormSubmit(form, url, targetSelector) {
        const target = document.querySelector(targetSelector);
        if (!target) return;

        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Sending...';
        submitButton.disabled = true;
        form.classList.add('loading');

        try {
            const formData = new FormData(form);
            
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });

            if (response.ok) {
                const result = await response.text();
                target.innerHTML = result;
                
                // Reset form if successful
                if (result.includes('success') || result.includes('Thank you')) {
                    form.reset();
                }
            } else {
                target.innerHTML = '<div class="text-red-600 text-sm">Error sending message. Please try again.</div>';
            }
        } catch (error) {
            console.error('Form submission error:', error);
            target.innerHTML = '<div class="text-red-600 text-sm">Network error. Please check your connection and try again.</div>';
        } finally {
            // Reset button state
            submitButton.textContent = originalText;
            submitButton.disabled = false;
            form.classList.remove('loading');
        }
    }
}

// Initialize when DOM is ready
new SimpleHTMX();