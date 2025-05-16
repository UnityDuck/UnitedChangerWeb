function toggleUpload() {
    const form = document.getElementById('uploadForm');
    form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
}

function validateFileType() {
    const fileInput = document.querySelector('input[name="avatar"]');
    const file = fileInput.files[0];

    if (file) {
        const validImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

        if (!validImageTypes.includes(file.type)) {
            alert("Пожалуйста, выберите изображение (форматы: JPG, PNG, GIF, WEBP).");
            fileInput.value = '';
        }
    }
}

function generateApiKey() {
    fetch('/generate_api_key', {
      method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('api-key-box').textContent = data.api_key;
    })
    .catch(error => console.error('Ошибка при генерации ключа:', error));
}