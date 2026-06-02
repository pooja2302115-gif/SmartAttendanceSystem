// Global hover animation smoothing
document.querySelectorAll("a, button, .login-card, .guest").forEach(el => {
  el.addEventListener("mouseenter", () => {
    el.style.transition = "all 0.3s ease";
  });
});
function goBack() {
  window.history.back();
}
