#######################################
#import modules
#######################################
import random
import copy
from tempfile import mkstemp
from shutil import move
from os import remove, close
import ast

#Copied from stackoverflow: 
#http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file
#-in-python
def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file_path)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

#removes a value from a dictionary
def removeFromDict(value, dict):
	for i in dict:
		if dict[i] == value:
			del dict[i]
			return dict

# Finds the value of each card by referring to the card dictionary
def findInCards(attemptedPlay, cards):
	cardValues = []
	for i in attemptedPlay:
		if type(i) == str:
			cardValues.append(cards[i])
		else:
			cardValues.append(i)
	return cardValues 

#checks if a comination is a pair
def isDouble(combination):
	combination = copy.deepcopy(combination)
	if len(combination) < 2: return False
	combination = copy.deepcopy(combination)
	#check if a phoenix is in the combination
	if 15 in combination:
		combination[combination.index(15)] = min(combination)
	return max(combination) == min(combination) and len(combination) == 2

#makes the phoenix the appropriate value in a combination
def makePhoenixLowest(combination, length):
	index = combination.index(15)
	for i in combination:
		if combination.count(i) < length and i != 15:
			combination[index] = i
	combination.sort()

#returns the correct value for the phoenix in a run
def changePhoenixInRun(combination, cards):
	combination = copy.deepcopy(combination)
	combination = findInCards(combination, cards)
	value = 0
	check = 0
	counter = min(combination)
	combination.pop(combination.index(15))
	for i in combination:
		if i != counter:
			check = 1
			value = counter
			counter += 1
		counter += 1
	if check == 0:
		if max(combination) == 14:
			return min(comination) - 1
		return max(combination) + 1
	return value

#checks if a combination is a pair sequence
def isPairSequence(combination):
	combination = copy.deepcopy(combination)
	if len(combination)%2 == 1 or len(combination) < 4: return False
	currValue = combination[0]
	if 15 in combination:
		makePhoenixLowest(combination, 2)
	for i in xrange(len(combination)):
		#every other one
		if i%2 == 0:
			if not isDouble([combination[i]]+[combination[i+1]]) or\
			combination[i] != currValue:
				return False
			currValue += 1
	return True

#checks if a combination is a triple
def isTrio(combination):
	combination = copy.deepcopy(combination)
	if len(combination) < 3: return False
	combination = copy.deepcopy(combination)
	if 15 in combination:
		combination[combination.index(15)] = min(combination)
	return max(combination) == min(combination) and len(combination) == 3

#checks if a combination is a triple sequence
def isTrioSequence(combination):
	combination = copy.deepcopy(combination)
	if len(combination)%3 != 0 or len(combination) < 6: return False
	currValue = combination[0]
	if 15 in combination:
		makePhoenixLowest(combination, 3)
	for i in xrange(len(combination)):
		#every third item
		if i%3 == 0:
			if not isTrio([combination[i]]+[combination[i+1]]+\
				[combination[i+2]]) or combination[i] != currValue:
				return False
			currValue += 1
	return True

#handles a full house with a phoenix
def fullHouseWithPhoenix(combination):
	combination.pop(combination.index(15))
	if min(combination) == max(combination): return False
	#three possibilities
	if (combination.count(min(combination)) == 1 and\
	 combination.count(max(combination)) == 3):
		combination.append(15)
		return True
	elif (combination.count(min(combination)) == 3 and\
	 combination.count(max(combination)) == 1):
		combination.append(15)
		return True
	elif (combination.count(max(combination)) == \
		combination.count(min(combination)) == 2):
		combination.append(15)
		return True
	return False

#checks if a combination is a full house
def isFullHouse(combination):
	combination = copy.deepcopy(combination)
	if len(combination) != 5: return False
	hasPheonix = 15 in combination
	if hasPheonix:
		return fullHouseWithPhoenix(combination)
	else:
		return combination.count(min(combination)) == 2 and \
		 combination.count(max(combination)) == 3 or combination.count\
		 (min(combination)) == 3 and combination.count(max(combination)) == 2

#checks if a combination is a straight
def isStraight(combination):
	combination = copy.deepcopy(combination)
	if len(combination) < 5:
		return False
	currElement = combination[0]
	pheonixUse = 0
	hasPheonix = 15 in combination
	if hasPheonix:
		combination.pop(combination.index(15))
	#cant have the dragon in a straight
	if 16 in combination: return False
	for i in combination:
		if i != currElement:
			if not hasPheonix or pheonixUse == 1 or i != currElement + 1:
				return False
			else:
				currElement += 1 
				pheonixUse = 1
		currElement += 1
	return True

