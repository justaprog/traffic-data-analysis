// static/js/script.js

// This script might add client-side interactivity or dynamic updates to the traffic list.

console.log("JavaScript loaded!");

// Example: highlight high congestion items ( > 70% ) after the page loads
document.addEventListener("DOMContentLoaded", () => {
  const listItems = document.querySelectorAll("#trafficList li");
  listItems.forEach(li => {
    const congestionElement = li.querySelector(".congestion");
    if (congestionElement) {
      // Extract the numeric congestion level from the text (e.g., "Congestion: 80%")
      const text = congestionElement.textContent.trim();
      const level = parseInt(text.replace(/\D/g, ""), 10);

      if (level > 70) {
        // highlight the item in red
        li.style.backgroundColor = "#ffe6e6";
      }
    }
  });
});
