// Mobile menu toggle script
const mobileMenuToggle = document.getElementById("mobile-menu-toggle");
const mobileMenu = document.getElementById("mobile-menu");
const hamburger = document.getElementById("hamburger");

mobileMenuToggle.addEventListener("click", () => {
  const isMenuOpen = mobileMenu.classList.contains("max-h-0");
  if (isMenuOpen) {
    mobileMenu.classList.remove("max-h-0", "opacity-0");
    mobileMenu.classList.add("max-h-96", "opacity-100");
  } else {
    mobileMenu.classList.add("max-h-0", "opacity-0");
    mobileMenu.classList.remove("max-h-96", "opacity-100");
  }
});