#makes sure the play matches the previous play
def comboMatches(play, currPlay):
	if currPlay == None: currPlay = play
	if isDouble(currPlay):
		return isDouble(play)
	elif isPairSequence(currPlay):
		return isPairSequence(play)
	elif isTrio(currPlay):
		return isTrio(play)
	elif isTrioSequence(currPlay):
		return isTrioSequence(play)
	elif isFullHouse(currPlay):
		if isFullHouse(play):
			return "full"
		return False
	elif isStraight(currPlay):
		return isStraight(play)
	else:
		return len(play) == 1

#checks if the selection is a bomb
def isBomb(play, cards):
	if len(play) < 4 or type(play[0]) == None: return False
	intHand = findInCards(play, cards)
	intHand.sort()
	if len(play) == 4:
		return min(intHand) == max(intHand)
	suit = play[0][:2]
	for i in play:
		if i[:2] != suit:
			return False
	return isStraight(intHand)

#handles the returns in complies with rules
def rulesReturnHandler(attemptedCombo,attemptedPlay,currPlayInt,currPlay,play):
	if attemptedCombo == False or attemptedPlay == None:
		return False
	if currPlay == None:
		return attemptedCombo
	elif attemptedCombo == "full":
		mustBeat = max(currPlayInt)
		if currPlayInt.count(min(currPlayInt)) == 3:
			mustBeat = min(currPlayInt)
		if play.count(min(play)) == 3: return min(play) > mustBeat
		else: return max(play) > mustBeat 
	if len(play) == 1:	
		return min(play) > max(currPlayInt)
	return min(play) > min(currPlayInt)


#checks if an attempted play complies with the rules
def compliesWithRules(attemptedPlay, cards, currPlay):
	play = findInCards(attemptedPlay, cards)
	currPlayInt = currPlay
	if currPlay != None and type(currPlayInt[0]) == str:
		currPlayInt = findInCards(currPlay, cards)
	if currPlay == None and isBomb(attemptedPlay, cards):
		return True
	elif currPlay != None and isBomb(currPlay, cards):
		return isBomb(attemptedPlay, cards) and min(play) > min(currPlayInt)
	elif isBomb(attemptedPlay, cards):
		return True
	play.sort()
	attemptedCombo = comboMatches(play, currPlayInt)
	return rulesReturnHandler(attemptedCombo,attemptedPlay,currPlayInt,\
	currPlay,play)
	
#####################################
#checks if an attempted play is legal
#####################################
def isLegalPlay(attemptedPlay, cards, currPlay=None):
	#checks if the attempted play complies with the rules
	if currPlay == None or currPlay[0] == None:
		currPlay = None
	if compliesWithRules(attemptedPlay, cards, currPlay):
		return True
	else:
		return False

#makes a list 2d, putting together same values 
def make2D(l):
	subList = []
	previousVals = []
	newL = []
	l.sort()
	for i in xrange(len(l)):
		if l.count(l[i]) > 1 and l[i] not in previousVals:
			previousVals.append(l[i])
			j = i
			while j < len(l) and l[j] == l[i]:
				subList.append(l[j])
				j+=1
			if len(subList) > 1: newL.append(subList)
			subList = []
		elif l[i] not in previousVals: newL.append(l[i])
	return newL

#makes a 2d list a 1d list
def removeLists(l):
	lists = []
	newList = copy.deepcopy(l)
	for i in xrange(len(l)):
		if type(l[i]) == list:
			newList.pop(i-len(lists))
			lists.append(l[i])
	if len(lists) == 0: return False
	return lists, newList

#handles the combinations
def comboHandler(newHand, i, endIndex, currCombos):
	hasList = checkFor2D(newHand[i:endIndex])
	if hasList:
		hasList.append(endIndex)
		currStart = i
		for j in hasList:
			if j - currStart >= 5: currCombos.append(newHand[currStart:j])
			currStart = j+1
	else: currCombos.append(newHand[i:endIndex])

#removes an item from the currentCombos
def removeItems(hand, currCombos):
	hand, currCombos
	for i in xrange(len(currCombos)):
		for j in xrange(len(currCombos[i])):
			hand.pop(hand.index(currCombos[i][j]))

#recursive combo checking, used for straights
def checkCombo(f, play, endIndex, minLen, additionalArg = None):
	check = None
	if additionalArg != None:
		check = f(play, additionalArg)
	else: check = f(play)
	if len(play) < minLen:
		return False
	elif check:
		return play, endIndex
	else:
		return checkCombo(f, play[:endIndex-1],endIndex-1,minLen,additionalArg)

