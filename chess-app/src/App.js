import logo from './logo.svg';
import { useState, useEffect } from 'react';
import './App.css';

// Empty: 0x00
// Pawn: 0x10 (black), 0x11 (white)
// Rock: 0x20 (black), 0x21 (white)
// Knight: 0x30 (black), 0x31 (white)
// Bishop: 0x40 (black), 0x41 (white)
// Queen: 0x50 (black), 0x51 (white)
// King: 0x60 (black), 0x61 (white)
function Square({ index, chessPiece, dragStart, drop }) {
  let imgSrc = "";
  switch (chessPiece) {
    case 0x10: imgSrc = "https://chessboardjs.com/img/chesspieces/wikipedia/bP.png"; break;
    case 0x20: imgSrc = "https://chessboardjs.com/img/chesspieces/wikipedia/bR.png"; break;
    case 0x30: imgSrc = "https://chessboardjs.com/img/chesspieces/wikipedia/bN.png"; break;
    case 0x40: imgSrc = "https://www.symbols.com/images/symbol/3401_black-bishop.png"; break;
    case 0x50: imgSrc = "https://chessboardjs.com/img/chesspieces/wikipedia/bQ.png"; break;
    case 0x60: imgSrc = "https://chessboardjs.com/img/chesspieces/wikipedia/bK.png"; break;

    case 0x11: imgSrc = "https://chessboardjs.com/img/chesspieces/wikipedia/wP.png"; break;
    case 0x21: imgSrc = "https://chessboardjs.com/img/chesspieces/wikipedia/wR.png"; break;
    case 0x31: imgSrc = "https://chessboardjs.com/img/chesspieces/wikipedia/wN.png"; break;
    case 0x41: imgSrc = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Chess_blt45.svg/1200px-Chess_blt45.svg.png"; break;
    case 0x51: imgSrc = "https://chessboardjs.com/img/chesspieces/wikipedia/wQ.png"; break;
    case 0x61: imgSrc = "https://chessboardjs.com/img/chesspieces/wikipedia/wK.png"; break;
  }

  const dragOver = (e) => {
    e.preventDefault();
  }

  let imgElement = "";
  if (imgSrc) {
    imgElement = <img src={imgSrc} alt={chessPiece} onDragStart={dragStart}></img>;
  }

  return (
    <div className="square" id={"s" + index} onDragOver={dragOver} onDrop={drop}>
      {imgElement}
    </div>
  );
}

function Board() {
  const [state, setState] = useState([
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  ]);

  const [moveFrom, setMoveFrom] = useState(-1);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch(`${window.location.pathname}/status`)
        .then((response) => response.json())
        .then((board) => setState(board));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const onMove = (from, to) => {
    fetch(`${window.location.pathname}/move/${from}/${to}`, { method: 'POST' })
      .then((response) => response.json())
      .then((board) => setState(board));
  }

  const dragStart = (e) => {
    let id = -1;
    if (e.target.id) {
      id = e.target.id.slice(1);
    } else {
      id = e.target.parentElement.id.slice(1);
    }

    setMoveFrom(id);
  };

  const drop = (e) => {
    e.stopPropagation();

    let id = -1;
    if (e.target.id) {
      id = e.target.id.slice(1);
    } else {
      id = e.target.parentElement.id.slice(1);
    }

    const moveTo = id;

    if (onMove) {
      onMove(moveFrom, moveTo);
    }
  }

  let content = [];
  for (let row = 0; row < 8; ++row) {
    let rowContent = [];
    for (let column = 0; column < 8; ++column) {
      const squareIndex = row * 8 + column;
      const rowElement = Square({ index: squareIndex, chessPiece: state[squareIndex], dragStart, drop });
      rowContent.push(rowElement);
    }
    const boardRow = <div className="board-row"> {rowContent} </div>;
    content.push(boardRow);
  }

  return <div className="board"> {content} </div>;
}


function App() {
  return (
    <div className="App">
      <Board />
    </div>
  );
}

export default App;
