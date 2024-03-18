// Function to preview image before uploading
function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function () {
        var output = document.getElementById('profile-image');
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}

// ajax
document.getElementById('updateUserForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent normal form submission
    const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const response = await fetch(`/update_user/`, {
            method: 'POST',
            body: new FormData(this),  // Create FormData object from the form
            headers: {
                'X-CSRFToken': csrfToken  // Send CSRF token
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }

        // Check if the response has 'Content-Type' header and is JSON
        const contentType = response.headers.get('Content-Type');
        console.log(contentType);
        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();  // Convert the received data to JSON
            document.getElementById('responseMessage').textContent = data.message;
        } else {
            // If not JSON, it might be HTML or something else
            document.getElementById('responseMessage').textContent = "The server did not return a JSON response.";
        }
    } catch (error) {
        // console.error('Error:', error);
        document.getElementById('responseMessage').textContent = "An error occurred!";
    }
});

// JavaScript to toggle between "Edit" and "Save" for First name
const editButton = document.getElementById("editButton");
const cancleB = document.getElementById("cancleB");
const saveButton = document.getElementById("saveButton"); // Add the Save button in your HTML
const firstnameInput = document.getElementById("firstname");
const lastnameInput = document.getElementById("lastname");
const emailInput = document.getElementById("id_email");
const updateUserForm = document.getElementById("updateUserForm");
const newEmail = emailInput.value;
const currentEmail = "{{ user.email }}";

editButton.addEventListener("click", function () {
    if (firstnameInput.readOnly && lastnameInput.readOnly && emailInput.readOnly) {
        firstnameInput.readOnly = false;
        lastnameInput.readOnly = false;
        emailInput.readOnly = false;
        editButton.style.display = "none";
        saveButton.style.display = "block"; // Show the Save button
        cancleB.style.display = "block";
    }
});

// Not saveButton.addEventListener("click", function () {
//     // After clicking the Save button
//     firstnameInput.readOnly = true;
//     lastnameInput.readOnly = true;
//     emailInput.readOnly = true;
//     editButton.style.display = "block";
//     saveButton.style.display = "none";
//     cancleB.style.display = "none";
//     const newFirstName = firstnameInput.value;
//     const newLastName = lastnameInput.value;
//     const newEmail = emailInput.value;
//     const currentEmail = "{{ user.email }}"; // Use the current email from Django template
//     fetch(`/update_user/` Not, {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//             "X-CSRFToken": "{{ csrf_token }}", // Add Django's CSRF token in the request
//         },
//         body: JSON.stringify({
//             first_name: newFirstName,
//             last_name: newLastName,
//             email: newEmail,
//         }),
//     })
//         .then((response) => response.json())
//         .then((data) => {
//             // After successfully updating the data
//             firstnameInput.readOnly = true;
//             lastnameInput.readOnly = true;
//             emailInput.readOnly = true;
//             editButton.style.display = "block";
//             saveButton.style.display = "none";
//             editButton.innerText = "Edit"; // Restore the Edit button text
//         })
//         .catch((error) => {
//             console.error("Error:", error);
//         });
//     updateUserForm.submit();
// });

cancleB.addEventListener("click", function () {
    // Cancel the edit and switch back to display mode
    firstnameInput.readOnly = true;
    lastnameInput.readOnly = true;
    emailInput.readOnly = true;
    editButton.style.display = "block";
    saveButton.style.display = "none";
    cancleB.style.display = "none";
});

// Function to blur the image on mouseover
function blurImage() {
    const profileImage = document.getElementById('profile-image');
    profileImage.classList.add('blurred');
}

// Function to unblur the image on mouseout
function unblurImage() {
    const profileImage = document.getElementById('profile-image');
    profileImage.classList.remove('blurred');
}

// Function to change the profile image on click
function changeProfileImage() {
    const fileInput = document.getElementById('hiddenFileInput');
    fileInput.addEventListener('change', handleImageChange);
    fileInput.click();
    console.log(fileInput);
}

// Function to read the image file and display it in the <img> element
function handleImageChange(event) {
    const file = event.target.files[0];
    if (file) {
        const profileImage = document.getElementById('profile-image');
        const reader = new FileReader();

        reader.onload = function (e) {
            profileImage.src = e.target.result;
            unblurImage(); // Unblur the image when displaying a new image
        };

        reader.readAsDataURL(file);

        // Submit the form
        const form = document.getElementById('updateUserForm');
        form.submit();
    }
}
