function checkFile() {
    const fileInput = document.getElementById('file');
    const uploadButton = document.getElementById('Upload');

    // Check if a file has been selected
    if (fileInput.files.length > 0) {
        // Get the first file in the list of selected files and check if it is an image
        const file = fileInput.files[0];
        const fileType = file.type.split('/')[0];
        if (fileType === 'image') {
            // If the file is an image, enable the upload button
            uploadButton.disabled = false;
        } else {
            // If the file is not an image, disable the upload button, show an alert message and reload the page
            uploadButton.disabled = true;
            alert('Please select an image file for analysis.');
            location.reload();
        }
    } else {
        // If no file has been selected, disable the upload button
        uploadButton.disabled = true;
    }
}

function showLoading() {
    const title = document.querySelector('h1');
    const form = document.querySelector('form');
    const loadingDiv = document.getElementById('loading');
    title.style.display = 'none';
    form.style.display = 'none';
    loadingDiv.style.display = 'flex';
}


