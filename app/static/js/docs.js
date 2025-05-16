function toggleUpload() {
    const form = document.getElementById('uploadForm');
    form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
}

function validateFileType() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const validImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

        if (!validImageTypes.includes(file.type)) {
            alert("Пожалуйста, выберите изображение (jpg, png, gif, webp).");
            fileInput.value = '';
        }
    }
}