#handles returning from findCombos
def findCombosReturnHandler(currCombos, newHand, removedLists):
	if len(currCombos) == 0: return False
	removeItems(newHand, currCombos)
	for i in removedLists:
		newHand.append(i)
	return currCombos, newHand

#finds a specific kind of combo from a hand
def findCombos(hand, f, minLen, lookingInList, additionalArg=None,\
 optionalFunction = None):
	currCombos = []
	removedLists = []
	if not lookingInList:
		check = removeLists(hand)
		if check:
			removedLists, hand = check
	if optionalFunction != None:
		hand = optionalFunction(hand)
	newHand = copy.deepcopy(hand)
	startIndex = 0
	while startIndex <= len(hand)-minLen:
		endIndex = len(hand)
		check = checkCombo(f, hand[startIndex:endIndex], endIndex, minLen,\
		 additionalArg)
		if check != False:
			currCombos.append(check[0])
			startIndex = check[1]
		else: startIndex += 1
	return findCombosReturnHandler(currCombos, newHand, removedLists)

#finds combos involving the 2d lists inside the hand
def findListCombo(hand, length):
	newHand = copy.deepcopy(hand)
	check = removeLists(newHand)
	if check != False:
		removedLists, newHand = check
	else: return False
	combos = []
	for i in removedLists:
		if len(i) == length:
			combos.append(i)
	if len(combos) == 0: return False
	for i in combos:
		removedLists.pop(removedLists.index(i))
	newHand.extend(removedLists)
	return combos, newHand

#handles returning from findFullHouses
def findFullHousesReturnHandler(combos, removedLists, newHand):
	if len(combos) == 0: return False
	combos = combinelists(combos)
	combos = make2D(combos)
	for i in combos:
		removedLists.pop(removedLists.index(i))
	newCombos = []
	for i in xrange(len(combos)):
		if i%2 == 0:
			newCombos.append(combos[i]+combos[i+1])
	combos = newCombos
	newHand.extend(removedLists)
	return combos, newHand

#finds the full houses inside a hand
def findFullHouses(hand):
	newHand = copy.deepcopy(hand)
	check = removeLists(newHand)
	if check != False:
		removedLists, newHand = check
	else: return False
	combos = []
	for i in xrange(len(removedLists)):
		if i % 2 == 0 and i+1 < len(removedLists):
			if isFullHouse(removedLists[i]+removedLists[i+1]):
				combos.append(removedLists[i]+removedLists[i+1])
	return findFullHousesReturnHandler(combos, removedLists, newHand)

#finds all the sequence bombs
def findSequenceBomb(hand, cards):
	combos = []
	hand = copy.deepcopy(hand)
	for i in xrange(len(hand)):
		if i % 5 == 0:
			if isBomb(hand[i:i+4], cards):
				combos.append(hand[i:i+4], cards)
	if len(combos) == 0: return False
	for i in combos:
		for j in i:
			hand.pop(hand.index(j))
	return combos, hand

#combines the lists inside a list
def combinelists(l):
	newL = []
	for i in l:
		if type(i) == list:
			newL.extend(i)
		else: newL.append(i)
	return newL

#handles returning from findListComboSequence
def findListComboSequenceReturnHandler(combos, removedLists, newHand):
	if len(combos) == 0: return False
	combos = combinelists(combos)
	combos = make2D(combos)
	for i in combos:
		removedLists.pop(removedLists.index(i))
	newCombos = []
	for i in xrange(len(combos)):
		newCombos.extend(combos[i])
	combos = [newCombos]
	newHand.extend(removedLists)
	return combos, newHand

#finds a specific combination from the lists inside a hand
def findListComboSequence(hand, length):
	newHand = copy.deepcopy(hand)
	check = removeLists(newHand)
	if check != False:
		removedLists, newHand = check
	else: return False
	combos = []
	counter = removedLists[0][0]
	currSequence = []
	for i in removedLists:
		if len(i) == length and i[0] == counter:
			currSequence.extend(i)
		else:
			if len(currSequence) >= length*2:
				combos.append(currSequence)
			currSequence = []
			counter = (i[0])
		#must be incrementing values
		counter += 1
	return findListComboSequenceReturnHandler(combos, removedLists, newHand)

#merges the lists inside a list
def mergeLists(l):
	newL = []
	counter = 0
	for i in l:
		if type(i) == list:
			counter += 1
			for j in i:
				newL.append(j)
		else: newL.append(i)
	return newL

