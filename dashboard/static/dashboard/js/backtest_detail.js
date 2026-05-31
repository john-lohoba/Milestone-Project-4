const deleteButton = document.getElementById("btn-del");
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteConfirm = document.getElementById("deleteConfirm");

const editButton = document.getElementById("btn-edit");
const editModal = new bootstrap.Modal(document.getElementById("editModal"));
const editForm = document.getElementById("editForm");

deleteButton.addEventListener("click", (e) => {
    deleteModal.show();
    let runId = e.target.getAttribute("data-run_id");
    deleteConfirm.href = `/dashboard/backtest_detail/delete/${runId}/`;
})

editButton.addEventListener("click", (e) => {
    editModal.show();
    let runId = e.target.getAttribute("data-run_id");
    editForm.setAttribute("action", `/dashboard/backtest_detail/edit/${runId}/`);
})