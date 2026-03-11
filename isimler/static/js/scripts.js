/* ============================================
   THEME SYSTEM - Premium Dark/Light Mode
   ============================================ */

(function () {
    // Apply theme immediately to prevent flash
    const savedTheme = localStorage.getItem('dark-mode');
    if (savedTheme === 'true') {
        document.documentElement.classList.add('dark-mode');
        document.body && document.body.classList.add('dark-mode');
    }
})();

document.addEventListener('DOMContentLoaded', function () {
    // Apply saved theme on DOM ready
    const isDark = localStorage.getItem('dark-mode') === 'true';
    if (isDark) {
        document.body.classList.add('dark-mode');
    }

    // Toggle handler
    const toggleBtn = document.getElementById('themeToggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            document.body.classList.toggle('dark-mode');
            const nowDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('dark-mode', nowDark ? 'true' : 'false');
        });
    }
});
