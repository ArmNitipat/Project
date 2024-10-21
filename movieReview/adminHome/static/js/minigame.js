// shows Rows when button is clicked
document.getElementById("showRowsButton1").addEventListener("click", function() {
    showRows();
    startGame();
    gametype = 1;
});

document.getElementById("showRowsButton2").addEventListener("click", function() {
    showRows();
    startGame();
    gametype = 2;
});

// game logic
let gametype = 0;
let currentRound = 0;
const totalRounds = 10;
let score = 0;
let countdownTimer;
const countdownDuration = 8; // 8 seconds
let answerSubmitted = false;

function startGame() {
    currentRound = 1;
    score = 0;
    update_session_game().then(() => {
        nextRound();
    }).catch(error => {
        // show err and reload web
        console.log("Game cannot proceed:", error);
        window.location.reload();
    });
}

function nextRound() {
    if (currentRound > totalRounds) {
        endGame();
        return;
    }
    fetchRoundData();
}

async function fetchRoundData() {
    let categoryParam = gametype === 1 ? 'Movie' : 'Star'; // Directly set the parameter based on gameType
    let url = `/minigame/?category=${categoryParam}`; // Construct the URL with the category query parameter
    try {
        const response = await fetch(url, {
            method: 'GET', // Specify method for clarity, though 'GET' is default
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        const data = await response.json();
        updateGameUI(data);
        startCountdown();
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

async function postScore() {
    try {
        const csrfToken = getCookie('csrftoken');
        const response = await fetch(`/updatecoin/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}',
            },
            body: JSON.stringify({})
        });
        if (!response.ok) {
            throw new Error('Server responded with a status: ' + response.status);
        }
        const data = await response.json();
        if (data.status === "success") {
            console.log('Coin updated successfully');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function getCookie(name) {
    // การดึงโทเค็น CSRF จากคุกกี้และรวมไว้ในคำขอ AJAX
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateGameUI(data) {
    console.log('Data:', data);
    const imageElement = document.querySelector('#rowAsk img');
    if (data.mainmovie_images) {
        imageElement.src = data.mainmovie_images;
        imageElement.alt = "Main Image";
        console.log('image:', data.mainmovie_images);
    }
    else {
        imageElement.src = data.mainstar_image;
        imageElement.alt = "Main Image";
        console.log('image:', data.mainstar_image);
    }

    answer = ('Data:', data.answer);
    const answersContainer = document.getElementById('rowAnswer');
    answersContainer.innerHTML = '';

    data.main_names.forEach(name => {
        const colDiv = document.createElement('div');
        colDiv.className = 'col-md-6 p-3 d-flex justify-content-center align-items-center';

        const cardDiv = document.createElement('div');
        cardDiv.className = 'border card-body w-100';

        const a = document.createElement('a');
        a.href = '#';
        a.className = 'answerBtn text-center d-block p-3';
        a.dataset.answer = name;
        a.textContent = name;
        a.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default anchor behavior
            selectAnswer(name,  answer);
        });

        cardDiv.appendChild(a);
        colDiv.appendChild(cardDiv);
        answersContainer.appendChild(colDiv);
    });
}


function startCountdown() {
    clearInterval(countdownTimer);
    let timeLeft = countdownDuration;
    document.getElementById("Timebody").style.display = 'flex';

    countdownTimer = setInterval(() => {
        timeLeft--;
        document.getElementById("time").textContent = timeLeft;
        if (timeLeft <= 0) {
            clearInterval(countdownTimer);
            currentRound++;
            nextRound();
        }
    }, 1000);
}

function selectAnswer(selectedOption, answer) {
    if (answerSubmitted) return;
    answerSubmitted = true;
    console.log('Selected option:', selectedOption);
    clearInterval(countdownTimer);
    if (selectedOption === answer) {
        score++;
    }

    document.getElementById('score').innerText = score;

    setTimeout(() => {
        currentRound++;
        if (currentRound <= totalRounds) {
            nextRound();
        } else {
            endGame();
        }
        answerSubmitted = false;
    }, 500);
}

function endGame() {
    if (score === 10) {
        postScore();
        alert("The game has ended. Your final score is: " + score);
        window.location.reload();

    }
    alert("The game has ended. Your final score is: " + score);
    window.location.reload();
}

function update_session_game() {
    return new Promise((resolve, reject) => {
        fetch('/update_session/', {
            method: 'POST', 
            headers: { 'X-CSRFToken': getCookie('csrftoken') }, 
            body: JSON.stringify({gameCompleted: true}) 
        })
        .then(response => response.json())
        .then(data => {
            if(data.error) {
                alert(data.error);
                reject(data.error);
            } else {
                console.log(data.message);
                resolve(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            reject(error);
        });
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    const csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfTokenInput) {
        const csrfToken = csrfTokenInput.value;
        // Use the csrfToken for your fetch call
    } else {
        console.error('CSRF token input not found.');
    }
});

function showRows() {
    document.getElementById("rowAsk").style.display = "flex";
    document.getElementById("rowAnswer").style.display = "flex";
    document.getElementById("showRowsButton1").style.display = "none";
    document.getElementById("showRowsButton2").style.display = "none";
    document.getElementById("colbut").style.position = "absolute";
    document.getElementById("Timebody").style.display = 'flex';
    document.getElementById("rowbut").style.display = 'none';
    document.getElementById("rowScore").style.display = "flex";
}
