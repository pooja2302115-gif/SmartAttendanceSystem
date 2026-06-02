// Global smooth hover animation helper
document.querySelectorAll("a, button, .login-card").forEach(el => {
  el.addEventListener("mouseenter", () => {
    el.style.transition = "all 0.3s ease";
  });
});
function goBack() {
  window.history.back();
}
