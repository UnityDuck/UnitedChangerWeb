function toggleUpload() {
    const form = document.getElementById('uploadForm');
    form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
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