function toggleUpload() {
    const form = document.getElementById('uploadForm');
    form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
}
