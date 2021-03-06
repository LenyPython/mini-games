import pygame as pg
from .constants import WIDTH, HEIGHT, RED, LORANGE, ORANGE
from .button import Button
from .ai import Player, Human, Ai

class Board:
	"""Class board for game logic"""

	def __init__(self):
		self._createBoard()
		self.turn = [Human('X'), Human('O')]
		self.buttons = [
				Button(650, 125, 'Pl', self.controlHumanX),
				Button(650, 200, 'Pl', self.controlHumanO),
				Button(800, 125, 'Ai', self.controlAiX),
				Button(800, 200, 'Ai', self.controlAiO),
				Button(650, 425, 'Reset Board', self.reset),
				Button(650, 500, 'Reset Score', self.resetScore)
				]

	def _createBoard(self):
		self.reset()
		self.resetScore()
	
	def resetScore(self):
		self.score = {'X': 0, 'O': 0}

	def reset(self):
		self.board = [[0, 0, 0],
						[0, 0, 0],
						[0, 0, 0]]
		self.left = 9
	
	def controlHumanX(self):
		self.turn[0] = Human('X')

	def controlHumanO(self):
		self.turn[1] = Human('O')
		
	def controlAiX(self):
		self.turn[0] = Ai('X')

	def controlAiO(self):
		self.turn[1] = Ai('O')
	
	def getRowCol(self, tup):
		"""gets tuple argument and returns row and col in list"""
		return tup[0] // 200, tup[1] // 200

	def placeSign(self, row, col):
		#place a sing of class Player/Human/Ai which is currently making a move
		#self.turn[i // 2 - 1].sign <=> Human.sing or Ai.sing
		self.board[row][col] = self.turn[self.left % 2 - 1].sign
		self.left -= 1

	def getMoves(self):
		'''Get empty fields from board, to allow computer player
		to know their choices'''
		return [[i,j] for i, row in enumerate(self.board) for j, val in enumerate(row) if not val]
	
	def drawButtons(self, win):
		for button in self.buttons:
			button.drawButton(win)

	def drawXO(self, win):
		'''Draws X's and O's placed in board.board'''
		for y in range(3):
			for x in range(3):
				if self.board[y][x] == 'X':
					pg.draw.line(win, LORANGE, (25 + 200 * x, 25 + 200 * y), (175 + 200 * x, 175 + 200 * y), width = 10)
					pg.draw.line(win, LORANGE, (25 + 200 * x, 175 + 200 * y), (175 + 200 * x, 25 + 200 * y), width = 10)
				elif self.board[y][x] == 'O':
					pg.draw.circle(win, LORANGE,(100 + 200 * x,100 + 200 * y), 75, width = 10)

	def drawLines(self, win):
		'''Draw board lines, creates 3 rows and cols'''
		for x in range(1,4):
			pg.draw.line(win, ORANGE, (200 * x,0), (200 * x,HEIGHT), 5)
			if x < 3:
				pg.draw.line(win, ORANGE, (0,200 * x), (600,200 * x), 5)

	def error(self, win, pos):
		'''Shows a crossed circle if clicked on closed position'''
		pg.draw.circle(win, RED, pos, 20, width=5)
		pg.draw.line(win, RED, (pos[0] - 25, pos[1] - 25), (pos[0] + 25, pos[1] + 25), width = 5)
		pg.draw.line(win, RED, (pos[0] + 25, pos[1] - 25), (pos[0] - 25, pos[1] + 25), width = 5)

	def checkWinner(self):
		for i in range(0, 3):
			if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0: return self.board[0][i]
			if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0: return self.board[i][0]
		if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0: return self.board[2][2]
		elif self.board[0][2] == self.board[1][1] == self.board[2][0] != 0: return self.board[2][0]

	def addScore(self, winner):
		self.score[winner] += 1
