###########################################
#Tutor Class
###########################################

class Tutor(object):
	def __init__(self):
		#creates the important tutorial information
		self.tutorial = """
Tichu is a 2-4 cardgame typically played to 1000 points.
Each hand is started by dealing out 8 cards to everyone, followed by a separate pile of 6 for each player(see below). After looking at all 14 cards everyone passes one card face down to each other player. 
The person with the Mah-Jong or 1 (see below) leads first.

The person who leads shows one of the legal types of plays:
\tsingle card
\tpair
\tany number of consecutive pairs (eg: 2-2-3-3-4-4)
\tthree of a kind
\tfull house
\tstraight of at least length 5
\tAfter the lead everyone may play or pass. A legal play is the same type of play as the lead (including matching exact length if it is a straight or running pairs) of higher value.
\tA player that previously passed may still play if it comes back around to him again. If all other players still in the game pass in succession that round is over and the winner takes all cards played into his scoring pile. 
\tThat player then gets the next lead. Play continues until all but one player has run out of cards. The player who failed to go out gives all of his cards in hand and all of his won cards away. Cards in hand always go to the opponents. 
\tCards in the scoring pile are given to the player who went out first (which could be that player's own partner).

Scoring:
\tThere are two general ways to score points: cards and going out
\tCards:
\t\t5s, 10s, and Ks are worth 5, 10, and 10 points respectively
\t\tDragon is 25 points
\t\tPhoenix is -25 points

Going out:
\tMore important than the card values is going out first.
\tIf the two members of a partnership both run out of cards before either opponent runs out of cards no card points are totalled and they instead are awarded 200 points, plus any points earned for a successful Tichu or Grand Tichu call.
\tA player may call Tichu before playing his first card (which, if he passes several times, could be several tricks into the game). A player that calls Tichu scores a bonus 100 points if he is the first to run out of cards. 
\tIf a Tichu caller fails to run out of cards first his team loses 100 points.
\tA player may call Grand Tichu after seeing his first 8 cards but before seeing the final 6. Grand Tichu is the same as Tichu, except is worth +200 or -200 for success or failure.

Game End:
\tPlay continues until one or both teams reaches a pre-determined point total - usually 1000 points. The team with the most points at that time wins. If the teams are tied you continue playing until the tie is broken.

For more information go to: http://boardgamegeek.com/thread/108365/rules-and-brief-review-of-tichu		
		"""