#finds the winds inside a hand
def findWins(hand, cards):
	if type(hand[0]) != int:
		hand = findInCards(hand, cards)
	wins = 0
	wins += hand.count(16)
	wins += hand.count(15)
	wins += hand.count(14)
	kings = hand.count(13) - (4 - hand.count(14))
	wins += kings
	queens = hand.count(12) - (4 - kings)
	return wins

#finds the best move based on a hand
def bestMove(play, hand, playLen):
	currPlay = []
	for i in xrange(len(hand)):
		if type(hand[i]) == list:
			if hand[i][0] > play[0] and len(hand[i]) == len(play):
				currPlay.append(i)
		else:  
			if hand[i] > play[0]:
				currPlay.append(i)
	if len(currPlay) == 0: return -1
	if type(play[0]) == list:
		if len(play[currPlay[0]]) != len(play): return -1
	if playLen < 10:
		return currPlay[int(len(currPlay)/2.0)]
	return currPlay[0]

#checks for valid plays inside a list based on a given value
def checkInComboList(i, combo, value, comboWithLowest, place):
	if min(combo[i]) > value:
		if len(comboWithLowest) == 0:
			comboWithLowest = combo[i]
			place = i
		low = min(comboWithLowest)
		currLow = min(combo[i])
		if currLow < low:
			comboWithLowest = combo[i]
			place = i
	return comboWithLowest, place

#checks for valid plays inside a combo
def checkInCombo(combo, value):
	place = 0
	comboWithLowest = []
	smallest = 0
	for i in xrange(len(combo)):
		if type(combo[i]) == list:
			comboWithLowest, place = checkInComboList(i, combo, value,\
			comboWithLowest, place)
		else:
			if value < combo[i]:
				if smallest == 0:
					smallest = combo[i]
					place = i
				elif combo[i] < smallest:
					smallest = combo[i]
					place = i
	if smallest != 0:
		return smallest, place
	elif len(comboWithLowest) > 0:
		return comboWithLowest
	return False

#breaks up double or doubles combinations
def breakUpDoubleCombos(doubles, double, singles):
	checkDoubles = checkInCombo(doubles,singles)
	if checkDoubles:
		i = checkDoubles[1]
		singles.extend(doubles[index])
		doubles.pop(index)
		return checkDoubles[0]
	
	checkDouble = checkInCombo(double, singles)
	if checkDouble:
		i = checkDouble[1]
		singles.extend(double[index])
		double.pop(index)
		return checkDouble[0]
	return False

#breaks up triple or triples combinations
def breakUpTripleCombos(triples, triple, singles):
	checkTriples = checkInCombo(triples,singles)
	if checkTriples:
		i = checkTriples[1]
		singles.extend(triples[index])
		triples.pop(index)
		return checkTriples[0]

	checkTriple = checkInCombo(triple,singles)
	if checkTriple:
		i = checkTriple[1]
		singles.extend(triple[index])
		triple.pop(index)
		return checkTriple[0]
	return False

#breaks up a combination from all the combos
def breakUpCombo(value, triples, fullHouses, doubles, triple, double, singles):
	checkFullHouses = checkInCombo(fullHouses,singles)
	if checkFullHouses:
		i = checkFullHouses[1]
		#fullHouses[i].pop(fullHouses[i].index(small))
		singles.extend(fullHouses[index])
		fullHouses.pop(index)
		return checkFullHouses[0]
	tri = breakUpTripleCombos(triples, triple, singles)
	if tri != False:
		return tri

	duo = breakUpDoubleCombos(doubles, double, singles)
	if duo != False:
		return duo

#finds the lowest from all the list combos
def findLowestFromLists(triples,fullHouses,doubles,triple,double,singles,\
	lowestVals):
	smallest = min(lowestVals)
	for combo in [triples, fullHouses, doubles, triple, double, singles]:
		if smallest in combo:
			i = combo.index(smallest)
			combo.pop(i)
			return smallest
		if smallest[0] in combo:
			i = combo.index(smallest[0])
			combo.pop(i)
			return smallest[0]

#finds the lowest from all the combinations
def findLowest(bombs, triples, fullHouses, doubles, triple, double, singles):
	triplesLowest = checkInCombo(triples, 1)
	fullHousesLowest = checkInCombo(fullHouses, 1)
	doublesLowest = checkInCombo(doubles, 1)
	tripleLowest = checkInCombo(triple, 1)
	doubleLowest = checkInCombo(double, 1)
	singlesLowest = checkInCombo(singles, 1)
	if singlesLowest:
		singlesLowest = [singlesLowest[0]]
	lowestVals = [triplesLowest, fullHousesLowest, doublesLowest,tripleLowest,\
	doubleLowest, singlesLowest]
	false = lowestVals.count(False)
	for i in xrange(false):
		lowestVals.pop(lowestVals.index(False))
	if len(lowestVals) == 0: 
		if len(bombs) > 0:
			return bombs.pop(0)
		return False
	return findLowestFromLists(triples, fullHouses, doubles, triple, double,\
	singles, lowestVals)

