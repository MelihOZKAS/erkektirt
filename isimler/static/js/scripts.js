function toggleDarkMode() {
    var body = document.body;
    body.classList.toggle("dark-mode");
    const navBar = document.querySelector('.navbar');
    navBar.classList.toggle('navbar-dark');

    const darkModeIcon = document.getElementById('darkModeIcon');
    if (body.classList.contains('dark-mode')) {
        darkModeIcon.src = "https://img.icons8.com/ios-filled/50/ffffff/sun.png";
        localStorage.setItem('dark-mode', 'true');
    } else {
        darkModeIcon.src = "https://img.icons8.com/?size=100&id=45475&format=png&color=000000";
        localStorage.setItem('dark-mode', 'false');
    }
}