const wordGuessForm = document.getElementById('word-guess-form');
const wordInput = document.getElementById('word');
const wordResult = document.getElementById('word-result');
const currentScore = document.getElementById('current-score');
const timerElement = document.getElementById('timer'); 
const submitButton = document.getElementById('submit-button');

let score = 0;
let highscore = 0;
const words = new Set();
let secondsLeft = 60; 

function updateTimer() {
  timerElement.textContent = `Time Left: ${secondsLeft} seconds`; 
}

function startTimer() {
  const timerInterval = setInterval(() => {

    if(secondsLeft <= 0) {
      //Disable game features when time is up
      clearInterval(timerInterval);
      wordInput.disabled = true; 
      submitButton.disabled = true; 
    } else {
      secondsLeft--;
      updateTimer()
    }
  }, 1000); 
}

startTimer(); 

wordGuessForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const word = wordInput.value.trim();

  if (word) {
    axios.post('/check-word', { word })
    .then((response) => {
      const result = response.data.result;
      if (result === 'ok') {
          words.add(word);
      }
      wordResult.textContent = 'Result: ' + (response.data.result);
      currentScore.textContent = "" + response.data.score;
    })  
  }
});

