document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const expanded = navLinks.classList.contains('active');
            navToggle.setAttribute('aria-expanded', expanded);
        });
    }

    document.querySelectorAll('[data-confirm]').forEach((link) => {
        link.addEventListener('click', (event) => {
            const message = link.dataset.confirm;
            if (message && !confirm(message)) {
                event.preventDefault();
            }
        });
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 768 && navLinks) {
            navLinks.classList.remove('active');
            if (navToggle) {
                navToggle.setAttribute('aria-expanded', 'false');
            }
        }
    });
});
