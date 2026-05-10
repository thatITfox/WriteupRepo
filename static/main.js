// The code below makes every code that will be rendered by highlight.js
// use the atom-one-dark theme.

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('pre').forEach(el => {
        el.classList.add('theme-atom-one-dark');
    });
});