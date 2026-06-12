// Point the logo link and the site-name title to the root homepage
document.addEventListener("DOMContentLoaded", function () {
    // Logo is an <a> — just update href
    document.querySelectorAll("a.md-header__button.md-logo").forEach(function (el) {
        el.setAttribute("href", "/");
    });

    // Site title is a <div> — make it behave like a link
    var titleEl = document.querySelector(".md-header__title");
    if (titleEl) {
        titleEl.style.cursor = "pointer";
        titleEl.addEventListener("click", function () {
            window.location.href = "/";
        });
    }
});
