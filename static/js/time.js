function updateDateTime() {
    const now = new Date();
    const year = now.getFullYear();
    const time = now.toLocaleTimeString();
    const date = now.toLocaleDateString();

    document.getElementById('current-year').textContent = year;
    document.getElementById('current-time').textContent = `${date} ${time}`;
}
