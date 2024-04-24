const fileInput = document.getElementById('fileInput');
const uploadForm = document.getElementById('uploadForm');
const resultFileDiv = document.getElementById('resultFileDiv');

uploadForm.addEventListener('submit', function(event) {
    event.preventDefault();

    resultFileDiv.style.display = 'block';

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload_audio', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            resultFileDiv.textContent = data.success;
        } else if (data.error) {
            resultFileDiv.textContent = 'Upload error: ' + data.error;
        }
        setTimeout(() => {
            resultFileDiv.style.display = 'none';
        }, 5000);
    })
    .catch(error => {
        resultFileDiv.textContent = 'Upload error: ' + error;
    });
});

/* Drug and drop*/
fileLabel.addEventListener('drop', function(e) {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
});

/* Hide and show edit track form*/
function toggleEditForm(index) {
    var editForm = document.getElementById('editForm_' + index);
    if (editForm.style.display === 'none') {
	    editForm.style.display = 'block';
    } else {
	    editForm.style.display = 'none';
    }
}


function editAudio(location, startTimeId, endTimeId) {
const begin = document.getElementById(startTimeId).value;
const end = document.getElementById(endTimeId).value;


fetch('/audio_edit', {
    method: 'POST',
    body: JSON.stringify({
	'track_name': location,
	'begin': begin,
	'end': end
    }),
    headers: {
	'Content-Type': 'application/json'
    }
})
.then(response => {
    if (response.ok) {
	console.log('Audio edited successfully!');
    } else {
	console.error('Failed to edit audio');
    }
})
.catch(error => {
    console.error('Error editing audio:', error);
});
}
