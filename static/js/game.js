class Board {
  constructor(initialBoard = undefined) {
    this.board = initialBoard ? initialBoard : this.getInitialSetup();
    this.history = [];
    this.newTiles = [];
  }

  getInitialSetup() {
    return [
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ];
  }

  getAtIndex({ index }) {
    let tile_x = index % 4;
    let tile_y = Math.floor(index / 4);
    return this.board[tile_y][tile_x];
  }

  setAtIndex({ index, value }) {
    let tile_x = index % 4;
    let tile_y = Math.floor(index / 4);
    return (this.board[tile_y][tile_x] = value);
  }

  addTile({ index, value }) {
    if (this.canAddTileAt({ index })) {
      this.setAtIndex({ index, value });
      this.newTiles.push(index);
      return;
    }
    console.error("[Error] Add Tile (", index, value, ") Failed");
  }

  canAddTileAt({ index }) {
    if (index < 0 || index > 15) {
      console.error("[Error] Invalid index", index);
    }
    return this.getAtIndex({ index }) == 0;
  }

  updateBoard({ newBoard }) {
    this.history.push(this.serialize());
    this.board = newBoard;
  }

  makeMove({ direction }) {
    this.newTiles = [];
    if (this.canMove({ direction })) {
      switch (direction) {
        case "UP":
          this.moveUp();
          break;
        case "DOWN":
          this.moveDown();
          break;
        case "LEFT":
          this.moveLeft();
          break;
        case "RIGHT":
          this.moveRight();
          break;
      }
    } else {
      console.error("[Error] Invalid direction", direction);
    }
  }

  moveLeft() {
    const newBoard = [];
    for (let y = 0; y < 4; y++) {
      const row = this.board[y];
      let newRow = [];
      const nonZeroRow = row.filter((r) => r > 0).reverse();
      while (nonZeroRow.length > 1) {
        const last = nonZeroRow.pop();
        const beforeLast = nonZeroRow.pop();
        if (last === beforeLast) {
          newRow.push(last + beforeLast);
        } else {
          newRow.push(last);
          nonZeroRow.push(beforeLast);
        }
      }
      if (nonZeroRow.length) {
        newRow.push(nonZeroRow.pop());
      }
      while (newRow.length < 4) {
        newRow.push(0);
      }
      newBoard.push(newRow);
    }
    this.updateBoard({ newBoard });
  }

  moveRight() {
    const rotatedBoard = new Board(
      this.rotateBoard(this.rotateBoard(this.board))
    );
    rotatedBoard.moveLeft();

    this.updateBoard({
      newBoard: this.rotateBoard(this.rotateBoard(rotatedBoard.board)),
    });
  }

  moveDown() {
    const rotatedBoard = new Board(this.rotateBoard(this.board));
    rotatedBoard.moveLeft();

    this.updateBoard({
      newBoard: this.rotateBoard(
        this.rotateBoard(this.rotateBoard(rotatedBoard.board))
      ),
    });
  }

  moveUp() {
    const rotatedBoard = new Board(
      this.rotateBoard(this.rotateBoard(this.rotateBoard(this.board)))
    );
    rotatedBoard.moveLeft();

    this.updateBoard({
      newBoard: this.rotateBoard(rotatedBoard.board),
    });
  }

  rotateBoard(board) {
    const newBoard = [];
    for (let y = 0; y < 4; y++) {
      for (let x = 0; x < 4; x++) {
        if (!newBoard[x]) {
          newBoard[x] = [0, 0, 0, 0];
        }
        newBoard[x][y] = board[y][x];
      }
    }
    return newBoard.map((row) => row.reverse());
  }

  undoMove() {
    this.newTiles = [];
    if (this.history.length) this.board = JSON.parse(this.history.pop());
  }

  skipToEnd({ moves, indexes }) {
    for (let i = 0; i < moves.length; i++) {
      this.makeMove({ direction: moves[i] });
      this.addTile({ index: indexes[i][0], value: indexes[i][1] });
    }
  }

  skipToStart() {
    this.board = this.getInitialSetup();
    this.history = [];
  }

  canMove({ direction }) {
    if (!["UP", "DOWN", "LEFT", "RIGHT"].includes(direction)) {
      console.error("[Error] Unknown direction", direction);
      return false;
    }
    return true;
  }

  serialize() {
    return JSON.stringify(this.board);
  }

  score() {
    return this.board
      .flat()
      .reduce(
        (score, tile) => (tile ? score + tile * Math.log2(tile) : score),
        0
      );
  }

  render() {
    const targetDiv = document.getElementById("tile-container");
    targetDiv.innerHTML = "";
    console.log(this.score());
    this.board.map((row, ridx) => {
      const rowElement = document.createElement("div");
      rowElement.style.display = "flex";
      rowElement.style.width = "100%";
      rowElement.style.justifyContent = "space-between";
      rowElement.style.height = `${100 / 4.4}%`;
      rowElement.style.marginBottom = "0.8em";
      rowElement.style.position = "relative";
      row.forEach((column, cidx) => {
        const index = ridx * 4 + cidx;
        const colElement = document.createElement("div");
        colElement.innerText = column ? column : "";
        colElement.classList.add(`tile--${column ? column : 0}`);
        if (this.newTiles.includes(index)) {
          colElement.classList.add(`tile--pop`);
        }
        colElement.style.display = "flex";
        colElement.style.alignItems = "center";
        colElement.style.justifyContent = "center";
        colElement.style.fontSize = "1.8rem";
        colElement.style.width = "100%";
        colElement.style.textAlign = "center";
        colElement.style.lineHeight = "10em";
        colElement.style.borderRadius = "8px";
        colElement.style.boxShadow = "1px 1px 5px rgba(0,0,0,0.4)";
        rowElement.appendChild(colElement);
      });
      targetDiv.appendChild(rowElement);
    });

    const currentScoreDiv = document.getElementById("currentScore");
    currentScoreDiv.innerText = this.score();
  }
}

// let board = new Board();
// // board.addTile({ index: 7, value: 2 });
// // board.addTile({ index: 11, value: 2 });
// // board.addTile({ index: 9, value: 2 });
// board.addTile({ index: 12 + 0, value: 4 });
// board.addTile({ index: 12 + 1, value: 4 });
// board.addTile({ index: 12 + 2, value: 4 });
// board.addTile({ index: 12 + 3, value: 16 });
// board.render();
// board.moveLeft();
// board.render();