#makes sure the combinations are not empty
def checkForNonEmpty(bombs, straights, triples, fullHouses, doubles, triple,\
 double, singles):
	nonEmpty = 0
	if len(bombs)  > 0:
		nonEmpty += 1
	if len(straights)  > 0:
		nonEmpty += 1
	if len(triples)  > 0:
		nonEmpty += 1
	if len(fullHouses)  > 0:
		nonEmpty += 1
	if len(doubles)  > 0:
		nonEmpty += 1
	if len(triple)  > 0:
		nonEmpty += 1
	if len(double)  > 0:
		nonEmpty += 1
	if len(singles)  > 0:
		nonEmpty += 1
	return nonEmpty

#finds the loest and best in a combination
def findLowestAndBest(otherHandLen, combo):
	if otherHandLen < 10:
			return combo.pop(int(len(triples)/2.0))
	return combo.pop(0)

#finds the lowest and best from the singles
def lowestAndBestInSingles(triple, otherHandLen, singles, hand, bombs):
	if len(triple) > 0 and otherHandLen < 10:
		return triple.pop(int(len(singles)/2.0))
	elif len(singles)>0: return singles.pop(0)
	else: 
		if len(hand) <=  4*len(bombs) and len(bombs) > 0:
			return bombs.pop(0)
		return False

#finds the best play without a previous play
def bestWithoutCurrPlay(bombs, straights, triples, fullHouses, doubles,\
 triple, double, singles, hand, otherHandLen):
	if checkForNonEmpty(bombs, straights, triples, fullHouses, doubles,\
	 triple, double, singles) > 1:
		return findLowest(bombs, triples, fullHouses, doubles, triple,\
		 double, singles)
	elif len(triples) > 0:
		return findLowestAndBest(otherHandLen, triples)
	elif len(fullHouses) > 0:
		return findLowestAndBest(otherHandLen, fullHouses)
	elif len(straights) > 0:
		return findLowestAndBest(otherHandLen, straights)
	elif len(doubles) > 0:
		return findLowestAndBest(otherHandLen, doubles)
	elif len(triple) > 0:
		return findLowestAndBest(otherHandLen, triple)
	elif len(double) > 0:
		return findLowestAndBest(otherHandLen, double)
	else:
		return lowestAndBestInSingles(triple, otherHandLen, singles,hand,bombs)

#finds the best inside a specific combination
def findBestInCombo(currPlay, combo, otherHandLen):
	best = bestMove(currPlay, combo, otherHandLen)
	if len(combo) > 0 and best != -1:
		return combo.pop(best)
	return False

#finds the best inside singles
def bestInSingles(currPlay, singles, triples, fullHouses, doubles, triple,\
 double, bombs, otherHandLen, hand):
	best = bestMove(currPlay, singles, otherHandLen)
	if len(singles)>0 and best != -1: 
		if singles[best] < 14 and otherHandLen > 15:
			return singles.pop(best)
		elif otherHandLen < 15:
			return singles.pop(best)
		if otherHandLen < len(hand) - 5:
			return breakUpCombo(currPlay, triples, fullHouses, doubles,\
			 triple, double, singles)
	if len(singles) == 0 and len(bombs) > 0:
		return bombs.pop(0)
	return False

#finds the best with a previous play
def bestWithCurrPlay(bombs, straights, triples, fullHouses, doubles, triple,\
 double, singles, otherHandLen, currPlay, hand):
	if otherHandLen < 6 and len(bombs) > 0:
		return bombs.pop(0)
	if isStraight(currPlay):
		return findBestInCombo(currPlay, straights, otherHandLen)
	elif isFullHouse(currPlay):
		return findBestInCombo(currPlay, fullHouses, otherHandLen)
	elif isTrioSequence(currPlay):
		return findBestInCombo(currPlay, triples, otherHandLen)
	elif isPairSequence(currPlay):
		return findBestInCombo(currPlay, doubles, otherHandLen)
	elif isTrio(currPlay):
		return findBestInCombo(currPlay, triple, otherHandLen)
	elif isDouble(currPlay):
		return findBestInCombo(currPlay, double, otherHandLen)
	else:
		return bestInSingles(currPlay,singles,triples,fullHouses,doubles,\
		triple, double, bombs, otherHandLen, hand)

