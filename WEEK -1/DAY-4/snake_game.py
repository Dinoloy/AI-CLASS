import streamlit as st
import streamlit.components.v1 as components


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Snake Game",
    page_icon="🐍",
    layout="centered"
)


# ---------------------------------------------------------
# STREAMLIT HEADER
# ---------------------------------------------------------

st.title("🐍 Snake Game")

st.caption(
    "Use Arrow Keys or W / A / S / D to control the snake."
)


# ---------------------------------------------------------
# HTML + CSS + JAVASCRIPT GAME
# ---------------------------------------------------------

game_html = """
<!DOCTYPE html>
<html>

<head>

<style>

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        padding: 20px;

        font-family:
            Arial,
            Helvetica,
            sans-serif;

        background:
            linear-gradient(
                135deg,
                #0f172a,
                #1e293b
            );

        color: white;

        display: flex;
        justify-content: center;
        align-items: center;
    }


    .game-container {

        width: 100%;
        max-width: 620px;

        text-align: center;

        background: rgba(
            255,
            255,
            255,
            0.05
        );

        padding: 24px;

        border-radius: 20px;

        box-shadow:
            0 20px 50px
            rgba(0, 0, 0, 0.35);

        backdrop-filter: blur(10px);
    }


    h1 {
        margin-top: 0;
        margin-bottom: 10px;

        font-size: 34px;
    }


    .subtitle {
        color: #94a3b8;
        margin-bottom: 20px;
    }


    .score-board {

        display: flex;

        justify-content: space-between;

        gap: 15px;

        margin-bottom: 18px;
    }


    .score-card {

        flex: 1;

        background: #111827;

        padding: 12px;

        border-radius: 12px;

        border:
            1px solid
            rgba(255, 255, 255, 0.08);
    }


    .score-label {

        color: #94a3b8;

        font-size: 13px;
    }


    .score-value {

        margin-top: 4px;

        font-size: 26px;

        font-weight: bold;
    }


    canvas {

        width: 100%;
        max-width: 500px;

        aspect-ratio: 1 / 1;

        background: #020617;

        border-radius: 16px;

        border: 2px solid #334155;

        box-shadow:
            inset 0 0 25px
            rgba(0, 0, 0, 0.6);
    }


    .buttons {

        display: flex;

        justify-content: center;

        gap: 12px;

        margin-top: 18px;

        flex-wrap: wrap;
    }


    button {

        border: none;

        padding: 11px 20px;

        border-radius: 10px;

        cursor: pointer;

        font-size: 15px;

        font-weight: bold;

        transition: 0.2s;
    }


    button:hover {

        transform:
            translateY(-2px);
    }


    .restart {

        background: #22c55e;

        color: #052e16;
    }


    .pause {

        background: #f59e0b;

        color: #451a03;
    }


    .speed {

        margin-top: 18px;

        color: #cbd5e1;
    }


    select {

        margin-left: 8px;

        padding: 7px 10px;

        border-radius: 8px;

        background: #111827;

        color: white;

        border: 1px solid #475569;
    }


    .instructions {

        margin-top: 20px;

        padding: 14px;

        border-radius: 12px;

        background: rgba(
            15,
            23,
            42,
            0.8
        );

        color: #cbd5e1;

        line-height: 1.6;
    }


    .game-over {

        display: none;

        margin-top: 15px;

        color: #f87171;

        font-size: 20px;

        font-weight: bold;
    }


</style>

</head>


<body>


<div class="game-container">


    <h1>🐍 Snake Game</h1>

    <div class="subtitle">
        Eat the food and avoid hitting the walls or yourself.
    </div>


    <div class="score-board">

        <div class="score-card">

            <div class="score-label">
                SCORE
            </div>

            <div
                id="score"
                class="score-value"
            >
                0
            </div>

        </div>


        <div class="score-card">

            <div class="score-label">
                HIGH SCORE
            </div>

            <div
                id="highScore"
                class="score-value"
            >
                0
            </div>

        </div>

    </div>


    <canvas
        id="gameCanvas"
        width="500"
        height="500"
    ></canvas>


    <div
        id="gameOver"
        class="game-over"
    >
        Game Over! 🐍
    </div>


    <div class="buttons">

        <button
            class="restart"
            onclick="restartGame()"
        >
            🔄 Restart
        </button>


        <button
            class="pause"
            onclick="togglePause()"
            id="pauseButton"
        >
            ⏸ Pause
        </button>

    </div>


    <div class="speed">

        Speed:

        <select
            id="speedSelect"
            onchange="changeSpeed()"
        >

            <option value="180">
                Easy
            </option>

            <option
                value="120"
                selected
            >
                Normal
            </option>

            <option value="80">
                Fast
            </option>

            <option value="55">
                Extreme
            </option>

        </select>

    </div>


    <div class="instructions">

        <strong>Controls</strong>

        <br>

        ⬆ Arrow Up / W

        <br>

        ⬇ Arrow Down / S

        <br>

        ⬅ Arrow Left / A

        <br>

        ➡ Arrow Right / D

        <br><br>

        Press <strong>Space</strong>
        to pause or resume.

    </div>


</div>


<script>


// ---------------------------------------------------------
// CANVAS
// ---------------------------------------------------------

const canvas =
    document.getElementById(
        "gameCanvas"
    );

const ctx =
    canvas.getContext(
        "2d"
    );


// ---------------------------------------------------------
// GAME SETTINGS
// ---------------------------------------------------------

const tileSize = 25;

const tileCount =
    canvas.width / tileSize;


let snake;

let food;

let direction;

let nextDirection;

let score;

let highScore =
    Number(
        localStorage.getItem(
            "snakeHighScore"
        )
    ) || 0;


let gameSpeed = 120;

let gameLoop;

let paused = false;

let gameEnded = false;


// ---------------------------------------------------------
// DISPLAY HIGH SCORE
// ---------------------------------------------------------

document.getElementById(
    "highScore"
).innerText =
    highScore;


// ---------------------------------------------------------
// START / RESET GAME
// ---------------------------------------------------------

function resetState() {

    snake = [

        {
            x: 10,
            y: 10
        },

        {
            x: 9,
            y: 10
        },

        {
            x: 8,
            y: 10
        }

    ];


    direction = {
        x: 1,
        y: 0
    };


    nextDirection = {
        x: 1,
        y: 0
    };


    score = 0;

    paused = false;

    gameEnded = false;


    document.getElementById(
        "score"
    ).innerText = score;


    document.getElementById(
        "gameOver"
    ).style.display =
        "none";


    document.getElementById(
        "pauseButton"
    ).innerText =
        "⏸ Pause";


    createFood();

}


function restartGame() {

    clearInterval(
        gameLoop
    );

    resetState();

    startLoop();

}


// ---------------------------------------------------------
// FOOD
// ---------------------------------------------------------

function createFood() {

    let valid = false;


    while (!valid) {

        food = {

            x:
                Math.floor(
                    Math.random()
                    * tileCount
                ),

            y:
                Math.floor(
                    Math.random()
                    * tileCount
                )

        };


        valid =
            !snake.some(
                segment =>
                    segment.x
                        === food.x
                    &&
                    segment.y
                        === food.y
            );

    }

}


// ---------------------------------------------------------
// GAME UPDATE
// ---------------------------------------------------------

function update() {

    if (
        paused
        ||
        gameEnded
    ) {
        return;
    }


    direction =
        nextDirection;


    const head = {

        x:
            snake[0].x
            + direction.x,

        y:
            snake[0].y
            + direction.y

    };


    // -----------------------------------------------------
    // WALL COLLISION
    // -----------------------------------------------------

    if (

        head.x < 0

        ||

        head.x >= tileCount

        ||

        head.y < 0

        ||

        head.y >= tileCount

    ) {

        endGame();

        return;

    }


    // -----------------------------------------------------
    // SELF COLLISION
    // -----------------------------------------------------

    if (
        snake.some(
            segment =>
                segment.x
                    === head.x
                &&
                segment.y
                    === head.y
        )
    ) {

        endGame();

        return;

    }


    snake.unshift(
        head
    );


    // -----------------------------------------------------
    // FOOD COLLISION
    // -----------------------------------------------------

    if (

        head.x === food.x

        &&

        head.y === food.y

    ) {

        score++;

        document.getElementById(
            "score"
        ).innerText =
            score;


        if (
            score > highScore
        ) {

            highScore =
                score;


            localStorage.setItem(
                "snakeHighScore",
                highScore
            );


            document.getElementById(
                "highScore"
            ).innerText =
                highScore;

        }


        createFood();

    }

    else {

        snake.pop();

    }

}


// ---------------------------------------------------------
// DRAW GAME
// ---------------------------------------------------------

function draw() {

    // background

    ctx.fillStyle =
        "#020617";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // -----------------------------------------------------
    // GRID
    // -----------------------------------------------------

    ctx.strokeStyle =
        "#0f172a";

    ctx.lineWidth = 1;


    for (
        let i = 0;
        i <= tileCount;
        i++
    ) {

        ctx.beginPath();

        ctx.moveTo(
            i * tileSize,
            0
        );

        ctx.lineTo(
            i * tileSize,
            canvas.height
        );

        ctx.stroke();


        ctx.beginPath();

        ctx.moveTo(
            0,
            i * tileSize
        );

        ctx.lineTo(
            canvas.width,
            i * tileSize
        );

        ctx.stroke();

    }


    // -----------------------------------------------------
    // FOOD
    // -----------------------------------------------------

    const foodX =
        food.x * tileSize
        + tileSize / 2;

    const foodY =
        food.y * tileSize
        + tileSize / 2;


    ctx.fillStyle =
        "#ef4444";


    ctx.beginPath();

    ctx.arc(
        foodX,
        foodY,
        tileSize * 0.35,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // -----------------------------------------------------
    // SNAKE
    // -----------------------------------------------------

    snake.forEach(
        (
            segment,
            index
        ) => {

            const padding = 2;


            if (
                index === 0
            ) {

                ctx.fillStyle =
                    "#22c55e";

            }

            else {

                ctx.fillStyle =
                    "#16a34a";

            }


            ctx.fillRect(

                segment.x
                    * tileSize
                    + padding,

                segment.y
                    * tileSize
                    + padding,

                tileSize
                    - padding * 2,

                tileSize
                    - padding * 2

            );

        }
    );

}


// ---------------------------------------------------------
// MAIN GAME LOOP
// ---------------------------------------------------------

function gameStep() {

    update();

    draw();

}


function startLoop() {

    clearInterval(
        gameLoop
    );

    gameLoop =
        setInterval(
            gameStep,
            gameSpeed
        );

}


// ---------------------------------------------------------
// GAME OVER
// ---------------------------------------------------------

function endGame() {

    gameEnded = true;


    document.getElementById(
        "gameOver"
    ).style.display =
        "block";

}


// ---------------------------------------------------------
// PAUSE
// ---------------------------------------------------------

function togglePause() {

    if (
        gameEnded
    ) {
        return;
    }


    paused =
        !paused;


    document.getElementById(
        "pauseButton"
    ).innerText =
        paused
        ? "▶ Resume"
        : "⏸ Pause";

}


// ---------------------------------------------------------
// CHANGE SPEED
// ---------------------------------------------------------

function changeSpeed() {

    const select =
        document.getElementById(
            "speedSelect"
        );


    gameSpeed =
        Number(
            select.value
        );


    startLoop();

}


// ---------------------------------------------------------
// KEYBOARD CONTROLS
// ---------------------------------------------------------

document.addEventListener(
    "keydown",

    function(event) {

        const key =
            event.key.toLowerCase();


        // Prevent page from scrolling
        // when arrow keys are used.

        if (
            [
                "arrowup",
                "arrowdown",
                "arrowleft",
                "arrowright",
                " "
            ].includes(key)
        ) {

            event.preventDefault();

        }


        // UP

        if (
            (
                key === "arrowup"
                ||
                key === "w"
            )
            &&
            direction.y !== 1
        ) {

            nextDirection = {
                x: 0,
                y: -1
            };

        }


        // DOWN

        else if (
            (
                key === "arrowdown"
                ||
                key === "s"
            )
            &&
            direction.y !== -1
        ) {

            nextDirection = {
                x: 0,
                y: 1
            };

        }


        // LEFT

        else if (
            (
                key === "arrowleft"
                ||
                key === "a"
            )
            &&
            direction.x !== 1
        ) {

            nextDirection = {
                x: -1,
                y: 0
            };

        }


        // RIGHT

        else if (
            (
                key === "arrowright"
                ||
                key === "d"
            )
            &&
            direction.x !== -1
        ) {

            nextDirection = {
                x: 1,
                y: 0
            };

        }


        // SPACE = PAUSE

        else if (
            key === " "
        ) {

            togglePause();

        }

    }

);


// ---------------------------------------------------------
// INITIALIZE GAME
// ---------------------------------------------------------

resetState();

startLoop();

draw();


</script>


</body>

</html>
"""


# ---------------------------------------------------------
# DISPLAY GAME
# ---------------------------------------------------------

components.html(
    game_html,
    height=900,
    scrolling=False
)