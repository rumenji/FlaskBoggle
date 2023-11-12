class Game {
    constructor() {
        this.score = 0;
        this.guessed = [];
    }

    async checkGuess(guess) {
        const checkWord = await axios({
            method: 'POST',
            url: `${BASE_URL}`,
            data: {'guess': guess}
        });
        return checkWord;
    }

    checkDuplicate(guess) {
        if(this.guessed.includes(guess)) {
            return 'duplicate'
        }
        else {
            return 'not duplicate'
        }
    }

    async calculateScore() {
        if(this.guessed.length){
            this.score = this.guessed.join('').length
        }
    }

    async sendHighScore(score) {
        const newScore = await axios({
            method: 'POST',
            url: `${BASE_URL}/high_score`,
            data: {'score': score}
        })
    }
}