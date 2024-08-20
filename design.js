// Function to update the file name display
function updateFileName() {
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name');
    fileNameDisplay.textContent = fileInput.files.length > 0 ? fileInput.files[0].name : 'No file chosen';
}

// Function to validate the form submission
function validateForm() {
    const fileInput = document.getElementById('file-upload');
    if (fileInput.files.length === 0) {
        showNotification();
        return false;
    }
    return true;
}

// Function to show the notification when no file is chosen
function showNotification() {
    const notification = document.querySelector('.notification');
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

// Function to handle file deletion
document.getElementById('delete-all-button').addEventListener('click', function() {
    const selectedFiles = document.querySelectorAll('input[name="files-to-delete"]:checked');
    const filenames = Array.from(selectedFiles).map(checkbox => checkbox.value);
    
    if (filenames.length > 0) {
        if (confirm('Are you sure you want to delete the selected files?')) {
            const form = document.getElementById('delete-form');
            document.getElementById('filenames-to-delete').value = filenames.join(',');
            form.submit();
        }
    } else {
        alert('No files selected.');
    }
});
