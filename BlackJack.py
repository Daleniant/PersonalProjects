# A Simple text-based game of BlackJack that you can easily play via terminal, made for OOP Practice
# Based on the following rules: https://www.themresort.com/-/media/png/midwest/boom-town/pdfs/btc-tablegames-blackjack-link.pdf

import random

cards = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
#        2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A
pWins, dWins = 0, 0

class Hand:
    score = 0
    name = ""

    def __init__(self, in_name):
        self.draw()
        self.draw()
        name = in_name

    def draw(self):
        card_id = random.randint(0, 12)
        while(cards[card_id] == 0):
            card_id = random.randint(0, 12)
        cards[card_id] -= 1

        if card_id <= 8:
            self.score += 2 + card_id
        elif card_id != 12:
            self.score += 10
        else:
            if self.score + 11 <= 21:
                self.score += 11
            else:
                self.score += 1

    def bust(self):
        print(f"{name} has busted with the score of {score}!")


def play(name):
    global cards, pWins, dWins
    print(f"\nPlayer-Dealer win score: {pWins}-{dWins}")
    print("\nGame Started!")

    if not name:
        name = "Player"

    dealer = Hand("Dealer")
    player = Hand(name)
    print(f"Starting hand: {player.score}\n")

    dealerStands = False
    playerStands = False

    while True:
        if dealer.score >= 17:
            dealerStands = True
            print("Dealer Stands")
        else:
            print("Dealer has drawn a card")
            dealer.draw()

        if dealer.score > 21:
            print(f"\nDealer has broken with the score of {dealer.score}!\n{name} wins!")
            pWins += 1
            break

        if not playerStands:
            print(f"Your move. Current score: {player.score}:")
            print("1. Hit")
            print("2. Stand")
            if input() == "1":
                player.draw()
                if player.score > 21:
                    print(f"You have broken with the score of {player.score}! \nDealer wins!")
                    dWins += 1
                    break
            else:
                playerStands = True

        if dealerStands and playerStands:
            if player.score > dealer.score:
                print("\nYou win!", end=" ")
                pWins += 1
            elif player.score == dealer.score:
                print("\nIt's a standoff!", end=" ")
            else:
                print("\nDealer wins!", end=" ")
                dWins += 1

            print(f"{name}: {player.score}, Dealer: {dealer.score}")
            break

    print("\nPlay another game? (Y/N) ", end="")
    if input()[0].lower() == 'y':
        cards = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        play(name)

if __name__ == '__main__':
    print("Enter your name(Or press Enter to skip): ", end="")
    play(input())
