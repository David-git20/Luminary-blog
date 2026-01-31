// Theme and Global Interactions
document.addEventListener('DOMContentLoaded', () => {
    console.log('Luminary Blog: Theme system initialized.');

    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    if (themeToggle) {
        // Check for saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'light') {
            body.classList.add('light-mode');
        }

        themeToggle.addEventListener('click', () => {
            body.classList.toggle('light-mode');

            // Save theme preference
            if (body.classList.contains('light-mode')) {
                localStorage.setItem('theme', 'light');
            } else {
                localStorage.setItem('theme', 'dark');
            }
        });
    }

    // Smooth hover effects for navigation
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            // Potential for micro-animations
        });
    });

    // Handle button clicks with subtle feedback
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mousedown', () => {
            button.style.transform = 'scale(0.98)';
        });
        button.addEventListener('mouseup', () => {
            button.style.transform = 'scale(1)';
        });
    });
});
