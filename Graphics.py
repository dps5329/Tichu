#####################################
#Import Modules
#####################################
from Tkinter import *
from Animation import Animation
from tutorial import *
from roundHandler import *
import time
import best
import random
import copy

#####################################
#The main game class
#####################################
class CardGame(Animation):

	#####################################
	#initialize the main game variables
	#####################################
	def __init__(self):
		#call all the initialization functions
		self.initGraphicalSettings()
		self.initGeneralButtons()
		self.initHelpButtons()
		self.initSettings()
		self.initSpecialButtons()
		self.playsCount = 0
		self.tempBest = ast.literal_eval(best.best)
		self.replaceDict = best.best

	#initialize graphical values
	def initGraphicalSettings(self):
		self.gameOver = False
		self.askHighScore = False
		self.root = Tk()
		self.width = self.root.winfo_screenwidth()
		self.height = self.root.winfo_screenheight() - 100
		self.startScreen = True
		self.winningScore = 500
		self.menuArea = self.width/13.85
		self.passFont = "Arvo 30 bold"
		self.delayMessage = "The computer passes"
		self.totalPlayers = 2
		self.playerScore = 0
		self.computerScore = 0
		self.currentPlayer = 1
		self.startTime = None
		self.tableYR = self.height * (1/4.0)
		self.findHandArea()
	
	#initialize general card game buttons
	def initGeneralButtons(self):
		self.settings = False
		self.exitL = self.width/2.0-35
		self.exitT = self.height*(17/32.0)+65 
		self.exitR = self.width/2.0+35 
		self.exitB = self.height*(17/32.0)+99
		self.findPlayingArea()
		self.passL = self.pileX+self.pileW-31
		self.passT = self.pileY - 15 +(self.pileY/4)
		self.passR = self.pileX+self.pileW+59
		self.passB = self.pileY + (self.pileY/4) + 21
		self.tichuL, self.tichuT, self.tichuR, self.tichuB = self.passL +\
		 (abs(self.passL - self.passR)*2), self.passT, self.passR + \
		 (abs(self.passL - self.passR)*2), self.passB
		self.helpText = Tutor()
		self.delay = False
		self.cardImages = None
		self.gameImages = None
		self.handEndX = self.width - self.menuArea
		self.handEndY = 128 #image height
		self.cardHeight = 128

	#initialize help and stats buttons
	def initHelpButtons(self):
		self.helpPL = self.width/2.0 - 48
		self.helpPT = self.height*(14/32.0)
		self.helpPR = self.width/2.0 + 48
		self.helpPB = self.height*(14/32.0) + 34
		self.playL = self.width * (7/16.0)
		self.playT = self.height * (8/16.0)
		self.playR = self.width* (7/16.0) + 96
		self.playB = self.height* (8/16.0) + 34
		self.helpL = self.width * (7/16.0)
		self.helpT = self.height * (9/16.0)
		self.helpR = self.width* (7/16.0) + 96
		self.helpB = self.height* (9/16.0) + 34
		self.statsL = self.width * (7/16.0)
		self.statsT = self.height * (10/16.0)
		self.statsR = self.width * (7/16.0) + 96
		self.statsB = self.height * (10/16.0) + 34
		self.statsPL = self.width/2.0 - 48
		self.statsPT = self.height*(28/32.0)
		self.statsPR = self.width/2.0 + 48
		self.statsPB = self.height*(28/32.0) + 34

	#initialize settings buttons
	def initSettings(self):
		self.settingsL = self.width * (7/16.0)
		self.settingsT = self.height * (11/16.0)
		self.settingsR = self.width * (7/16.0) + 96
		self.settingsB = self.height * (11/16.0) + 34
		self.settingsSL = self.width * (7/16.0)
		self.settingsST = self.height * (5/16.0)
		self.settingsSR = self.width * (7/16.0) + 96
		self.settingsSB = self.height * (5/16.0) + 34
		self.settingsPL = self.width * (9.5/16.0)
		self.settingsPT = self.height * (5/16.0)
		self.settingsPR = self.width * (9.5/16.0) + 96
		self.settingsPB = self.height * (5/16.0) + 34
		self.settingsML = self.width * (11.1/16.0)
		self.settingsMT = self.height * (5/16.0)
		self.settingsMR = self.width * (11.1/16.0)+96
		self.settingsMB = self.height * (5/16.0)+34
		self.universalBackL = self.width * (1/32.0)
		self.universalBackT = self.height * (2/64.0)
		self.universalBackR = self.width * (1/32.0) + 96
		self.universalBackB = self.height * (2/64.0) + 34

	#initialize special game play buttons
	def initSpecialButtons(self):
		self.passingL = self.width * (7/16.0)
		self.passingT = self.height * (8/16.0)
		self.passingR = self.width*(7/16.0) + 96
		self.passingB = self.height* (8/16.0) + 34
		self.grandYL = self.width/2.0 - 108 
		self.grandYT = self.height*(11/16.0)
		self.grandYR = self.width/2.0 - 12
		self.grandYB = self.height*(11/16.0) + 34
		self.grandNL = self.width/2.0 + 12
		self.grandNT = self.height*(11/16.0)
		self.grandNR = self.width/2.0 + 108
		self.grandNB = self.height*(11/16.0) + 34
		self.enterNameL = self.width/2.0-105
		self.enterNameT = self.height*(17/32.0)+20
		self.enterNameR = self.width/2.0-5
		self.enterNameB = self.height*(17/32.0)+55
		self.noThanksL = self.width/2.0+5
		self.noThanksT = self.height*(17/32.0)+20
		self.noThanksR = self.width/2.0+105 
		self.noThanksB = self.height*(17/32.0)+55

	#create the cards dictionary and the dealing cards list
	def createCards(self):
		self.cards = {'schwj': 11, 'schwk': 13,'rot2': 2,'schwa':14,'rott':10,\
	'gruen5': 5, 'gruen4': 4, 'gruen7': 7, 'gruen6': 6, 'mahjong': 1,'gruen3':\
	3, 'gruen2': 2, 'rot6': 6, 'gruen9': 9, 'gruen8': 8, 'rot9': 9, 'rot8': 8,\
	'schwq': 12, 'blau9': 9, 'blau8': 8, 'blau5': 5, 'blau4': 4, 'blau7': 7,\
	'blau6': 6, 'rot5': 5, 'rot4': 4, 'blau3': 3, 'blau2': 2, 'gruena': 14,\
	'phoenix': 15, 'gruenk': 13, 'gruenj': 11, 'gruent': 10, 'schw8': 8,\
	'schw9': 9, 'gruenq': 12, 'schw2': 2, 'schw3': 3, 'rot7': 7, 'schw6': 6,\
	'schw7': 7, 'schw4': 4, 'schw5': 5, 'rotq': 12, 'blaut': 10, 'blauq': 12,\
	'dragon': 16, 'rotk': 13, 'rotj': 11, 'blauk': 13, 'blauj': 11,\
	'rota': 14, 'blaua': 14, 'rot3': 3, "schwt": 10} # 'dog': 0
		self.dealingCards = ['blau2','blau3','blau4','blau5','blau6','blau7',\
	'blau8','blau9','blaua','blauj','blauk','blauq','blaut','dragon',\
	'gruen2','gruen3','gruen4','gruen5','gruen6','gruen7','gruen8','gruen9',\
	'gruena', 'gruenj','gruenk','gruenq','gruent','mahjong','phoenix','rot2',\
	'rot3','rot4','rot5','rot6','rot7','rot8','rot9','rota','rotj','rotk',\
	'rotq','rott','schw2','schw3','schw4','schw5','schw6','schw7','schw8',\
	'schw9', 'schwa', 'schwj', 'schwk', 'schwq','schwt'] # 'dog'

	#change the current player
	def changePlayers(self):
		self.currentPlayer += 1
		if (self.currentPlayer > self.totalPlayers):
			self.currentPlayer = 1

	############################################
	#key pressed handler for the Animation class
	############################################
	def keyPressed(self, event):
		if self.askHighScore:
			if event.keysym == "BackSpace" and len(self.playerName) > 0:
				self.playerName = self.playerName[:len(self.playerName)-1]
			elif event.keysym.isalpha():
				self.playerName = self.playerName + event.keysym

	#gets the card based on the x and y coordinates
	def getCardLocation(self, x, y):
		cardLeft = self.cardLen
		cardBottom = self.height - self.cardHeight
		cardRight = cardLeft
		cardTop = cardBottom + 128	
		self.playerHand = sorted(self.playerHand, self.customSort)
		for i in xrange(len(self.playerHand)):
			left, right = cardLeft * i, cardRight * (i+1)
			if int(left) <= x <= int(right) and cardBottom <= y <= cardTop:
				return i
   #handles currSelection and currUp for displaying and keeping track of a play
	def cardPressed(self, cardIndex):
		if cardIndex != None:
			self.playerHand = sorted(self.playerHand, self.customSort)
			self.currUp[cardIndex] = False if self.currUp[cardIndex] == True\
			 else True
			for i in xrange(len(self.currUp)):
				if i < len(self.playerHand) and self.currUp[i] == True and\
				 self.playerHand[i] not in self.currSelection:
					self.currSelection.append(self.playerHand[i])
				elif self.currUp[i] == False:
					if i < len(self.playerHand) and self.playerHand[i] in\
					 self.currSelection:
						self.currSelection.pop\
						(self.currSelection.index(self.playerHand[i]))
	
	#checks if a press is on a players hand
	def isOnHand(self, x, y):
		if x > self.handEndX or y < self.height - self.handEndY:
			return False
		return True

	#checks if the player is intending to play the current selection
	def isPlaying(self, x, y):
		left = 0
		top = self.height*(16/32.0) - self.tableYR
		right = self.width - self.menuArea
		bottom = self.height*(16/32.0) + self.tableYR
		if left <= x <= right and top <= y <= bottom:
			return True
		return False

	#removes the cards in currSelection from the hand
	def removeCards(self):
		hand = self.playerHand
		play = self.currSelection
		for i in play:
			hand.pop(hand.index(i))

	#a custom sort for the dictionaries
	def customSort(self, item, secondItem):
		if type(item) == str and type(secondItem) == str:
			return self.cards[item] - self.cards[secondItem]
		else:
			return cmp(item, secondItem)

	#a custom sort for the dictionary keeping track of scores
	def scoreSort(self, item, secondItem):
		if type(item) == str and type(secondItem) == str:
			return self.tempBest[item] - self.tempBest[secondItem]
		else:
			return cmp(item, secondItem)

	#resets the help button location for the game
	def resetHelpForPlay(self):
		self.helpL = self.width - self.menuArea*(1/4.0) - 77
		self.helpT = self.height/2.0 - 18
		self.helpR = self.width - self.menuArea*(1/4.0) + 29
		self.helpB = self.height/2.0 + 18

	#resets the help button for the main menu
	def resetHelp(self):
		self.helpL = self.width * (7/16.0)
		self.helpT = self.height * (9/16.0)
		self.helpR = self.width* (7/16.0) + 96
		self.helpB = self.height* (9/16.0) + 34

	#handles the game over case for mousePressed
	def mouseGameOver(self, event):
		if self.width/2.0 - 80 <= event.x <= self.width/2.0 - 20 and\
		 self.height/4.0-20 <= event.y <= self.height/4.0 + 20:
			self.gameOver = False
			self.playerScore = 0
			self.computerScore = 0
			self.init()
		elif self.width/2.0 + 30 <= event.x <= self.width/2.0 + 130 and\
		 self.height/4.0-20 <= event.y <= self.height/4.0 + 20:
			self.root.quit()
			self.resetHelpForPlay()

	#handles the play button case on the main menu
	def startScreenPlay(self):
		if self.gameOver:
			self.gameOver = False
			self.playerScore = 0
			self.computerScore = 0
			self.init()
		self.startScreen = False
		self.mustPass = True
		self.resetHelpForPlay()

	#handles the entire startScreen for mousePressed
	def mouseStartScreen(self, event):
		if self.playL <= event.x <= self.playR and\
		 self.playT <= event.y <= self.playB:
			self.startScreenPlay()
		elif self.helpL <= event.x <= self.helpR and\
		 self.helpT <= event.y <= self.helpB:
			self.startScreen = False
			self.helpScreen = True
			self.resetHelpForPlay()
		elif self.statsL <= event.x <= self.statsR and\
		 self.statsT <= event.y <= self.statsB:
			self.highScores = True
			self.startScreen = False
			self.resetHelpForPlay()
		elif self.settingsL <= event.x <= self.settingsR and\
		 self.settingsT <= event.y <= self.settingsB:
			self.startScreen = False
			self.settings = True
			self.resetHelpForPlay()

	#handles all the mouse presses while in the help screen
	def mouseHelpScreen(self, event):
		if self.helpPL <= event.x <= self.helpPR and\
		 self.helpPT <= event.y <= self.helpPB:
			if self.gameOver:
				self.gameOver = False
				self.playerScore = 0
				self.computerScore = 0
				self.init()
			self.helpScreen = False
		if self.universalBackL <= event.x <= self.universalBackR and\
		 self.universalBackT <= event.y <= self.universalBackB:
			self.helpScreen = False
			self.startScreen = True
			self.resetHelp()

	#handles the enter case on the ask high score screen
	def askHighEnter(self):
		self.tempBest[self.playerName] = self.playsCount
		replace("best.py", self.replaceDict, repr(self.tempBest))
		if len(self.tempBest) > 10:
			replace("best.py", repr(self.tempBest),\
			 removeFromDict(min(self.tempBest.values()),\
			  self.tempBest))
		self.playsCount = 0
		self.highScores = True
		self.askHighScore = False

	#handles the mouse presses for the ask high score screen
	def mouseAskHighScore(self, event):
		self.grandTichu = False
		if self.enterNameL <= event.x <= self.enterNameR and\
		 self.enterNameT <= event.y <= self.enterNameB and\
		  len(self.playerName) > 0:
			self.askHighEnter()
		elif self.noThanksL <= event.x <= self.noThanksR and\
				 self.noThanksT <= event.y <= self.noThanksB:
					self.highScores = True
					self.askHighScore = False
		elif self.exitL <= event.x <= self.exitR and\
		 self.exitT <= event.y <= self.exitB:
			self.root.quit()
			self.askHighScore = False

	#handles all the mouse presses on the high score page
	def mouseHighScores(self, event):
		if self.statsPL <= event.x <= self.statsPR and self.statsPT\
		 <= event.y <= self.statsPB:
			if self.gameOver:
				self.gameOver = False
				self.playerScore = 0
				self.computerScore = 0
				self.init()
			self.highScores = False
			self.gameOver = False

		if self.universalBackL <= event.x <= self.universalBackR and\
		 self.universalBackT <= event.y <= self.universalBackB:
			self.highScores = False
			self.startScreen = True
			self.resetHelp()

	#handles the mouse presses in the settings screen
	def mouseSettings(self, event):
		if self.settingsPL <= event.x <= self.settingsPR and\
		 self.settingsPT <= event.y <= self.settingsPB:
			self.winningScore += 100

		if self.settingsML <= event.x <= self.settingsMR and\
		 self.settingsMT <= event.y <= self.settingsMB:
			self.winningScore -= 100
			if self.winningScore < 100:
				self.winningScore = 100

		if self.universalBackL <= event.x <= self.universalBackR and\
		 self.universalBackT <= event.y <= self.universalBackB:
			self.settings = False
			self.startScreen = True
			self.resetHelp()

	#handles the grand tichu mouse presses
	def mouseGrand(self, event):
		if self.grandYL <= event.x <= self.grandYR and\
		 self.grandYT <= event.y <= self.grandYB:
			self.playerGrand = True
			self.playerCanCallTichu = False
			self.initAfterGrand()

		elif self.grandNL <= event.x <= self.grandNR and\
		 self.grandNT <= event.y <= self.grandNB:
			self.initAfterGrand()

		elif self.helpL <= event.x <= self.helpR and self.helpT <= event.y\
		 <= self.helpB:
			self.helpScreen = True

	#handles the event of a player passing a card
	def passHandler(self):
		if self.currSelection[0] == "mahjong":
			self.changePlayers()
		self.singles.extend(findInCards(self.currSelection,\
		 self.cards))
		self.computerHandPile.extend(self.currSelection)
		self.playerHand.pop(self.playerHand.index\
			(self.currSelection[0]))
		cPassCard = self.findInDictionary\
		(self.computerCardSelection, False)
		self.playerHand.append(cPassCard)
		self.delayTime = 2
		self.delay = True
		self.delayMessage = "The Computer Passed You A %s" %\
		 cPassCard[len(cPassCard)-1]
		self.playerPassCard = False

	#handles the mouse presses when a player must pass a card
	def mousePassCard(self, event):
		cardIndex = None
		if (self.isOnHand(event.x, event.y)):
			cardIndex = self.getCardLocation(event.x, event.y)
			self.cardPressed(cardIndex)
		elif self.helpL <= event.x <= self.helpR and self.helpT <= event.y\
		 <= self.helpB:
			self.helpScreen = True
		elif self.isPlaying(event.y, event.y):
			if not(0 < len(self.currSelection) < 2):
				self.delay = True
				self.delayTime = 2
				self.delayMessage = "Please Select One Card To Pass"
			else:
				self.passHandler()
			self.pile = []
			self.recentPlay = None
			self.computerPile = []
			self.playerPile = []
			self.currSelection = []
			self.currentlyUp()

	#Handles the event of a player winning the round
	def mousePlayerRoundOver(self):
		self.delay = True
		self.delayMessage = "You Won The Round!"
		self.delayTime = 2
		self.roundOver = True
		self.playerScore += 100 #self.calculateScore(self.playerTakes)
		if self.playerTichu:
			self.playerScore += 100
		if self.playerGrand:
			self.playerScore += 200
		if self.computerTichu:
			self.computerScore -= 100
		if self.computerGrand:
			self.computerScore -= 200
		if self.playerScore >= self.winningScore:
			self.gameOver = True
			self.roundOver = False
			self.grandTichu = False

	#handles the event a player uses a phoenix
	def mousePhoenixHandler(self):
		self.phoenixCount = 1
		if len(self.pile) == 1:
			self.cards["phoenix"] = 0
		if len(self.currSelection) == 1:
			self.cards["phoenix"] = self.cards[self.pile[len(self.pile)-2]]

	#handles the event a player plays a legal hand
	def mousePreviousPlay(self, legal):
		if legal:
			self.playerCanCallTichu = False
			self.recentPlay = self.convertToDictionary(self.currSelection,True)
			self.pile.extend(self.recentPlay)
			if "phoenix" in self.currSelection and self.phoenixCount == 0:
				self.mousePhoenixHandler()
			self.firstPlay = False
			self.removeCards()
			self.pile = copy.deepcopy(self.currSelection)
			self.playerPile = (copy.deepcopy(self.currSelection))
			self.currSelection = []
			self.playsCount += 1
			if len(self.playerHand) == 0:
				self.mousePlayerRoundOver()
			else: 
				self.changePlayers()

	#handles the event of a player trying to play
	def mouseIsPlaying(self):
		self.playerHand = sorted(self.playerHand, self.customSort)
		legal = None
		if len(self.pile) > 0:
			if (type(self.currSelection)==list and type(self.currSelection[0])\
			 == int) or type(self.currSelection) == int:
				play = findInCards(self.currSelection)
				currPlay = self.pile
				legal = isLegalPlay(play, self.cards, self.recentPlay)
			else: 
				legal = isLegalPlay(self.currSelection,self.cards,\
					self.recentPlay)
		else:
			legal = isLegalPlay(self.currSelection, self.cards, None)
		self.mousePreviousPlay(legal)
		self.currentlyUp()
		self.currSelection = []
		return legal

	#handles the event of a player passing 
	def mousePass(self):
		self.computerTakes.extend(self.pile)
		self.pile = []
		self.recentPlay = None
		self.computerPile = []
		self.playerPile = []
		self.delay = True
		self.delayTime = 1
		self.delayMessage = "You Passed"
		self.changePlayers()

	#handles all the special screens for mousePressed
	def mouseSpecialCase(self, event):
		if self.gameOver:
			self.mouseGameOver(event)
		if self.startScreen:
			self.mouseStartScreen(event)
		elif self.helpScreen:
			self.mouseHelpScreen(event)
		elif self.askHighScore:
			self.mouseAskHighScore(event)
		elif self.highScores:
			self.mouseHighScores(event)
		elif self.settings:
			self.mouseSettings(event)
		elif self.grandTichu:
			self.mouseGrand(event)
		elif self.playerPassCard:
			self.mousePassCard(event)

	#handles a normal play in mousePressed
	def mouseNormalPlay(self, event):
		if (self.isOnHand(event.x, event.y)):
			(cardIndex) = self.getCardLocation(event.x, event.y)
			self.cardPressed(cardIndex)
		elif self.isPlaying(event.x, event.y) and\
		 len(self.currSelection) > 0:
			self.mouseIsPlaying()
		elif self.passL <= event.x <= self.passR and self.passT\
		 <= event.y <= self.passB and self.currentPlayer == 1 and\
		  len(self.pile) > 0:
			self.mousePass()
		elif self.tichuL <= event.x <= self.tichuR and self.tichuT\
		 <= event.y <= self.tichuB and self.playerCanCallTichu:
			self.playerTichu = True
			self.playerCanCallTichu = False
		if self.helpL <= event.x <= self.helpR and self.helpT <= event.y\
		 <= self.helpB:
			self.helpScreen = True

	##############################################
	#mouse pressed handler for the Animation class
	##############################################
	def mousePressed(self, event):
		if self.gameOver or self.startScreen or self.helpScreen or self.delay\
		 or self.playerPassCard or self.grandTichu or self.askHighScore or\
		  self.highScores or self.settings:
			self.mouseSpecialCase(event)
		else:
			if self.roundOver == False and self.gameOver == False and\
			 self.currentPlayer == 1:
			 	self.mouseNormalPlay(event)

	#handles the case of the computer winning a round
	def computerWonRound(self):
		self.roundOver = True
		self.delay = True
		self.delayTime = 2
		self.delayMessage = "The Computer Won The Round"
		self.computerScore += 100 #self.calculateScore(self.computerTakes)
		if self.playerTichu:
			self.playerScore -= 100
		if self.computerTichu:
			self.computerScore += 100
		if self.computerGrand:
			self.computerScore += 200
		if self.computerScore >= self.winningScore:
			self.gameOver = True
			self.delayMessage = "The Computer Won The Game"

	#handles the case of the computer playing a phoenix
	def handleComputerPhoenix():
		self.phoenixCount = 1
		if len(self.pile) == 1:
			self.cards["phoenix"] = 0
		else:
			self.cards["phoenix"] = self.cards[self.pile[len(self.pile)-2]]

	#handles retrieving the computer's move
	def timerMove(self, move):
		subtract = 1
		if type(move) == list:
			subtract = len(move)
		self.computerHand = self.computerHand[:len(self.computerHand)-subtract]
		if checkForNonEmpty(self.bombs, self.straights, self.triples,\
		 self.fullHouses, self.doubles, self.triple, self.double,\
		  self.singles) == 0:
			self.computerWonRound()
		if type(move) == list:
			self.pile.extend(move)
			self.recentPlay = self.convertToDictionary(move, False)
		else: 
			self.recentPlay = self.convertToDictionary(move, False)
			self.pile.extend(self.recentPlay)
		if "phoenix" in self.pile and self.phoenixCount == 0:
			self.handleComputerPhoenix()
		self.computerPile = self.convertToDictionary(move, True)

	#handles the normal computer move case for timerFired
	def timerNormal(self):
		currPlay = self.playerPile
		if currPlay == []:
			currPlay = None
		move = getComputerMove(self.computerHand, self.cards, self.bombs,\
		 self.straights, self.triples, self.fullHouses, self.doubles,\
		  self.triple, self.double, self.singles, len(self.playerHand),\
		   self.recentPlay)
		return currPlay, move

	#Handles the overall logistics of the computer's move
	def timerComputerMove(self):
		move = None
		if self.firstPlay == True:
			self.firstPlay = False
			move = getComputerMove(self.computerHand, self.cards, self.bombs,\
			 self.straights, self.triples, self.fullHouses, self.doubles,\
			  self.triple, self.double, self.singles, len(self.playerHand),\
			   None, True)
		else:
			currPlay, move = self.timerNormal()
		if move:
			self.timerMove(move)
		else: 
			self.playerTakes.extend(self.pile)
			self.passing = True
			self.delay = True
		self.changePlayers()

	#handles when the computer passes
	def timerComputerPass(self):
		self.computerPassCard = False
		if len(self.triple) > 0 and self.triple[0][0] < 10:
			self.computerCardSelection = self.triple[0][0]
			self.double.append(self.triple[0][1:])
			self.triple.pop(0)
		elif len(self.double) > 0 and self.double[0][0] <= 10:
			self.computerCardSelection = self.double[0][0]
			self.singles.append(self.double[0][0])
			self.double.pop(0)
		else:
			self.computerCardSelection = self.singles[1]
			self.singles.pop(1)

	#############################################
	#Time keeping handler for the Animation class
	#############################################
	def timerFired(self):
		if self.currentPlayer==2 and self.gameOver==False and self.roundOver\
		 == False and self.delay==False and self.computerPassCard==False and\
		  self.playerPassCard == False and self.grandTichu == False:
			self.timerComputerMove()
		elif self.computerPassCard:
			self.timerComputerPass()
		elif self.delay:
			if self.startTime == None:
				self.startTime = int(time.time())
			currTime = int(time.time())	
			if (currTime - self.startTime) >= self.delayTime:
				self.delayTime = 2
				self.startTime = None
				self.delayMessage = "The computer passes"
				self.delay = False
		elif self.roundOver == True:
			self.init()

	#converts a list of integers to strings based on the cards dictionary
	def convertToDictionary(self, l, remove):
		if (type(l) == list or type(l) == str) and len(l) > 0 and\
		 type(l[0]) != int:
			if type(l) == str:
				return [l]
			if type(l[0]) == str:
				return l
		if type(l) == int:
			l = [l]
		newl = []
		for i in l:
			newl.append(self.findInDictionary(i, remove))
		return newl

	#finds a value in the cards dictionary
	def findInDictionary(self, value, remove):
		cards = self.cards
		playerHand = self.playerHandPile
		computerHand = self.computerHandPile
		for i in cards:
			if (cards[i] == value) and (computerHand.count(i) == 1):
				if remove:
					return computerHand.pop(computerHand.index(i))
				return i

	#handles drawing the startScreen for redrawAll
	def drawStartScreen(self):
		self.canvas.create_image(self.width/2.0, self.height/2.0, image =\
		 self.gameImages["wood"])
		self.canvas.create_image((self.playL + self.playR)/2.0, self.height\
		 * (1/8.0), image = self.gameImages["icon"])
		self.canvas.create_image((self.playL + self.playR)/2.0, (self.playT\
		 + self.playB)/2.0, image=self.gameImages["blueButton"])
		self.canvas.create_text((self.playL + self.playR)/2.0, (self.playT\
		 + self.playB)/2.0, text = "Play", font = "Times 20 bold")
		self.canvas.create_image((self.helpL + self.helpR)/2.0, (self.helpT\
		 + self.helpB)/2.0, image=self.gameImages["blueButton"])
		self.canvas.create_text((self.helpL + self.helpR)/2.0, (self.helpT +\
		 self.helpB)/2.0, text = "Help", font = "Times 20 bold")
		self.canvas.create_image((self.statsL + self.statsR)/2.0,(self.statsT+\
		 self.statsB)/2.0, image=self.gameImages["blueButton"])
		self.canvas.create_text((self.statsL + self.statsR)/2.0, (self.statsT+\
		 self.statsB)/2.0, text = "Scores", font = "Times 20 bold")
		self.canvas.create_image((self.settingsL + self.settingsR)/2.0,(self.\
			settingsT+self.settingsB)/2.0,image=self.gameImages["blueButton"])
		self.canvas.create_text((self.settingsL + self.settingsR)/2.0, (self.\
			settingsT+self.settingsB)/2.0,text="Settings",font="Times 20 bold")

	#handles drawing the helpScreen for redrawAll
	def drawHelpScreen(self):
		self.canvas.create_image(self.width/2.0, self.height/2.0, image =\
		 self.gameImages["wood"])
		self.canvas.create_image((self.universalBackL+self.universalBackR)/2.0\
			, (self.universalBackT+self.universalBackB)/2.0,\
			 image=self.gameImages["blackButton"])
		self.canvas.create_text((self.universalBackL+self.universalBackR)/2.0,\
		 (self.universalBackT+self.universalBackB)/2.0, text="Back")
		self.canvas.create_text(self.width/2, 0, text="Tichu:", anchor=N,font=\
		 "Times 30 bold", fill="white")
		self.helpPL, self.helpPT, self.helpPR, self.helpPB = self.width*\
		(15/32.0), self.height*(30/32.0), self.width*(16.5/32), self.height*\
		(31/32.0)
		self.canvas.create_text(self.height *(2/32.0), self.height*(1.5/25.0),\
		text=self.helpText.tutorial,anchor=NW,font="Times 9 bold",fill="white")
		self.canvas.create_image((self.helpPL + self.helpPR)/2.0, (self.helpPT\
		 + self.helpPB)/2.0, image=self.gameImages["blueButton"])
		self.canvas.create_text((self.helpPL + self.helpPR)/2.0, (self.helpPT\
		 + self.helpPB)/2.0, text = "Play", font = "Times 20 bold")

	#handles drawing the settings screen for redrawAll
	def drawSettingsScore(self):
		self.canvas.create_rectangle(self.settingsSL, self.settingsST,\
		 self.settingsSR, self.settingsSB, fill="white")
		self.canvas.create_text((self.settingsSL + self.settingsSR)/2.0,\
		 (self.settingsST + self.settingsSB)/2.0, text = "%d" % \
		 self.winningScore, font="Times 18 bold")
		self.canvas.create_image((self.settingsPL + self.settingsPR)/2.0,\
		 (self.settingsPT + self.settingsPB)/2.0, image=\
		 self.gameImages["blueButton"])
		self.canvas.create_text((self.settingsPL + self.settingsPR)/2.0,\
		 (self.settingsPT + self.settingsPB)/2.0, text = "+ 100")
		self.canvas.create_image((self.settingsML + self.settingsMR)/2.0,\
		 (self.settingsMT + self.settingsMB)/2.0, image=self.gameImages\
		 ["blueButton"])
		self.canvas.create_text((self.settingsML + self.settingsMR)/2.0,\
		 (self.settingsMT + self.settingsMB)/2.0, text = "- 100")

	#draws the main initialization objects for the settings screen
	def drawSettings(self):
		self.canvas.create_image(self.width/2.0, self.height/2.0, image =\
		 self.gameImages["wood"])
		self.canvas.create_image((self.universalBackL+self.universalBackR)\
			/2.0, (self.universalBackT+self.universalBackB)/2.0, image=\
			self.gameImages["blackButton"])
		self.canvas.create_text((self.universalBackL+self.universalBackR)\
			/2.0, (self.universalBackT+self.universalBackB)/2.0, text="Back",\
			 font = "Times 12 bold")
		self.canvas.create_text((self.settingsSL + self.settingsSR)/2.0,\
		 (self.settingsST + self.settingsSB)/2.0-50, text = "Score Limit:",\
		  font = "Times 24 bold", fill="white")
		self.drawSettingsScore()

	#draws the computer's hand
	def drawComputerHand(self):
		handLen = len(self.computerHand)
		cx, cy = self.cardLen, self.cardHeight/2
		for i in xrange(0, handLen+1):
			self.canvas.create_image(i*cx + 42, cy, image=self.computerImage)

	#draws the playing pile
	def drawPile(self):
		left = self.pileX - self.pileW/2 
		top = self.pileY - self.pileH/2
		right = self.pileX + self.pileW/2 
		bottom =self.pileY + self.pileH/2
		userPile = self.playerPile
		computerPile = self.computerPile
		if computerPile != None and None not in computerPile:
			for i in xrange(len(computerPile)):
				self.canvas.create_image(left + i*self.cardLen+self.cardLen/2,\
				 self.height*.35, image=self.cardImages[computerPile[i]])
		if userPile != None:
			for i in xrange(len(userPile)):
				self.canvas.create_image(left + i*self.cardLen+self.cardLen/2,\
				 bottom - (bottom-top)/2, image=self.cardImages[userPile[i]])

	#draws the player's hand
	def drawPlayerHand(self):
		currUp = self.currUp
		hand = self.playerHand
		cx = self.cardLen
		cy = self.cardHeight/2
		hand = sorted(hand, self.customSort)
		for i in xrange(len(hand)):
			if currUp != None and currUp[i] == True:
				self.canvas.create_image(i*cx + 42, self.height - cy-self.\
					cardHeight/9.0, image=self.cardImages[hand[i]])
			elif hand[i] != None:
				self.canvas.create_image(i*cx + 42, self.height - cy, image=\
					self.cardImages[hand[i]])

	#draws the menu in the game screen
	def drawMenu(self):
		x, y = self.width - self.menuArea, self.height
		self.canvas.create_rectangle(x + x/3.0, y/2.0, x + x/3.0 +15,y/2.0+15,\
		 fill="#f7463c")
		self.canvas.create_text(x + x/3.0+7, y/2.0+7, text="Help")
		if self.playerTichu:
			self.canvas.create_text((self.helpL + self.helpR)/2.0,y*(7/10.0),\
			 text="TICHU", font = "Times 18 bold", fill="#0d4f35")
		if self.computerTichu:
			self.canvas.create_text((self.helpL + self.helpR)/2.0,y*(3/10.0),\
			 text="TICHU", font = "Times 18 bold", fill="#0d4f35")
		if self.playerGrand:
			self.canvas.create_text((self.helpL + self.helpR)/2.0,y*(7/10.0),\
			 text="GRAND", font = "Times 18 bold", fill="#FFD700")
		if self.computerGrand:
			self.canvas.create_text((self.helpL + self.helpR)/2.0,y*(3/10.0),\
			 text="GRAND", font = "Times 18 bold", fill="#FFD700")

	#draws the tichu button
	def drawTichu(self):
		left, top, right, bottom = self.tichuL, self.tichuT, self.tichuR,\
		 self.tichuB
		self.canvas.create_image((left+right)/2.0, (top+bottom)/2.0,\
		 image=self.gameImages["yellowButton"])
		self.canvas.create_text((left+right)/2.0, (top+bottom)/2.0,\
		 text = "Call Tichu", font = "Times 11")

	#draws the delay message
	def drawDelay(self):
		self.canvas.create_text(self.width/2.0, self.height/2.0 - 20, text="%s"\
		 % self.delayMessage, font = "Times 24 bold", fill="white")

	#draws the pass card objects
	def drawPassedCard(self):
		self.canvas.create_text(self.width/2.0, self.height*(5/8.0), text=\
			"Select A Card To Pass And Click On The Table", font=\
			"Times 20 bold", fill="white")
		self.drawHelp()

	#draws the grand Tichu buttons and text
	def drawGrand(self):
		self.canvas.create_text(self.width/2.0, self.height/2.0, text=\
	    "Do You Want To Call Grand Tichu?", font="Times 20 bold", fill="white")
		self.canvas.create_image((self.grandYL+self.grandYR)/2.0,(self.grandYT\
		 + self.grandYB)/2.0, image=self.gameImages["yellowButton"])
		self.canvas.create_text((self.grandYL+ self.grandYR)/2.0,(self.grandYT\
		 + self.grandYB)/2.0, text="Yes")
		self.canvas.create_image((self.grandNL+self.grandNR)/2.0,(self.grandNT\
		 + self.grandNB)/2.0, image=self.gameImages["yellowButton"])
		self.canvas.create_text((self.grandNL+ self.grandNR)/2.0,(self.grandNT\
		 + self.grandNB)/2.0, text="No")
		self.drawHelp()

	#draws user input aspect of the ask high score screen
	def askHighScoreUserInput(self):
		self.canvas.create_text((self.enterNameL+self.enterNameR)/2.0, \
			(self.enterNameT + self.enterNameB)/2.0, text="Enter", font=\
			"Times 13 bold")
		self.canvas.create_image((self.noThanksL+self.noThanksR)/2.0, (self.\
			noThanksT + self.noThanksB)/2.0, image=self.gameImages\
		["yellowButton"])
		self.canvas.create_text((self.noThanksL+self.noThanksR)/2.0, (self.\
			noThanksT + self.noThanksB)/2.0, text="No Thanks", \
		font="Times 13 bold")
		self.canvas.create_image((self.exitL+self.exitR)/2.0, (self.exitT +\
		 self.exitB)/2.0, image=self.gameImages["yellowButton"])
		self.canvas.create_text((self.exitL+self.exitR)/2.0, (self.exitT +\
		 self.exitB)/2.0, text="Exit", font="Times 13 bold")

	#draws the ask high score screen
	def drawAskHighScore(self):
		self.canvas.create_rectangle(0, 0, self.width, self.height,\
		 fill="#004c13")
		self.canvas.create_text(self.width/2.0, self.height*(14/32.0),\
		 text="You Can Be On The High Score List! Enter Your Name In The Box",\
		  font = "Times 24 bold")
		self.canvas.create_rectangle(self.width/2.0-200, self.height/2.0,\
		 self.width/2.0+200, self.height/2.0+30, fill="white")
		self.canvas.create_text(self.width/2.0, self.height/2.0 + 15, text = \
			"%s" % self.playerName, font="Times 18 bold")
		self.canvas.create_image((self.enterNameL+self.enterNameR)/2.0, \
			(self.enterNameT + self.enterNameB)/2.0, image=self.gameImages\
			["yellowButton"])
		self.askHighScoreUserInput()

	#handles drawing the basic high score screen
	def initDrawHighScores(self):
		self.canvas.create_rectangle(0, 0, self.width, self.height,\
		 fill="#004c13")
		self.canvas.create_image((self.universalBackL+self.universalBackR)/2.0\
			, (self.universalBackT+self.universalBackB)/2.0, image=self.\
			gameImages["blackButton"])
		self.canvas.create_text((self.universalBackL+self.universalBackR)/2.0,\
		 (self.universalBackT+self.universalBackB)/2.0, text="Back")
		self.canvas.create_text(self.width/2.0, self.height*(2/32.0), text=\
			"Best Players (sorted by fewest number of plays):", font =\
			 "Times 24 bold")
	
	#draws the high score screen with names and scores
	def drawHighScores(self):
		self.initDrawHighScores()
		playerX, scoreX = self.width*(10/32.0), self.width*(19/32.0)
		y = 200
		scores = self.tempBest
		scores = sorted(scores, self.scoreSort)
		for i in scores:
			self.canvas.create_text(playerX, y, text="Name: %s"%i, font =\
			 "Times 20 bold", anchor=W)
			self.canvas.create_text(scoreX, y, text="Number of Plays: %d" %\
			 self.tempBest[i], font = "Times 20 bold", anchor=W)
			y += 50
		self.canvas.create_image((self.statsPL + self.statsPR)/2.0, (\
			self.statsPT + self.statsPB)/2.0, image=self.gameImages\
		["blueButton"])
		self.canvas.create_text((self.statsPL + self.statsPR)/2.0, (\
			self.statsPT + self.statsPB)/2.0, text = "Play", font =\
			 "Times 20 bold")

	#draws the game over screen
	def redrawGameOver(self):
		if (len(self.tempBest) < 10 or self.playsCount > sorted(self.tempBest.\
			values())[0]) and len(self.playerHand) == 0:
				self.askHighScore = True
				self.drawAskHighScore()
		elif self.delay == False:
			self.canvas.create_image(self.width/2.0, self.height/2.0, image\
			 = self.gameImages["wood"])
			self.canvas.create_text(self.width/2.0, self.height/2.0, text=\
				"Game Over", font = "Times 30 bold")
			self.canvas.create_image(self.width/2.0-50, self.height/4.0, image\
				=self.gameImages["blueButton"])
			self.canvas.create_text(self.width/2.0-50, self.height/4.0, text=\
				"Reset", font="Times 14 bold")
			self.canvas.create_image(self.width/2.0+50, self.height/4.0,image=\
				self.gameImages["blueButton"])
			self.canvas.create_text(self.width/2.0+50, self.height/4.0, text=\
				"Exit", font="Times 14 bold")

	#draws the computer's pass
	def normalPassing(self):
		self.canvas.create_text(self.pileX, self.pileY - self.pileH/2.0, text=\
		 "The computer passes", font = self.passFont)
		self.passing = False
		self.pile = []
		self.recentPlay = None
		self.computerPile = []
		self.playerPile = []

	#draws the help button
	def drawHelp(self):
		self.canvas.create_image((self.helpL + self.helpR)/2.0, (self.helpT +\
		 self.helpB)/2.0, image=self.gameImages["blueButton"])
		self.canvas.create_text((self.helpL + self.helpR)/2.0, (self.helpT +\
		 self.helpB)/2.0, text = "Help!", font = "Times 18")

	#draws the right-side menu inside the game
	def normalMenu(self):
		self.drawHelp()
		if self.playerCanCallTichu == True:
			self.drawTichu()
		self.drawScores()
		self.drawPile()
		if self.delay:
			self.drawDelay()

	#draws all the main objects related to the cards
	def drawHands(self):
		if self.roundOver == False:
			self.drawComputerHand()
		self.drawMenu()
		self.drawPlayerHand()
		if self.grandTichu:
			self.drawGrand()
		elif self.playerPassCard:
			self.drawPassedCard()
		else:
			self.normalMenu()

	#draws the normal card game objects
	def redrawNormalGame(self):
		if self.passing == True:
			self.normalPassing()
		self.canvas.create_image(self.width/2.0, self.height/2.0, image =\
		 self.gameImages["wood"])
		if self.currentPlayer == 1 and self.grandTichu == False and\
		 self.playerPassCard == False and self.roundOver == False and\
		 self.delay == False:
			self.canvas.create_text(self.width/2, self.height*(3/4.0),\
			text = "Your turn", font = "Times 24 bold", fill="white")
			if self.recentPlay != None and self.recentPlay[0] != None:
				self.canvas.create_image(self.pileX+self.pileW, self.pileY+\
					(self.pileY/4.0), image=self.gameImages["yellowButton"])
				self.canvas.create_text(self.pileX+self.pileW, self.pileY+\
					(self.pileY/4.0), text = "Pass", font = "Times 18")
		self.drawHands()

	#draws the scores on the right side of the screen
	def drawScores(self):
		left, right = self.helpL, self.helpR
		self.canvas.create_text((left+right)/2.0, self.height*(13/32.0), text\
		 = "Their score: %d" % self.computerScore, font = "Times 15 bold",\
		  fill="#7a2228")
		self.canvas.create_text((left+right)/2.0, self.height * (19/32.0),text\
		="Your score: %d"%self.playerScore,font="Times 15 bold",fill="#7a2228")

	#redraws all the normal game play objects
	def redrawNormal(self):
		if self.gameOver and self.delay == False:
			self.redrawGameOver()
		else:
			self.redrawNormalGame()

	########################################
	#drawing handler for the Animation class
	########################################
	def redrawAll(self):
		if self.cardImages == None:
			self.createCardImages()
		if self.helpScreen:
			self.drawHelpScreen()
		if self.startScreen or self.helpScreen:
			if self.startScreen:
				self.drawStartScreen()
			if self.helpScreen:
				self.drawHelpScreen()
		elif self.highScores:
			self.drawHighScores()
		elif self.settings:
			self.drawSettings()
		else:
			self.redrawNormal()

	#finds the playing area
	def findPlayingArea(self):
		self.pileX = self.width/2.0
		self.pileW = self.width/5.0
		self.pileY = self.height*(2.4/4.0)
		self.pileH = self.height/5.0

	#deals the cards for grand tichu
	def dealGrand(self, players):
		cards = self.dealingCards
		random.shuffle(cards)
		currPlayer = 0
		for i in xrange(len(players) * 8 - 1):
			players[currPlayer].append(cards[i])
			currPlayer += 1
			if currPlayer >= len(players):
				currPlayer = 0
		cards = cards[len(players)*8-1:]
		self.dealingCards = cards

	#deals the rest of the cards
	def dealRest(self, players):
		cards = self.dealingCards
		random.shuffle(cards)
		currPlayer = 0
		for i in cards:
			players[currPlayer].append(i)
			currPlayer += 1
			if currPlayer >= len(players):
				currPlayer = 0

	#creates dictionaries of the necessary game images
	def createCardImages(self):
		self.cardImages = {}
		self.gameImages = {}
		self.computerImage = PhotoImage(file="cardImages/cardBack.gif") 
		for i in self.cards:
			self.cardImages[i] = PhotoImage(file="cardImages/"+i+".gif")
		self.gameImages["icon"] = PhotoImage(file="cardImages/icon.gif")
		self.gameImages["blackButton"] = PhotoImage(file="cardImages/blackButton.gif")
		self.gameImages["blueButton"] = PhotoImage(file="cardImages/blueButton.gif")
		self.gameImages["yellowButton"] = PhotoImage(file="cardImages/yellowButton.gif")
		self.gameImages["wood"] = PhotoImage(file = "cardImages/woodBack.gif")

	#decides whether the computer should call Tichu or not
	def callTichu(self, hand = None):
		if hand == None:
			hand = self.singles
		winners = 0
		for i in hand:
			if i > 13:
				winners += 1
		if winners >= 4:
			self.computerTichu = True

	#creates the bombs list for the computer's hand
	def createBombs(self):
		bombs = findListCombo(self.intComputerHand,4)
		straightBombs = findSequenceBomb(self.computerHand, self.cards)
		if bombs:
			self.bombs = bombs[0]
			self.intComputerHand = bombs[1]
		else: self.bombs = []
		if straightBombs:
			self.bombs.append(straightBombs[0])
			self.computerHand = straightBombs[1]
			self.intComputerHand = findInCards(straightBombs[1], self.cards)
			self.intComputerHand = make2D(self.intComputerHand)

	#creates the full houses and triples lists for the computer's hand
	def createFullHousesTriples(self):
		triples = findListComboSequence(self.intComputerHand, 3)
		if triples:
			self.triples = triples[0]
			self.intComputerHand = triples[1]
		else: self.triples = []
		fullHouses = findFullHouses(self.intComputerHand)
		if fullHouses:
			self.fullHouses = fullHouses[0]
			self.intComputerHand = fullHouses[1]
		else: self.fullHouses = []

	#creates the straights and doubles lists for the computer's hand
	def createStraightsDoubles(self):
		straights = findCombos(self.intComputerHand, isStraight, 5, False)
		if straights:
			self.straights = straights[0]
			self.intComputerHand = straights[1]
			if 15 in self.intComputerHand:
				self.straights[0].append(15)
				self.intComputerHand.pop(self.intComputerHand.index(15))
		else: self.straights = []
		doubles = findListComboSequence(self.intComputerHand, 2)
		if doubles:
			self.doubles = doubles[0]
			self.intComputerHand = doubles[1]
		else: self.doubles = []

	#creates the triple and double lists for the computer's hand
	def createTripleDouble(self):
		triple = findListCombo(self.intComputerHand, 3)
		if triple:
			self.triple = triple[0]
			self.intComputerHand = triple[1]
		else:
			self.triple = []
		double = findListCombo(self.intComputerHand, 2)
		if double:
			self.double = double[0]
			self.intComputerHand = double[1]
			if 15 in self.intComputerHand:
				self.double[0].append(15)
				self.triple.append(self.double.pop(0))
				self.intComputerHand.pop(self.intComputerHand.index(15))
		else: self.double = []

	#creates the singles list for the computer's hand
	def createSingles(self):
		self.singles = (copy.deepcopy(self.intComputerHand))
		if len(self.singles) < 2:
			smallest = self.double.index(min(self.double))
			self.singles.extend(self.double(smallest))
			self.double.pop(smallest)
		if 15 in self.singles:
			self.singles.sort()
			biggest = self.singles[self.singles.index(15)-1]
			self.double.append([15]+[biggest])
			self.singles.pop(self.singles.index(biggest))
			if 15 in self.singles:
				self.singles.pop(self.singles.index(15))	

	#handler for organizing the computer's hand
	def createComboLists(self):
		self.createBombs()
		self.createFullHousesTriples()
		self.createStraightsDoubles()
		self.createTripleDouble()
		self.createSingles()
		if self.computerCanCallTichu:
			self.callTichu()

	#initializes the currently up variable
	def currentlyUp(self):
		self.currUp = [False for i in xrange(len(self.playerHand))]

	#calculates the score
	def calculateScore(self, pile):
		score = 0
		pile = combinelists(pile)
		pile = findInCards(pile, self.cards)
		for i in pile:
			if i == 5:
				score += 5
			elif i == 10:
				score += 10
			elif i == 13:
				score += 10
			elif i == 15:
				score += 25
			elif i == 14:
				score -= 25
		return score

	#finds the area needed to display all the cards
	def findHandArea(self):
		width, players, cards = self.width-self.menuArea, self.totalPlayers,55
		cardsInHand = 0
		if cards%players == 0:
			cardsInHand = cards/players
		else: cardsInHand = int(cards/(players*1.0))+2
		self.cardLen = width/(cardsInHand*1.0)

	#initializes the calling Tichu variables 
	def initTichu(self):
		self.computerTakes = []
		self.playerTakes = []
		self.playerTichu = False
		self.computerTichu = False
		self.delayTime = 2
		self.grandTichu = True
		self.playerGrand = False
		self.recentPlay = None
		self.phoenixCount = 0
		self.pile = []

	#the initialization for the first deal
	def initFirstDeal(self):
		self.createCards()
		players = [[], []]
		self.dealGrand(players)
		self.playerHand = players[0]
		self.playerHand = sorted(self.playerHand, self.customSort)
		self.computerHand = players[1]
		self.playerCanCallTichu = True
		self.computerCanCallTichu = True
		self.intComputerHand = findInCards(self.computerHand, self.cards)
		self.computerGrand = False
		if self.callTichu(self.intComputerHand):
			self.computerGrand = True
			self.computerCanCallTichu = False
		self.initTichu()

	#the initialization for before grand tichu
	def initBeforeGrand(self):
		self.roundOver = False
		self.firstPlay = True
		self.mustPass = False
		self.passing = False
		self.passed = False
		self.playerPassCard = False
		self.computerPassCard = False
		self.cards["phoenix"] = 15
		self.playerPile = []
		self.computerPile = []
		self.helpScreen = False
		self.computerPile = []
		self.playerPile = []
		self.currSelection = []
		self.currentlyUp()
		self.playerName = ""
		self.highScores = False

	#initializes the second deal
	def initSecondDeal(self):
		self.grandTichu = False
		players = [self.playerHand, self.computerHand]
		self.dealRest(players)
		self.playerHandPile = self.playerHand
		self.computerHandPile = copy.deepcopy(self.computerHand)
		self.playerHand = sorted(self.playerHand, self.customSort)
		self.intComputerHand = findInCards(self.computerHand, self.cards)
	
	#initializes after grand tichu
	def initAfterGrand(self):
		self.initSecondDeal()
		aces = self.intComputerHand.count(14)
		if 'mahjong' not in self.playerHand:
			self.changePlayers()
		for i in xrange(aces):
			self.intComputerHand.pop(self.intComputerHand.index(14))
		self.intComputerHand = make2D(self.intComputerHand)
		for i in xrange(aces):
			self.intComputerHand.append(14)
		self.computerHand.pop(0)
		self.createComboLists()
		self.playerPassCard = True
		self.computerPassCard = True
		self.currentlyUp()

	####################################################################
	#initialization handler for each round called by the Animation class
	####################################################################
	def init(self):
		self.initFirstDeal()
		self.initBeforeGrand()

	#######################################
	#run function that runs the entire game
	#######################################
	def run(self):
		self.root.wm_title("Tichu")
		super(CardGame, self).run(self.root, self.width, self.height)
		