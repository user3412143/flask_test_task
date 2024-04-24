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


const resultDiv = document.getElementById('result');
const resultRegDiv = document.getElementById('resultReg');
const loginModal = document.getElementById('loginModal');
const registerModal = document.getElementById('registerModal');

function handleFormSubmit(endpoint, form, resultElement) {
    const formData = new FormData(form);

    resultElement.style.display = 'block';

    fetch(endpoint, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            resultElement.textContent = 'Success: ' + data.success;
        } else if (data.error) {
            resultElement.textContent = 'Failed: ' + data.error;
        }
        setTimeout(() => {
            resultElement.style.display = 'none';
        }, 5000);
    });
}

loginModal.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    handleFormSubmit('/login', event.target, resultDiv);
});

registerModal.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    handleFormSubmit('/create_account', event.target, resultRegDiv);
});
