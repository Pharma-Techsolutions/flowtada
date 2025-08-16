// static/js/main.js

// ==========================================================================
//   FlowTada Website JavaScript - v1.0.0
// ==========================================================================

// Smooth scrolling for navigation links
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

// Fade in animation on scroll
function handleScrollAnimations() {
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;

        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('visible');
        }
    });
}

// Mobile menu toggle
function toggleMobileMenu() {
    const mobileMenu = document.querySelector('.mobile-menu');
    mobileMenu.classList.toggle('active');
}

document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    if (hamburger) {
        hamburger.addEventListener('click', toggleMobileMenu);
    }
});

// Portal modal functions
function openPortal() {
    document.getElementById('portalModal').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closePortal() {
    document.getElementById('portalModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function handlePortalLogin(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Simulate login process
    alert(`Welcome back! Redirecting to your CRM dashboard for ${email}...`);
    closePortal();

    // In a real implementation, this would handle authentication
    // and redirect to the actual CRM dashboard
}

// Header scroll effect
function handleHeaderScroll() {
    const header = document.querySelector('header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255, 255, 255, 0.98)';
        header.style.backdropFilter = 'blur(20px)';
        header.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
        header.style.boxShadow = 'none';
    }
}

// Event listeners
window.addEventListener('scroll', () => {
    handleScrollAnimations();
    handleHeaderScroll();
});

window.addEventListener('load', handleScrollAnimations);

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', function() {
    const portalModal = document.getElementById('portalModal');
    if (portalModal) {
        portalModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closePortal();
            }
        });
    }
});

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
    const nav = document.querySelector('nav');
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.querySelector('.mobile-menu');

    if (!nav.contains(e.target)) {
        mobileMenu.classList.remove('active');
    }
});

// Keyboard navigation for accessibility
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closePortal();
        document.querySelector('.mobile-menu').classList.remove('active');
    }
});

// Performance optimization - throttle scroll events
function throttle(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Apply throttling to scroll events
window.addEventListener('scroll', throttle(() => {
    handleScrollAnimations();
    handleHeaderScroll();
}, 16)); // ~60fps

// Logo fallback - show text if image fails to load
document.addEventListener('DOMContentLoaded', function() {
    const logoImg = document.querySelector('.logo-img');
    if (logoImg) {
        logoImg.addEventListener('error', function() {
            const logoContainer = document.querySelector('.logo-container');
            logoContainer.innerHTML = '<div class="logo">FlowTada</div>';
        });
    }
});

// Form validation enhancement
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Enhanced portal login with validation
function handlePortalLogin(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Basic validation
    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    if (password.length < 6) {
        alert('Password must be at least 6 characters long.');
        return;
    }

    // Show loading state
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Signing In...';
    submitBtn.disabled = true;

    // Simulate login process with delay
    setTimeout(() => {
        alert(`Welcome back! Redirecting to your CRM dashboard for ${email}...`);

        // Reset button
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;

        // Clear form and close modal
        document.getElementById('email').value = '';
        document.getElementById('password').value = '';
        closePortal();

        // In a real implementation, this would handle authentication
        // and redirect to the actual CRM dashboard
    }, 1500);
}

// Intersection Observer for better scroll animations
if ('IntersectionObserver' in window) {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe all fade-in elements
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.fade-in').forEach(el => {
            observer.observe(el);
        });
    });
}