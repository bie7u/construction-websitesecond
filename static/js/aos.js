// Simple Animation on Scroll library to replace blocked AOS
class SimpleAOS {
    constructor() {
        this.elements = [];
        this.initialized = false;
    }

    init(options = {}) {
        this.options = {
            duration: options.duration || 1000,
            once: options.once !== false, // Default to true
            offset: options.offset || 100,
            ...options
        };

        // Find all elements with data-aos attributes
        this.elements = Array.from(document.querySelectorAll('[data-aos]'));
        
        // Create observer
        this.observer = new IntersectionObserver(
            this.handleIntersection.bind(this),
            {
                rootMargin: `0px 0px -${this.options.offset}px 0px`,
                threshold: 0.1
            }
        );

        // Start observing elements
        this.elements.forEach(el => {
            this.observer.observe(el);
            // Initially hide elements
            el.style.opacity = '0';
            el.style.transform = this.getInitialTransform(el.getAttribute('data-aos'));
            el.style.transition = `opacity ${this.options.duration}ms ease, transform ${this.options.duration}ms ease`;
        });

        this.initialized = true;
    }

    getInitialTransform(animation) {
        switch (animation) {
            case 'fade-up':
                return 'translateY(50px)';
            case 'fade-down':
                return 'translateY(-50px)';
            case 'fade-left':
                return 'translateX(50px)';
            case 'fade-right':
                return 'translateX(-50px)';
            case 'zoom-in':
                return 'scale(0.8)';
            case 'zoom-out':
                return 'scale(1.2)';
            default:
                return 'translateY(30px)';
        }
    }

    getFinalTransform() {
        return 'translateY(0) translateX(0) scale(1)';
    }

    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const delay = parseInt(element.getAttribute('data-aos-delay')) || 0;
                
                setTimeout(() => {
                    element.style.opacity = '1';
                    element.style.transform = this.getFinalTransform();
                }, delay);

                // If once is true, stop observing this element
                if (this.options.once) {
                    this.observer.unobserve(element);
                }
            } else if (!this.options.once) {
                // Reset animation if once is false
                const element = entry.target;
                element.style.opacity = '0';
                element.style.transform = this.getInitialTransform(element.getAttribute('data-aos'));
            }
        });
    }

    refresh() {
        if (this.initialized) {
            // Re-observe all elements
            this.elements.forEach(el => {
                this.observer.unobserve(el);
                this.observer.observe(el);
            });
        }
    }
}

// Create global AOS object
window.AOS = new SimpleAOS();

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (window.AOS && !window.AOS.initialized) {
        window.AOS.init();
    }
});