let board = [
  ["", "", ""],
  ["", "", ""],
  ["", "", ""],
];

let currentPlayer = "X";
let gameActive = true;

function makeMove(row, col) {
  if (!gameActive) return;

  if (board[row][col] === "") {
    board[row][col] = currentPlayer;
    document.getElementById("board").children[row * 3 + col].innerText =
      currentPlayer;

    if (checkWinner()) {
      document.getElementById("message").innerText = `${currentPlayer} wins!`;
      highlightWinner(currentPlayer);
      gameActive = false;
    } else if (checkDraw()) {
      document.getElementById("message").innerText = "It's a draw!";
      gameActive = false;
    } else {
      currentPlayer = currentPlayer === "X" ? "O" : "X";
      document.getElementById("message").innerText = `${currentPlayer}'s turn`;
    }
  }
}

function checkWinner() {
  // Check rows
  for (let i = 0; i < 3; i++) {
    if (
      board[i][0] !== "" &&
      board[i][0] === board[i][1] &&
      board[i][0] === board[i][2]
    ) {
      return true;
    }
  }
  // Check columns
  for (let i = 0; i < 3; i++) {
    if (
      board[0][i] !== "" &&
      board[0][i] === board[1][i] &&
      board[0][i] === board[2][i]
    ) {
      return true;
    }
  }
  // Check diagonals
  if (
    board[0][0] !== "" &&
    board[0][0] === board[1][1] &&
    board[0][0] === board[2][2]
  ) {
    return true;
  }
  if (
    board[0][2] !== "" &&
    board[0][2] === board[1][1] &&
    board[0][2] === board[2][0]
  ) {
    return true;
  }
  return false;
}

function checkDraw() {
  for (let row of board) {
    for (let cell of row) {
      if (cell === "") {
        return false;
      }
    }
  }
  return true;
}

function highlightWinner(player) {
  const cells = Array.from(document.getElementsByClassName("cell"));
  let playerColor = "";
  if (player === "X") {
    playerColor = "#f21717";
    cells.forEach((cell, index) => {
      const row = Math.floor(index / 3);
      const col = index % 3;
      cell.innerText = "";
      if (
        !(
          (row === 0 && col === 1) ||
          (row === 1 && (col === 0 || col === 2)) ||
          (row === 2 && col === 1)
        )
      ) {
        cell.style.backgroundColor = playerColor;
      }
    });
  } else if (player === "O") {
    playerColor = "blue";

    cells.forEach((cell, index) => {
      const row = Math.floor(index / 3);
      const col = index % 3;
      cell.innerText = "";
      if (!(row === 1 && col === 1)) {
        cell.style.backgroundColor = playerColor;
      }
    });
  }
}

function resetGame() {
  board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""],
  ];
  currentPlayer = "X";
  gameActive = true;
  document.querySelectorAll(".cell").forEach((cell) => {
    cell.innerText = "";
    cell.style.backgroundColor = "#fff";
  });
  document.getElementById("message").innerText = `${currentPlayer}'s turn`;
}
