// Collapsible left-nav toggle button
document.addEventListener("DOMContentLoaded", function () {
    var btn = document.createElement("button");
    btn.id = "nav-toggle";
    btn.title = "Toggle navigation";
    btn.textContent = "◀";
    document.body.appendChild(btn);

    btn.addEventListener("click", function () {
        var hidden = document.body.classList.toggle("nav-hidden");
        btn.textContent = hidden ? "▶" : "◀";
    });
});
