const fileInput = document.getElementById('fileInput');


fileLabel.addEventListener('drop', function(e) {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
});



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

alert(location)

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
