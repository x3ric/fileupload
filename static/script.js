document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("upload-form");
    const fileInput = document.getElementById("file-upload");
    const fileLabel = document.getElementById("file-label");
    const selectedFile = document.getElementById("selected-file");

    form.addEventListener("dragover", function(event) {
        event.preventDefault();
        form.classList.add("dragover");
    });

    form.addEventListener("dragleave", function(event) {
        event.preventDefault();
        form.classList.remove("dragover");
    });

    form.addEventListener("drop", function(event) {
        event.preventDefault();
        form.classList.remove("dragover");
        const file = event.dataTransfer.files[0];
        fileInput.files = event.dataTransfer.files;
        displaySelectedFileName(file);
    });

    fileInput.addEventListener("change", function(event) {
        const file = event.target.files[0];
        displaySelectedFileName(file);
    });

    function displaySelectedFileName(file) {
        if (file) {
            selectedFile.textContent = 'Selected file: ' + file.name;
        } else {
            selectedFile.textContent = '';
        }
    }
});
