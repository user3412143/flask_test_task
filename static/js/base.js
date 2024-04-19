document.addEventListener("DOMContentLoaded", function() {
	document.getElementById("registerBtn").addEventListener("click", function() {
		document.getElementById("loginModal").style.display = "block";
	});

document.querySelectorAll(".close").forEach(function(closeBtn) {
	closeBtn.addEventListener("click", function() {
		this.parentElement.parentElement.style.display = "none";
	});
});
});

document.getElementById('switchToRegister').addEventListener('click', function() {
    document.getElementById('loginModal').style.display = 'none';
    document.getElementById('registerModal').style.display = 'block';
});

document.getElementById('switchToLogin').addEventListener('click', function() {
    document.getElementById('registerModal').style.display = 'none';
    document.getElementById('loginModal').style.display = 'block';
});



async function postData(url = 'http://127.0.0.1:5000', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.json();
}

// Обработчик события отправки формы для логина
document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    const response = await postData('/login', data);
    console.log(response); // Здесь можно обновить содержимое страницы согласно полученному JSON
});

// Обработчик события отправки формы для регистрации
document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = {
        username: formData.get('username'),
        email: formData.get('email'),
        password: formData.get('password')
    };
    const response = await postData('/create_account', data);
    console.log(response); // Здесь можно обновить содержимое страницы согласно полученному JSON
});
