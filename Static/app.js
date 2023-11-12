const $guessForm = $('#guess-form');
const $input = $('#guess');
const $submit = $('#submit-guess');
const $score = $('#score');
const BASE_URL = 'http://127.0.0.1:5000';

$guessForm.on('submit', submitGuess);

async function submitGuess(evt) {
    evt.preventDefault();
    const guess = $input.val();
    const checkDuplicate = game.checkDuplicate(guess);
    if(checkDuplicate === 'not duplicate'){
        const checkWord = await game.checkGuess(guess);
        return displayResult(checkWord.data, guess);
    }
    else {
        return displayResult(checkDuplicate);
    }
    
    
}

function displayResult(resultGuess, guess) {
    $('.result').remove();
    console.log(`Result: ${resultGuess}`)
    if (resultGuess === 'not-on-board') {
        $guessForm.prepend('<p class="result warning">The word is not on the board!<p>')
    }
    else if (resultGuess === 'not-word') {
        $guessForm.prepend('<p class="result error">This is not a word!<p>')
    }
    else if (resultGuess === 'duplicate') {
        $guessForm.prepend('<p class="result warning">You have already guessed the word!<p>')
    }
    else {
        game.guessed.push(guess)
        game.calculateScore();
        $score.text(`Score: ${game.score}`)
        $guessForm.prepend('<p class="result success">You have guessed correctly!<p>')
    }
}

$(document).ready(function(){
    game = new Game();
    $score.text(`Score: 0`)
    const timeOut = setTimeout(function(){
        $submit.prop('disabled', true);
        game.sendHighScore(game.score);
        $guessForm.prepend('<p class="result error">Time is out!<p>')

    }, 60000) 
})