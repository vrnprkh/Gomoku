const boardSize = 10;
const board = [];

function createBoard() {
    const gameBoard = document.getElementById('gameBoard');
    for (let i = 0; i < boardSize; i++) {
        board[i] = [];
        for (let j = 0; j < boardSize; j++) {
            board[i][j] = '';
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.addEventListener('click', () => handleCellClick(i, j));
            gameBoard.appendChild(cell);
        }
    }
}

function handleCellClick(row, col) {
    if (board[row][col] === '') {
        board[row][col] = 'played';
        const cells = document.querySelectorAll('.cell');
        const index = row * boardSize + col;
        cells[index].classList.add('played');
        checkWinner(row, col);
    }
}

function checkWinner(row, col) {
    // Add your logic to check for a win condition
    console.log(`Checking win condition for row: ${row}, col: ${col}`);
}

createBoard();
