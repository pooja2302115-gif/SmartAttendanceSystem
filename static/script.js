// Global hover ripple effect (light UX polish)
document.querySelectorAll("button, a, .card").forEach(el => {
  el.addEventListener("mouseenter", () => {
    el.style.transition = "all 0.3s ease";
  });
});
