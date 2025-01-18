// Preloader functionality
document.addEventListener("DOMContentLoaded", function () {
  window.addEventListener("load", function () {
    const preloader = document.getElementById("preloader");
    if (preloader) {
      preloader.style.display = "none";
    }
  });
});