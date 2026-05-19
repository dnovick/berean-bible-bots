// Point the logo/site-name links back to the landing page root
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(
        "a.md-header__button.md-logo, a.md-header__title"
    ).forEach(function (el) {
        el.setAttribute("href", "https://bereanbiblebots.com/");
    });
});
