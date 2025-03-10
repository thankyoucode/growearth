document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".message-alert");

  alerts.forEach((alert) => {
    // Fade in effect
    setTimeout(() => {
      alert.classList.remove("opacity-0", "translate-x-full");
    }, 100); // Delay for fade-in effect

    // Attach event listener to the close button
    const closeButton = alert.querySelector(".close-message");
    closeButton.addEventListener("click", function () {
      removeMessage(alert);
    });
  });
});

// Function to remove a message alert
function removeMessage(alert) {
  alert.classList.add("opacity-0", "translate-x-full"); // Add classes for fade-out effect

  // Remove the alert from the DOM after the fade-out transition
  setTimeout(() => {
    alert.remove();
  }, 300); // Match this duration with your CSS transition duration
}
