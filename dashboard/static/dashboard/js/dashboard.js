// Makes each row in backtest dashboard clickable
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".clickable-row").forEach(function (row) {
        row.addEventListener("click", function () {
            const href = row.dataset.href;
            if (href) {
                window.location.href = href;
            }
        });
    });
});

