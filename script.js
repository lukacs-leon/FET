// All buttons intentionally "fail" after a delay
document.querySelectorAll(".action-btn").forEach(button => {
  button.addEventListener("click", () => {
    const originalText = button.textContent;
    button.disabled = true;
    button.textContent = "loading...";

    const delay = 3000 + Math.random() * 2000;

    setTimeout(() => {
      button.textContent = "something went wrong";
    }, delay);
  });
});