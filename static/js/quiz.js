/**
 * quiz.js
 * -----------------------------------------------------------------------
 * Runs the quiz flow inside #quiz-container: loads questions, tracks the
 * learner's answers, scores the attempt, and submits the result.
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
        if (typeof showToast === 'function') {
            showToast('Could not load quiz questions. Please try again.', 'error');
        }
        return [];
    }
}

/**
 * Renders the current question and its available options inside #quiz-container.
 */
function renderCurrentQuestion() {
    const quizContainer = document.getElementById('quiz-container');
    if (!quizContainer) return;

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
        const optionValue = currentQuestion[optionKey];
        
        // Skip null or empty options (e.g., for true/false or 3-option questions)
        if (!optionValue) return;

        const optionButton = document.createElement('button');
        optionButton.type = 'button';
        optionButton.className = 'quiz-option';
        optionButton.textContent = optionValue;
        optionButton.addEventListener('click', () => handleAnswerSelection(optionKey));
        optionsList.appendChild(optionButton);
    });

    quizContainer.appendChild(questionProgress);
    quizContainer.appendChild(questionText);
    quizContainer.appendChild(optionsList);
}

/**
 * Records choice, updates score, and moves to the next question.
 * @param {'option_a'|'option_b'|'option_c'|'option_d'} selectedOptionKey
 */
function handleAnswerSelection(selectedOptionKey) {
    const currentQuestion = quizQuestions[currentQuestionIndex];
    
    // Normalizes comparison (in case correct_answer is 'option_a' vs 'Option_A')
    const normalizedSelected = (selectedOptionKey || '').toLowerCase();
    const normalizedCorrect = (currentQuestion.correct_answer || '').toLowerCase();
    
    const isCorrect = normalizedSelected === normalizedCorrect;

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
 * Displays the final score and submits results to Flask.
 */
async function renderQuizResults() {
    const quizContainer = document.getElementById('quiz-container');
    if (!quizContainer) return;

    const totalQuestions = quizQuestions.length;
    const scorePercentage = totalQuestions
        ? Math.round((correctAnswerCount / totalQuestions) * 100)
        : 0;

    quizContainer.innerHTML = `
        <div class="quiz-result-card">
            <h3 class="quiz-result-heading">Quiz Complete!</h3>
            <p class="quiz-result-score">You scored ${correctAnswerCount} out of ${totalQuestions} (${scorePercentage}%)</p>
            <button type="button" class="btn btn-primary" onclick="initQuizPage()">Retake Quiz</button>
        </div>
    `;

    try {
        // Direct fetch request with explicit headers for JSON payloads
        const response = await fetch('/quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                answers: learnerAnswers,
                score: scorePercentage
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned status ${response.status}`);
        }
        
        if (typeof showToast === 'function') {
            showToast('Quiz results saved successfully!', 'success');
        }
    } catch (error) {
        console.error('Error submitting quiz results:', error);
        if (typeof showToast === 'function') {
            showToast('Your score could not be saved. Check your connection.', 'error');
        }
    }
}

async function initQuizPage() {
    const quizContainer = document.getElementById('quiz-container');
    if (!quizContainer) return;

    quizQuestions = await loadQuizQuestions();
    currentQuestionIndex = 0;
    correctAnswerCount = 0;
    learnerAnswers.length = 0;

    if (!Array.isArray(quizQuestions) || quizQuestions.length === 0) {
        quizContainer.innerHTML = '<p class="quiz-empty-state">No quiz questions available right now.</p>';
        return;
    }

    renderCurrentQuestion();
}

document.addEventListener('DOMContentLoaded', initQuizPage);