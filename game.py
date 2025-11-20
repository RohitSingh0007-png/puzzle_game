<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2048 Game Project</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* PRANJAL'S PART: Custom CSS & Animations */
        body { font-family: 'Inter', sans-serif; touch-action: none; }
        
        .tile {
            display: flex; align-items: center; justify-content: center;
            font-weight: 900; border-radius: 0.375rem;
            font-size: 1.875rem; transition: all 0.15s ease-in-out;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Tile Colors */
        .tile-0 { background-color: #374151; }
        .tile-2 { background-color: #EEE4DA; color: #776E65; }
        .tile-4 { background-color: #EDE0C8; color: #776E65; }
        .tile-8 { background-color: #F2B179; color: #F9F6F2; }
        .tile-16 { background-color: #F59563; color: #F9F6F2; }
        .tile-32 { background-color: #F67C5F; color: #F9F6F2; }
        .tile-64 { background-color: #F65E3B; color: #F9F6F2; }
        .tile-128 { background-color: #EDCF72; color: #F9F6F2; }
        .tile-2048 { background-color: #EDC22E; color: #F9F6F2; box-shadow: 0 0 30px gold; }

        /* Animation: Pop Effect */
        .tile-new { animation: spawn 0.2s ease-out; }
        @keyframes spawn {
            0% { transform: scale(0.5); opacity: 0.5; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .hidden { display: none !important; }
    </style>
</head>
<body class="text-gray-100 p-4 bg-gray-900 min-h-screen flex flex-col items-center justify-center">

    <main id="welcome-page" class="text-center">
        <h1 class="text-5xl font-bold mb-4">2048</h1>
        <p class="mb-8 text-gray-400">Project by Pranjal & Rohit</p>
        <button id="welcome-btn" class="bg-indigo-600 px-6 py-3 rounded-lg font-bold hover:bg-indigo-500">Start Game</button>
    </main>

    <main id="game-page" class="hidden w-full max-w-md">
        <header class="flex justify-between items-center mb-4">
            <h1 class="text-4xl font-bold text-indigo-400">2048</h1>
            <div class="flex gap-2">
                <div class="bg-gray-800 p-2 rounded text-center">
                    <div class="text-xs text-gray-400">SCORE</div>
                    <div id="score" class="font-bold">0</div>
                </div>
                <div class="bg-gray-800 p-2 rounded text-center">
                    <div class="text-xs text-gray-400">BEST</div>
                    <div id="high-score" class="font-bold">0</div>
                </div>
            </div>
        </header>

        <div id="game-board" class="grid grid-cols-4 gap-3 bg-gray-800 p-3 rounded-lg aspect-square">
            </div>

        <button id="restart-btn" class="mt-4 w-full bg-indigo-600 py-2 rounded font-bold">New Game</button>
    </main>

    <script>
        // Configuration
        const SIZE = 4;
        const scoreEl = document.getElementById('score');
        const highScoreEl = document.getElementById('high-score');
        const gameBoard = document.getElementById('game-board');

        // --- ROHIT'S CORE LOGIC CLASS ---
        class Game2048 {
            constructor() {
                this.size = SIZE;
                this.score = 0;
                
                // [ROHIT]: 2D Matrix Initialization (The Database)
                this.board = Array(this.size).fill().map(() => Array(this.size).fill(0));
                
                this.init();
            }

            init() {
                this.score = 0;
                this.board = Array(this.size).fill().map(() => Array(this.size).fill(0));
                this.spawn();
                this.spawn();
                this.updateUI();
            }

            // [ROHIT]: Algorithm to Spawn Random Tiles
            spawn() {
                const empty = [];
                // Nested Loop to find empty spots
                for (let r = 0; r < this.size; r++) {
                    for (let c = 0; c < this.size; c++) {
                        if (this.board[r][c] === 0) empty.push({ r, c });
                    }
                }
                if (empty.length === 0) return;
                const { r, c } = empty[Math.floor(Math.random() * empty.length)];
                this.board[r][c] = Math.random() < 0.1 ? 4 : 2;
            }

            // [ROHIT]: Core Logic - Remove Zeros (Compression)
            compress(row) {
                const newRow = row.filter(i => i !== 0);
                while (newRow.length < this.size) newRow.push(0);
                return newRow;
            }

            // [ROHIT]: Core Logic - Merge Tiles (The Math: 2+2=4)
            merge(row) {
                for (let i = 0; i < this.size - 1; i++) {
                    if (row[i] !== 0 && row[i] === row[i + 1]) {
                        row[i] *= 2;
                        this.score += row[i];
                        row[i + 1] = 0;
                    }
                }
                return row;
            }

            // [ROHIT]: Smart Logic - Reverse Array (For Right Move)
            reverse(row) { return row.slice().reverse(); }

            // [ROHIT]: Smart Logic - Transpose Matrix (For Up/Down Moves)
            transpose() {
                const newBoard = Array(this.size).fill().map(() => Array(this.size).fill(0));
                for (let r = 0; r < this.size; r++) {
                    for (let c = 0; c < this.size; c++) {
                        newBoard[c][r] = this.board[r][c];
                    }
                }
                this.board = newBoard;
            }

            // [ROHIT]: Controller - Handling Moves
            moveLeft() {
                let moved = false;
                const newBoard = this.board.map(row => {
                    const compressed = this.compress(row);
                    const merged = this.merge(compressed);
                    const final = this.compress(merged); // Re-compress after merge
                    if (JSON.stringify(row) !== JSON.stringify(final)) moved = true;
                    return final;
                });
                this.board = newBoard;
                return moved;
            }

            moveRight() {
                this.board = this.board.map(row => this.reverse(row));
                const moved = this.moveLeft();
                this.board = this.board.map(row => this.reverse(row));
                return moved;
            }

            moveUp() {
                this.transpose();
                const moved = this.moveLeft();
                this.transpose();
                return moved;
            }

            moveDown() {
                this.transpose();
                const moved = this.moveRight();
                this.transpose();
                return moved;
            }

            handleMove(direction) {
                let moved = false;
                if (direction === 'ArrowLeft') moved = this.moveLeft();
                if (direction === 'ArrowRight') moved = this.moveRight();
                if (direction === 'ArrowUp') moved = this.moveUp();
                if (direction === 'ArrowDown') moved = this.moveDown();

                if (moved) {
                    this.spawn();
                    this.updateUI();
                    this.saveHighScore();
                }
            }

            // [ROHIT]: Persistence - LocalStorage
            saveHighScore() {
                const currentHigh = localStorage.getItem('2048-best') || 0;
                if (this.score > currentHigh) {
                    localStorage.setItem('2048-best', this.score);
                }
            }

            // [PRANJAL]: Frontend Rendering (Updating the View)
            updateUI() {
                scoreEl.innerText = this.score;
                highScoreEl.innerText = localStorage.getItem('2048-best') || 0;
                gameBoard.innerHTML = '';
                
                for (let r = 0; r < this.size; r++) {
                    for (let c = 0; c < this.size; c++) {
                        const val = this.board[r][c];
                        const tile = document.createElement('div');
                        tile.className = `tile tile-${val} ${val ? 'tile-new' : ''}`;
                        tile.innerText = val || '';
                        gameBoard.appendChild(tile);
                    }
                }
            }
        }

        // --- INITIALIZATION ---
        const game = new Game2048();

        // Event Listeners
        document.addEventListener('keydown', (e) => game.handleMove(e.key));
        
        document.getElementById('welcome-btn').addEventListener('click', () => {
            document.getElementById('welcome-page').classList.add('hidden');
            document.getElementById('game-page').classList.remove('hidden');
        });

        document.getElementById('restart-btn').addEventListener('click', () => game.init());

    </script>
</body>
</html>
