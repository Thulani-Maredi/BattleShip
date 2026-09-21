from GameClient import *

class BattleShipTextClient(GameClient):

    def __init__(self):
        GameClient.__init__(self)
        self.board = [x[:] for x in [[' ']*6]*6] # creates 6x6 game board
        self.role = None # role C (for captain) or G (for general)
        
    def clear_board(self):
        self.board = [x[:] for x in [[' ']*6]*6]
        
    def input_server(self):
        return input('enter server:')
     
    def input_move(self):
        return input('enter move(0-5,0-5):')
     
    def input_play_again(self):
        return input('play again(y/n):')

    def display_board(self):
        # draw the table for players to play on
        for i in self.board:
            for k in i:
                print("_|_ ",end = "")
            print()
            
    
    def handle_message(self,msg):
        self.messages = msg.split(",") # split messages by comma and put in list
        
        if self.messages[0] == "new game":
            self.clear_board() #clears all contents of the board
            # welcome menu for different players
            if self.messages[1] == "C":
                print("Welcome to BattleShip Game Captain!")
                self.display_board() 
            else:
                print("Welcome to BattleShip Game General!")
                self.display_board() 
                
        # prompt user to play move and send the answer into the given code        
        if self.messages[0] == "your move":
            print("We attack now, enter your coordinates (0-5,0-5) to shoot!!!")
            self.move = self.input_move()
            self.send_message(self.move)
        
        if self.messages[0] == "valid move":
            # if moves are valid show each player who has moved, where and the score for each player
            if self.messages[1] == "C":
                print(f"Captain has moved to row {self.messages[2]}, column {self.messages[3]}.")
                print(f"Captain score is {self.messages[4]}.")
                print(f"General score is {self.messages[5]}.")
            else:
                print(f"General has moved to row {self.messages[2]}, column {self.messages[3]}.")
                print(f"Captain socre is {self.messages[4]}.")
                print(f"General score is {self.messages[5]}.")
                
        # message for when it it time for opponent to play
        elif self.messages[0] == "opponents move":
            print("Hold very still, opponent is about to attack.")
            
        # prompt user to play again if move is invalid   
        elif self.messages[0] == "invalid move":
            print("Position chosen is invalid. Play another move.")
            self.move = self.input_move()
            self.send_message(self.move)
            
        # if game is over show final scores    
        elif self.messages[0] == "game over":
            if self.messages[1] == "C":
                print("The game has come to a close!!")
                print("And the winner is....Captain")
            elif self.messages[1] == "G":
                print("The game has come to a close!!")
                print("And the winner is....General")
            else:
                print("The game has come to a close!!")
                print("And the winner is....No one, it's a Tie.")
                
        # prompt users to play again or not
        elif self.messages[0] == "play again":
            self.answer = self.input_play_again()
            if self.answer == "y":
                self.clear_board()
                if self.messages[1] == "C":
                    print("Welcome to BattleShip Game Captain!")
                    self.display_board()
                else:
                    print("Welcome to BattleShip Game General!")
                    self.display_board()
            else:
                print("Thank you for playing, we'll see again soon shooter.")
                
        #exit message
        elif self.messages[0] == "exit":
            print("You have now exited the game, Come back soon.")
                
    
    def play_loop(self):
        while True:
            msg = self.receive_message()
            if len(msg): self.handle_message(msg)
            else: break
            
def main():
    bstc = BattleShipTextClient()
    while True:
        try:
            bstc.connect_to_server(bstc.input_server())
            break
        except:
            print('Error connecting to server!')
    bstc.play_loop()
    input('Press enter to exit.')
        
main()