# King of the Hill

This project implements a playable chess variant in Python using object-oriented design. The game begins with a standard chess setup and supports legal movement for all standard pieces, while following modified win conditions:

- A player wins by **capturing the opponent’s king**
- A player also wins by moving their own king to one of the four center squares:
  - `d4`, `e4`, `d5`, or `e5`

This version intentionally excludes several standard chess rules, including:
- check / checkmate
- castling
- en passant
- pawn promotion

## Why I’m Including This Project

I’m using this project in my portfolio because it demonstrates several skills that are relevant to software development:

- designing a class-based program with clear responsibilities
- translating written requirements into working logic
- validating user input and game rules
- breaking a larger problem into helper methods
- managing application state across many conditional paths
- debugging edge cases in rule-based systems

## Technologies Used

- Python

## File

- `chess_var.py` — contains the `ChessVar` class and supporting helper function(s)

## Features

- standard 8x8 chess board stored as a nested list
- turn tracking with white moving first
- move validation for:
  - pawns
  - rooks
  - knights
  - bishops
  - queens
  - kings
- detection of captured kings
- detection of center-square win condition
- algebraic notation input such as `d2` to `d4`

## Example Usage

```python
game = ChessVar()
print(game.make_move('d2', 'd4'))
print(game.make_move('g7', 'g5'))
print(game.make_move('c1', 'g5'))
print(game.make_move('e7', 'e6'))
print(game.make_move('g5', 'd8'))
print(game.get_board())