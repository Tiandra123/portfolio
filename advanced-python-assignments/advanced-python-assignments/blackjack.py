# pre-works
#imports
from DeckOfCards import *

#variables

restart = True
userHand = []
userScore = 0
houseHand = []
houseScore = 0
newUserScore = 0
newHouseScore = 0

def user_over21():
  print("\n", "Your cards: ")
  for card in userHand:
    print(card) # the str thingy here too
  print("Your Score: ", userScore, "\n")
  print("\n", "You busted! House wins!", "\n")
  print("\n", "House cards: ")
  for card in houseHand:
    print(card)  # using the __ str __ thingy 

def house_over21():
  print("\n", "Your cards: ")
  for card in userHand:
    print(card) # the str thingy here too
  print("Your Score: ", userScore, "\n")
  print("\n", "House Busted, you win!", "\n")
  print("\n", "House cards: ")
  for card in houseHand:
    print(card)  # using the __ str __ thingy 

def user_hit_yes():
  nextcard = deck.get_card()
  print("\n", "Next card: ", nextcard)
  newUserScore = userScore + nextcard.val
  print("\n", "Your new score: ", newUserScore, "\n")
  userHand.append(nextcard)
  return newUserScore

def user_hit_no():
  print("\n", "Your cards: ")
  for card in userHand:
    print(card) # the str thingy here too
  print("Your Score: ", userScore, "\n")
  print("\n", "House cards: ")
  for card in houseHand:
    print(card)  # using the __ str __ thingy 
  print("House Score: ", houseScore, "\n")
  
def house_hit_yes():
  housenextcard = deck.get_card()
  print("\n", "House's next card: ", housenextcard)
  newHouseScore = houseScore + housenextcard.val
  print("\n", "House's Score: ", newHouseScore, "\n")
  houseHand.append(housenextcard)
  return newHouseScore

def house_hit_no():
  print("\n", "Your cards: ")
  for card in userHand:
    print(card) # the str thingy here too
  print("Your Score: ", userScore, "\n")
  print("\n", "House cards: ")
  for card in houseHand:
    print(card)  # using the __ str __ thingy 
  print("House Score: ", houseScore, "\n")

def evaluate_winner():
    if houseScore > 21:
        print("\n", "House Busted, you win!", "\n")
    elif houseScore > userScore and houseScore <= 21:
        print("\n", "House is high, you lose . . .", "\n")
    else:
        print("\n", "House is low, you win!", "\n")

def restart_game():
  restartChoice = input("Do you want to play again? Yes or no? ")
  if restartChoice == "yes":
    return True
  else:
    print("\n", "Thanks for playing!", "\n")
    return False


# the intro
print("\n", "Welcome to Blackjack!", "\n")

deck = DeckOfCards()

while restart is True: 
    restart = True
    userHand = []
    userScore = 0
    houseHand = []
    houseScore = 0
    newUserScore = 0
    newHouseScore = 0

    print("\n")
    deck.print_deck()

    deck.shuffle_deck()

    print("\n", "Deck shuffled:", "\n")
    deck.print_deck()

    # the set up - deal user two cards - Don't display dealers cards yet but keep track of them
    print("\n", "Your cards:", "\n")
    card = deck.get_card()
    card2 = deck.get_card()
    print(card)
    print(card2)

    userHand.append(card)
    userHand.append(card2)

    houseCard = deck.get_card()
    houseCard2 = deck.get_card()

    houseHand.append(houseCard)
    houseHand.append(houseCard2)

    houseScore += houseCard.val
    houseScore += houseCard2.val

    userScore += card.val
    userScore += card2.val
    print("\n", "Your Score: ", userScore, "\n")

    # the GAME
    game_over = False # need this because we keep getting stuck in the wanna restart loop
    for play in range (3): # user already has two cards - can only have 5 total
        if userScore > 21:
            user_over21()
            restart = restart_game()
            game_over = True
            break
            
    # game end ------------------------------------------------------
        else:
            print("\n")
            hit = input("Would you like a hit? yes or no? ")
            print("\n")

            # another one
            if hit == "yes":
                userScore = user_hit_yes()
                if userScore > 21:
                    print("You busted! You lose!", "\n")

            elif hit == "no":
                # the house 
                print("\n", "House cards: ")
                for card in houseHand:
                    print(card)  # using the __ str __ thingy 
                print("House Score: ", houseScore, "\n")
                
                # house playing rules
                if houseScore > 21:
                    house_over21()
                elif houseScore > 17:
                    house_hit_no()
                    evaluate_winner()
                else:  
                    while houseScore <= 17: # adding while loop because for loop is not working lol
                        houseScore = house_hit_yes()
                    house_hit_no()
                    evaluate_winner()
            
            restart = restart_game()
            game_over = True
            break
            
    if not game_over:
        if userScore <= 21:
            print("\n", "Your cards: ")
            for card in userHand:
                print(card)
            print("Your Score: ", userScore, "\n")
            print("\n", "five card Charlie! You win!!!", "\n")
            restart = restart_game()
        else:
            user_over21()
            restart = restart_game()
