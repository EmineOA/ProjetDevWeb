// Charge le header et footer sur toutes les pages
document.addEventListener('DOMContentLoaded', () => {
    fetch('partials/header.html')
      .then(response => response.text())
      .then(data => document.getElementById('header').innerHTML = data);
  
    fetch('partials/footer.html')
      .then(response => response.text())
      .then(data => document.getElementById('footer').innerHTML = data);
  });