#finds the computer's best play
def findBestPlay(hand, cards, bombs, straights, triples, fullHouses, doubles,\
 triple, double, singles, otherHandLen, currPlay=None):
	currentCombo = []
	if currPlay == None:
		return bestWithoutCurrPlay(bombs, straights, triples, fullHouses,\
		 doubles, triple, double, singles, hand, otherHandLen)

	else:
		return bestWithCurrPlay(bombs, straights, triples, fullHouses,\
		 doubles, triple, double, singles, otherHandLen, currPlay, hand)
		
#finds the computer move with a previous move
def findComputerMoveWithMove(hand, currPlay, cards, bombs, straights, triples,\
 fullHouses, doubles, triple, double, singles, otherHandLen):
	if isBomb(currPlay, cards):
		if len(bombs) == 0:
			return False
		else:
			mustBeat = findInCards(currPlay, cards)
			for i in bombs:
				if i[0] > mustBeat:
					return bombs.pop(bombs.index(i))
			return False
	currPlay = findInCards(currPlay, cards)
	currPlay.sort()
	play = findBestPlay(hand, cards, bombs, straights, triples,\
	 fullHouses, doubles, triple, double, singles, otherHandLen, currPlay)
	return play

###################################
#gets the computer's move
###################################
def getComputerMove(hand, cards, bombs, straights, triples, fullHouses,\
 doubles,triple,double,singles,otherHandLen,currPlay=None,firstPlay=False):
	if firstPlay == True:
		wins = findWins(hand, cards)
		for i in straights:
			if 1 in i:
				if wins >= 10:
					return straights.pop(straights.index(i)), True
				return straights.pop(straights.index(i))
		return singles.pop(singles.index(1))
	if currPlay == None:
		play = findBestPlay(hand, cards, bombs, straights, triples,\
		 fullHouses, doubles, triple, double, singles, otherHandLen)
		return play
	else:
		return findComputerMoveWithMove(hand, currPlay,cards,bombs,straights,\
		triples,fullHouses,doubles,triple,double,singles,otherHandLen)

###################################
#Test Functions
###################################

def testIsLegalPlay():
	assert isLegalPlay(["eightS", "eightS"],cards,["sevenD", "Pheonix"])==True
	assert isLegalPlay(["nineH","nineC", "tenH", "tenS", "jackD", "jackS"],\
	 cards, ["eightS", "eightD", "nineD", "nineS", "tenD","Pheonix"]) == True
	assert isLegalPlay(["eightS", "eightS", "eightS"], cards, ["sevenD",\
	 "Pheonix", "sevenD"]) == True
	assert isLegalPlay(["nineH","nineC", "nineC", "tenH", "tenS","tenS",\
	 "jackD", "jackS", "jackH"], cards, ["eightS", "eightD","eightD", "nineD",\
	  "nineS", "nineD", "tenD","Pheonix", "tenS"]) == True
	assert isLegalPlay(["threeD", "threeC", "fourD", "fourC", "fourH"], cards,\
	 ["twoD", "twoH", "fiveD", "fiveH", "fiveS"]) == False
	assert isLegalPlay(["fourH", "fiveH", "sixH", "sevenH", "eightH"], cards,\
	 ["Dragon"]) == True
	assert isLegalPlay(["threeC", "fourC", "fiveH", "sixD", "sevenH"], cards,\
	 ["twoD", "threeC", "fourC", "fiveH", "sixD"]) == True

def testRemoveFromDict():
	dictionary = {"hi": 3, "hi1": 4, "hi2": 5, "hi3": 6}
	removeFromDict(3, dictionary)
	removeFromDict(6, dictionary)
	removeFromDict(4, dictionary)
	assert(dictionary == {"hi2": 5})

cards = {'schwj': 11, 'schwk': 13,'rot2': 2,'schwa':14,'rott':10,\
'gruen5': 5, 'gruen4': 4, 'gruen7': 7, 'gruen6': 6, 'mahjong': 1,'gruen3':\
3, 'gruen2': 2, 'rot6': 6, 'gruen9': 9, 'gruen8': 8, 'rot9': 9, 'rot8': 8,\
'schwq': 12, 'blau9': 9, 'blau8': 8, 'blau5': 5, 'blau4': 4, 'blau7': 7,\
'blau6': 6, 'rot5': 5, 'rot4': 4, 'blau3': 3, 'blau2': 2, 'gruena': 14,\
'phoenix': 15, 'gruenk': 13, 'gruenj': 11, 'gruent': 10, 'schw8': 8,\
'schw9': 9, 'gruenq': 12, 'schw2': 2, 'schw3': 3, 'rot7': 7, 'schw6': 6,\
'schw7': 7, 'schw4': 4, 'schw5': 5, 'rotq': 12, 'blaut': 10, 'blauq': 12,\
'dragon': 16, 'rotk': 13, 'rotj': 11, 'blauk': 13, 'blauj': 11,\
'rota': 14, 'blaua': 14, 'rot3': 3, "schwt": 10}

