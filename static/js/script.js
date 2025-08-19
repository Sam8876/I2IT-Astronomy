
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

// Loader
window.addEventListener("load", function () {
    const loader = document.getElementById("loadergif");
    const main = document.getElementById("main-content");

    if (loader && main) {
      loader.classList.add("fade-out");

      setTimeout(() => {
        loader.style.display = "none";
        main.style.display = "block";
      }, 500);  // Time should match CSS fade transition
    }
});

setTimeout(() => {
  document.getElementById("main-content").style.display = "block";
}, 3000);  // fallback if 'load' doesn't fire