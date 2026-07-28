let questions = [];
let currentQuestion = 0;
let score = 0;

// Generate Quiz
document.getElementById("generate-btn").addEventListener("click", generateQuiz);

async function generateQuiz() {

    const topic = document.getElementById("quiz-topic").value.trim();
    const difficulty = document.getElementById("quiz-difficulty").value;

    if (!topic) {
        alert("Please enter a topic.");
        return;
    }

    document.getElementById("generate-btn").disabled = true;
    document.getElementById("generate-btn").innerText = "Generating...";

    try {

        const response = await fetch("/quiz/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: topic,
                difficulty: difficulty
            })
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            resetButton();
            return;
        }

        questions = parseQuiz(data.quiz);

        if (questions.length === 0) {
            alert("Gemini returned an invalid quiz.");
            resetButton();
            return;
        }

        currentQuestion = 0;
        score = 0;

        document.getElementById("quiz-box").style.display = "block";
        document.getElementById("result-box").style.display = "none";

        showQuestion();

    }
    catch (err) {

        console.error(err);
        alert("Error generating quiz.");

    }

    resetButton();
}

function resetButton(){

    document.getElementById("generate-btn").disabled = false;
    document.getElementById("generate-btn").innerText = "🚀 Generate AI Quiz";

}

// ----------------------
// Parse Gemini Response
// ----------------------

function parseQuiz(text){

    const quiz = [];

    const blocks = text.split("Question");

    blocks.forEach(block=>{

        if(block.trim()==="") return;

        const lines = block.trim().split("\n");

        if(lines.length<6) return;

        quiz.push({

            question: lines[0].replace(":","").trim(),

            options: [

                lines[1].replace("A.","").trim(),
                lines[2].replace("B.","").trim(),
                lines[3].replace("C.","").trim(),
                lines[4].replace("D.","").trim()

            ],

            answer: lines[5]
                .replace("Answer:","")
                .trim()
                .charAt(0)

        });

    });

    return quiz;

}

// ----------------------
// Show Question
// ----------------------

function showQuestion(){

    if(currentQuestion>=questions.length){

        finishQuiz();
        return;

    }

    const q = questions[currentQuestion];

    document.getElementById("question-title").innerHTML =
        `Question ${currentQuestion+1}<br><br>${q.question}`;

    const container = document.getElementById("options-container");

    container.innerHTML="";

    q.options.forEach((option,index)=>{

        const letter = ["A","B","C","D"][index];

        container.innerHTML += `
        <div style="margin-bottom:15px">

            <label>

                <input
                    type="radio"
                    name="answer"
                    value="${letter}"
                >

                ${letter}. ${option}

            </label>

        </div>
        `;

    });

}

// ----------------------
// Next Button
// ----------------------

document.getElementById("next-btn").addEventListener("click",()=>{

    const selected =
        document.querySelector('input[name="answer"]:checked');

    if(!selected){

        alert("Select an answer.");
        return;

    }

    if(selected.value===questions[currentQuestion].answer){

        score++;

    }

    currentQuestion++;

    showQuestion();

});

// ----------------------
// Finish
// ----------------------

async function finishQuiz(){

    document.getElementById("quiz-box").style.display="none";
    document.getElementById("result-box").style.display="block";

    const percent =
        Math.round(score/questions.length*100);

    document.getElementById("final-score").innerHTML=

        `Score : ${score}/${questions.length}<br>
         Percentage : ${percent}%`;

    // Save Result

    await fetch("/quiz/submit",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            score:score,
            total:questions.length

        })

    });

}