def testFindInCards():
	assert(findInCards(["gruen9"], cards) == [9])
	assert(findInCards(["schw8"], cards) == [8])
	assert(findInCards(["phoenix"], cards) == [15])

def testIsDouble():
	assert(isDouble([2,2]) == True)
	assert(isDouble([2,2,3]) == False)
	assert(isDouble([9,15]) == True)

def testMakePhoenixLowest():
	l = [2,2,3,15]
	makePhoenixLowest(l, 2)
	assert(l == [2,2,3,3])
	l = [2,2,2,3,3,15]
	makePhoenixLowest(l, 3)
	assert(l == [2,2,2,3,3,3])
	l = [4,4,5,5,6,15]
	makePhoenixLowest(l, 2)
	assert(l == [4,4,5,5,6,6])

def testIsPairSequence():
	assert(isPairSequence([2,2,3,3]) == True)
	assert(isPairSequence([2,2,3]) == False)
	assert(isPairSequence([9,15,10,10]) == True)

def testIsTrio():
	assert(isTrio([2,2,2]) == True)
	assert(isTrio([2,2]) == False)
	assert(isTrio([5,5,15]) == True)

def testIsTrioSequence():
	assert(isTrioSequence([2,2,2,3,3,3]) == True)
	assert(isTrioSequence([2,2,2,3,3,3,4,4]) == False)
	assert(isTrioSequence([2,2,2,3,3,3,4,4,15]) == True)

def testFullHouseWithPhoenix():
	assert(fullHouseWithPhoenix([2,2,2,3,15]) == True)
	assert(fullHouseWithPhoenix([2,2,2,15]) == False)
	assert(fullHouseWithPhoenix([4,4,5,5,15]) == True)

def testIsFullHouse():
	assert(isFullHouse([2,2,2,3,15]) == True)
	assert(isFullHouse([10,11,12,13,15]) == False)
	assert(isFullHouse([10,10,12,12,12]) == True)

def testIsStraight():
	assert(isStraight([2,3,4,15,6]) == True)
	assert(isStraight([2,3,4,5]) == False)
	assert(isStraight([10,11,12,13,15]) == True)

def testComboMatches():
	assert(comboMatches([2,3,4,15,6], [1,2,3,4,5]) == True)
	assert(comboMatches([2,2,4,4,4], [2,2,3,3]) == False)
	assert(comboMatches([10,11,12,13,15], None) == True)

def testIsBomb():
	assert(isBomb(["rot3", "blau3", "gruen3", "schw3"],cards) == True)
	assert(isBomb(["rot3", "blau3", "gruen3"],cards) == False)
	assert(isBomb(["rot3", "rot4", "rot5", "rot6", "rot7"],cards) == True)

def testCompliesWithRules():
	assert(compliesWithRules(["rot3", "blau3", "gruen3", "schw3"],cards,None)\
	 == True)
	assert(compliesWithRules(["rot3", "blau3", "gruen3"],cards,["rot4",\
	 "blau4", "gruen4"]) == False)
	assert(compliesWithRules(["rot3", "blau4", "rot5", "rot6", "rot7"],\
		cards,["rot2", "rot3", "blau4", "rot5", "rot6"]) == True)

def testIsLegalPlay():
	assert(isLegalPlay(["rot3", "blau3", "gruen3", "schw3"],cards,None)\
	 == True)
	assert(isLegalPlay(["rot3", "blau3", "gruen3"],cards,["rot4", "blau4"\
		, "gruen4"]) == False)
	assert(isLegalPlay(["rot3", "blau4", "rot5", "rot6", "rot7"],cards,\
		["rot2", "rot3", "blau4", "rot5", "rot6"]) == True)

