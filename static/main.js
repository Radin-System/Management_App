const toggleButton = document.getElementById('darkModeToggle');
toggleButton.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
});
/*
// this part checks for the darkmode cookie
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('dark-mode') === 'true') {
        document.body.classList.add('dark-mode');
    }
});

// this part creates and changes the darkmode cookie
toggleButton.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('dark-mode', document.body.classList.contains('dark-mode'));
});
*/