/**
 * quiz.js
 * -----------------------------------------------------------------------
 * Runs the quiz flow inside #quiz-container: loads questions, tracks the
 * learner's answers, scores the attempt, and submits the result.
 *
 * DEPENDS ON (must load before this file): script.js -> fetchJson(), getEmbeddedData(), showToast()
 *
 * DATA SOURCE: embedded JSON (<script type="application/json" id="quiz-data">
 * rendered on GET /quiz) with a GET /quiz fallback. Each question matches the
 * Quiz table: { id, topic, question, option_a, option_b, option_c, option_d, correct_answer }.
 *
 * ASSUMPTION: Quiz.correct_answer stores one of the literal strings
 * "option_a" | "option_b" | "option_c" | "option_d" (i.e. it names the
 * correct column). If the models/ owner stores it differently (e.g. the
 * answer text itself), only the comparison in handleAnswerSelection() needs
 * to change.
 */

let quizQuestions = [];
let currentQuestionIndex = 0;
let correctAnswerCount = 0;
const learnerAnswers = [];

async function loadQuizQuestions() {
    const embeddedData = getEmbeddedData('quiz-data');
    if (embeddedData) {
        return embeddedData;
    }

    try {
        const quizData = await fetchJson('/quiz');
        return quizData || [];
    } catch (error) {
        console.error('Error loading quiz questions:', error);
        showToast('Could not load quiz questions. Please try again.', 'error');
        return [];
    }
}

/**
 * Renders the current question and its four options inside #quiz-container.
 */
function renderCurrentQuestion() {
    const quizContainer = document.getElementById('quiz-container');
    if (!quizContainer) {
        return;
    }

    const currentQuestion = quizQuestions[currentQuestionIndex];
    if (!currentQuestion) {
        renderQuizResults();
        return;
    }

    quizContainer.innerHTML = '';

    const questionProgress = document.createElement('p');
    questionProgress.className = 'quiz-progress';
    questionProgress.textContent = `Question ${currentQuestionIndex + 1} of ${quizQuestions.length}`;

    const questionText = document.createElement('h3');
    questionText.className = 'quiz-question';
    questionText.textContent = currentQuestion.question;

    const optionsList = document.createElement('div');
    optionsList.className = 'quiz-options';

    const optionKeys = ['option_a', 'option_b', 'option_c', 'option_d'];
    optionKeys.forEach((optionKey) => {
        const optionButton = document.createElement('button');
        optionButton.type = 'button';
        optionButton.className = 'quiz-option';
        optionButton.textContent = currentQuestion[optionKey];
        optionButton.addEventListener('click', () => handleAnswerSelection(optionKey));
        optionsList.appendChild(optionButton);
    });

    quizContainer.appendChild(questionProgress);
    quizContainer.appendChild(questionText);
    quizContainer.appendChild(optionsList);
}

/**
 * Records the learner's choice, updates the score, and advances to the next question.
 * @param {'option_a'|'option_b'|'option_c'|'option_d'} selectedOptionKey
 */
function handleAnswerSelection(selectedOptionKey) {
    const currentQuestion = quizQuestions[currentQuestionIndex];
    const isCorrect = selectedOptionKey === currentQuestion.correct_answer;

    if (isCorrect) {
        correctAnswerCount += 1;
    }

    learnerAnswers.push({
        quizId: currentQuestion.id,
        topic: currentQuestion.topic,
        selectedOption: selectedOptionKey,
        isCorrect
    });

    currentQuestionIndex += 1;
    renderCurrentQuestion();
}

/**
 * Renders the final score and submits the attempt to the backend.
 */
async function renderQuizResults() {
    const quizContainer = document.getElementById('quiz-container');
    if (!quizContainer) {
        return;
    }

    const scorePercentage = quizQuestions.length
        ? Math.round((correctAnswerCount / quizQuestions.length) * 100)
        : 0;

    quizContainer.innerHTML = '';

    const resultHeading = document.createElement('h3');
    resultHeading.className = 'quiz-result-heading';
    resultHeading.textContent = 'Quiz Complete!';

    const resultScore = document.createElement('p');
    resultScore.className = 'quiz-result-score';
    resultScore.textContent = `You scored ${correctAnswerCount} out of ${quizQuestions.length} (${scorePercentage}%)`;

    quizContainer.appendChild(resultHeading);
    quizContainer.appendChild(resultScore);

    try {
        await fetchJson('/quiz', {
            method: 'POST',
            body: { answers: learnerAnswers, score: scorePercentage }
        });
    } catch (error) {
        console.error('Error submitting quiz results:', error);
        showToast('Your score could not be saved. Check your connection.', 'error');
    }
}

async function initQuizPage() {
    const quizContainer = document.getElementById('quiz-container');
    if (!quizContainer) {
        return;
    }

    quizQuestions = await loadQuizQuestions();
    currentQuestionIndex = 0;
    correctAnswerCount = 0;
    learnerAnswers.length = 0;

    if (quizQuestions.length === 0) {
        quizContainer.innerHTML = '<p class="quiz-empty-state">No quiz questions available right now.</p>';
        return;
    }

    renderCurrentQuestion();
}

document.addEventListener('DOMContentLoaded', initQuizPage);