def testRemoveItems():
	hand = [2,4,5,2,7,8,2,5,8,10]
	removeItems(hand, [[2,2]])
	assert(hand == [4,5,7,8,2,5,8,10])
	hand = [2,4,5,2,7,8,2,5,8,10]
	removeItems(hand, [[5,5,2,2,2]])
	assert(hand == [4,7,8,8,10])
	hand = [2,4,5,2,7,8,2,5,8,10]
	removeItems(hand, [[10]])
	assert(hand == [2,4,5,2,7,8,2,5,8])

def testCheckCombo():
	assert(checkCombo(isStraight, [2,4,5,6,7,8,9], 6, 5) == False)
	assert(checkCombo(isStraight, [4,5,6,7,8,9], 5, 5) == ([4,5,6,7,8,9], 5))
	assert(checkCombo(isStraight, [2,4,5,6,7], 4, 5) == False)

def testFindListCombo():
	hand = [[2,2],[3,3,3],[5,5],8,1,10]
	assert(findListCombo(hand, 2) == ([[2,2],[5,5]], [8, 1, 10, [3,3,3]]))
	hand = [[2,2],[3,3,3],[5,5],8,1,10]
	assert(findListCombo(hand, 3) == ([[3, 3, 3]], [8, 1, 10, [2, 2], [5, 5]]))
	hand = [[2,2],[3,3,3],[5,5],8,1,10]
	assert(findListCombo(hand, 4) == False)

def testFindFullHouses():
	hand = [[2,2],[3,3,3],[5,5],8,1,10]
	assert(findFullHouses(hand) == ([[2,2,3,3,3]], [8, 1, 10, [5,5]]))

def testCombinelists():
	hand = [[2,2],[3,3],10,4,5]
	assert(combinelists(hand) == [2,2,3,3,10,4,5])
	hand = [[2,2],[3,3],[10,10],4,5]
	assert(combinelists(hand) == [2,2,3,3,10,10,4,5])
	hand = [[2,2],3,3,10,4,5]
	assert(combinelists(hand) == [2,2,3,3,10,4,5])

def testFindListComboSequence():
	hand = [[2,2,2],[3,3,3],[5,5],8,1,10]
	assert(findListComboSequence(hand,3) == ([[2,2,2,3,3,3]],[8, 1, 10,[5,5]]))

def testMergeLists():
	assert(mergeLists([[2,2], [3,3], 3, 4, 5, 6, [7,7]]) ==\
	 [2,2,3,3,3,4,5,6,7,7])

def testFindWins():
	hand = [2,4,1,4,6,7,8,14,13,15,16,14]
	assert(findWins(hand, cards) == 3)

def testGetComputerMove():
	hand = ['gruen9', 'blau3', 'gruen3', 'rotj', 'rot3', 'gruenj', 'gruena',\
	 'blau7', 'blaua', 'rot9', 'gruen8', 'rot6', 'rot7', 'rot2', 'blau8',\
	  'schw8', 'schw3', 'blau4', 'rot4', 'gruen7', 'blau9', 'schwj', 'gruen2',\
	   'schw6', 'rotq', 'schw2']
	otherHandLen = 15
	bombs, straights, triples, fullHouses, doubles, triple, double, singles =\
	 [[3, 3, 3, 3]], [], [[7, 7, 7, 8, 8, 8, 9, 9, 9]], [[2, 2, 2, 4, 4],\
	  [6, 6, 11, 11, 11]], [], [], [], [10, 14, 14, 1]
	assert(getComputerMove(hand, cards, bombs, straights, triples, fullHouses,\
 	doubles,triple,double,singles,otherHandLen,None,True)\
 	== 1)
 	assert(getComputerMove(hand, cards, bombs, straights, triples, fullHouses,\
 	doubles,triple,double,singles,otherHandLen,None,False)\
 	== [2,2,2,4,4])
 	assert(getComputerMove(hand, cards, bombs, straights, triples, fullHouses,\
 	doubles,triple,double,singles,otherHandLen,["blau2", "rot2", "gruen2",\
 	 "schw2"],False)\
 	== False)

def testFirstHalf():
	testIsLegalPlay()
	testRemoveFromDict()
	testFindInCards()
	testIsDouble()
	testMakePhoenixLowest()
	testIsPairSequence()
	testIsTrio()
	testIsTrioSequence()
	testFullHouseWithPhoenix()
	testIsFullHouse()
	testIsStraight()
	testGetComputerMove()
	print "Success!!"

def testSecondHalf():
	testComboMatches()
	testIsBomb()
	testCompliesWithRules()
	testIsLegalPlay()
	testRemoveItems()
	testCheckCombo()
	testFindListCombo()
	testFindFullHouses()
	testCombinelists()
	testFindListComboSequence()
	testMergeLists()
	testFindWins()
	print "Success!!"