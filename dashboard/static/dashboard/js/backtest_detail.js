const deleteButton = document.getElementById("btn-del");
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteConfirm = document.getElementById("deleteConfirm");

deleteButton.addEventListener("click", (e) => {
    deleteModal.show();
    let runId = e.target.getAttribute("data-run_id");
    deleteConfirm.href = `/dashboard/backtest_detail/delete/${runId}/`;
})