
const sideNav = document.getElementById('sideNav');
const burger = document.querySelector('.burger');
const closeBtn = document.querySelector('.closebtn');

function openNav() {
  // Open side navigation
  sideNav.style.width = '250px';
}

function closeNav() {
  // Close side navigation
  sideNav.style.width = '0';
}

// Attach events
burger.addEventListener('click', openNav);
closeBtn.addEventListener('click', closeNav);