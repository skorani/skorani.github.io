// Copy-to-clipboard for the email address.
// The button stays hidden unless the browser can copy, and the status message
// only reports success after the copy has actually worked.
(function () {
  if (!navigator.clipboard || !window.isSecureContext) return;

  document.querySelectorAll("[data-copy]").forEach(function (button) {
    var status = document.getElementById(button.getAttribute("data-copy-status"));
    button.hidden = false;
    button.addEventListener("click", function () {
      navigator.clipboard.writeText(button.getAttribute("data-copy")).then(
        function () {
          if (status) status.textContent = "Email address copied.";
        },
        function () {
          if (status) status.textContent = "Couldn't copy automatically. Select the address above and copy it.";
        }
      );
    });
  });
})();
