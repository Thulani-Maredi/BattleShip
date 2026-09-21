import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from GameClient import *
from functools import partial
from PyQt5.QtMultimedia import *

class BattleShipGame(QWidget, GameClient):
  def __init__(self,parent = None):
    QWidget.__init__(self, parent)
    GameClient.__init__(self)
    self.setWindowTitle("Battle Ship")
    self.setGeometry(0, 0, 800, 600)
    self.setMaximumSize(900,600)
     
    # put colours to text
    palette = QPalette()
    palette.setColor(QPalette.Foreground, QColor("lightgray"))
    
    # putting a background to our game
    self.bg_label = QLabel(self)
    self.pixmap = QPixmap("logo.png")
    self.bg_label.setPixmap(self.pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
    self.bg_label.setGeometry(0, 0, self.width(), self.height())
    self.bg_label.lower()
    main_layout = QVBoxLayout()
    top_buttons_layout = QHBoxLayout()
    
    # Putting in instruction for player
    instruction_button = QPushButton("Operation Guidelines")
    instruction_button.setFont(QFont("Algerian", 12))
    instruction_button.setFixedWidth(250)
    main_layout.addWidget(instruction_button)
    top_buttons_layout.addWidget(instruction_button)
    top_buttons_layout.addStretch()
    
    # put music in game and sound effects # Thulani Ehnancements
    music_label = QLabel("Music:")
    music_label.setPalette(palette) 
    music_label.setFont(QFont("Algerian", 12))
    top_buttons_layout.addWidget(music_label)
                
    self.checkbox = QCheckBox() 
    self.checkbox.setChecked(True)
    top_buttons_layout.addWidget(self.checkbox)
    
    sound_effects_label = QLabel("Sound Effects:")#Lungile's enhancements
    sound_effects_label.setPalette(palette) 
    sound_effects_label.setFont(QFont("Algerian", 12))
    top_buttons_layout.addWidget(sound_effects_label)
    
    self.soundeffect_checkbox = QCheckBox()#Lungile's enhancements
    self.soundeffect_checkbox.setChecked(True)
    top_buttons_layout.addWidget(self.soundeffect_checkbox)    
        
    main_layout.addLayout(top_buttons_layout)
    
    # Create and set up the media player # Thulani Enhancement
    self.media_player = QMediaPlayer()
    self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("Love Me Again.mp3")))
    
    # Create and set up sound effects/Lungile's enhancements
    self.hitsound_effect = QMediaPlayer()
    self.hitsound_effect.setMedia(QMediaContent(QUrl.fromLocalFile("Hit Sound Effect.mp3")))
    self.sinksound_effect = QMediaPlayer()
    self.sinksound_effect.setMedia(QMediaContent(QUrl.fromLocalFile("Sink Sound Effect.mp3")))
    self.misssound_effect = QMediaPlayer()
    self.misssound_effect.setMedia(QMediaContent(QUrl.fromLocalFile("Miss Sound Effect.mp3")))    
    
    # check if toggle is on # Thulani Enhancement
    if self.checkbox.isChecked():
        self.media_player.play()
        
    # make music play over and over
    self.media_player.mediaStatusChanged.connect(self.handle_music_status)
    
    # method to control play or pause of music
    self.checkbox.stateChanged.connect(self.toggle_music)
    
    
    # The title of the Game
    title = QLabel("Welcome to <br> BattleShip")
    title.setFont(QFont("Algerian",28))
    title.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(title)
    title.setPalette(palette) 
    
    # Add name tag to each player
    player_layout = QHBoxLayout()
    self.player_label = QLabel(" ")
    self.player_label.setFont(QFont("Algerian", 16))
    self.player_label.setAlignment(Qt.AlignCenter)
    colour = QPalette()
    colour.setColor(QPalette.WindowText, QColor("orange"))
    self.player_label.setPalette(colour)
    player_layout.addWidget(self.player_label) 
    main_layout.addLayout(player_layout)    
  
    # The layout of the body section of the game
    input_layout = QHBoxLayout()
    
    # The layout of all the important editlines and boxes
    server_layout = QVBoxLayout()
    server_label = QLabel("Game server:")
    server_label.setFont(QFont("Algerian",12))
    server_label.setAlignment(Qt.AlignCenter)
    server_label.setPalette(palette)     
    self.server_input = QLineEdit()
    self.server_input.setPlaceholderText("Enter server address")
    self.server_input.setMaximumWidth(150)
    connect_button = QPushButton("Connect")
    connect_button.setFont(QFont("Algerian",10))
        
    # lay the bottons vertically
    server_layout.addWidget(server_label)
    server_layout.addWidget(self.server_input)
    server_layout.addWidget(connect_button)
    input_layout.addLayout(server_layout)
    main_layout.addLayout(input_layout)
  
    # Show what is on the right and what is on the left
    specific_layout = QHBoxLayout()
    debrief_label =  QLabel("Mission Debrief:")
    debrief_label.setFont(QFont("Algerian",12)) 
    debrief_label.setPalette(palette) 
    specific_layout.addWidget(debrief_label)
    specific_layout.addStretch()
    table_label = QLabel("Gaming Table                 ")
    table_label.setFont(QFont("Algerian",20))
    table_label.setPalette(palette) 
    specific_layout.addWidget(table_label)
    main_layout.addLayout(specific_layout)
    
    # Area for to show feedback and board
    game_layout = QHBoxLayout()
    self.feedback_box = QTextEdit()
    self.feedback_box.setFixedSize(300, 420)
    game_layout.addWidget(self.feedback_box)
    self.feedback_box.setReadOnly(True) # make so that no user can edit text
    
    # Spacer between feedback and board
    game_layout.addStretch()
    
    # Create a grid of bottons on the right hand side
    self.grid_widget = QWidget()
    grid_layout = QGridLayout()
    self.buttons = []
    rows = 6
    cols = 6
    for row in range(rows):
      row_buttons = [] # creates new list for new row
      for col in range(cols):
        btn = QPushButton() 
        btn.setFixedSize(80, 60) #size of bottons
        btn.clicked.connect(partial(self.handle_click, row, col)) # connects every click to handle_function to show row and column
        grid_layout.addWidget(btn, row, col)
        row_buttons.append(btn)
      self.buttons.append(row_buttons)                
  
    self.grid_widget.setLayout(grid_layout)
    game_layout.addWidget(self.grid_widget)
    
    # add the game on the main layout
    main_layout.addLayout(game_layout)
    
    # this is to put black screen over table so player does not play when opponent move # Thulani Enhancement
    self.overlay = QWidget(self.grid_widget)
    self.overlay.setGeometry(0, 0, self.grid_widget.width(), self.grid_widget.height())
    overlay_palette = QPalette()
    overlay_palette.setColor(QPalette.Window, QColor(128, 128, 128, 160))
    self.overlay.setAutoFillBackground(True)
    self.overlay.setPalette(overlay_palette)
    self.overlay_label = QLabel("Wait for opponent to play", self.overlay)
    self.overlay_label.setAlignment(Qt.AlignCenter)
    self.overlay_label.setFont(QFont("Algerian", 16))
    overlay_layout = QVBoxLayout(self.overlay)
    overlay_layout.addWidget(self.overlay_label, alignment=Qt.AlignCenter)
    QTimer.singleShot(0, self.align_overlay)
    self.overlay.hide() 
    
    # this is to put black screen over table when game is restarted # Thulani Enhancement
    self.restart = QWidget(self.grid_widget)
    self.restart.setGeometry(0, 0, self.grid_widget.width(), self.grid_widget.height())
    restart_palette = QPalette()
    restart_palette.setColor(QPalette.Window, QColor(128, 128, 128, 160))
    self.restart.setAutoFillBackground(True)
    self.restart.setPalette(restart_palette)
    self.restart_label = QLabel("Wait opponent to restart game.", self.restart)
    self.restart_label.setAlignment(Qt.AlignCenter)
    self.restart_label.setFont(QFont("Algerian", 16))
    restart_layout = QVBoxLayout(self.restart)
    restart_layout.addWidget(self.restart_label, alignment=Qt.AlignCenter)
    QTimer.singleShot(0, self.align_overlay)
    self.restart.hide()     
    
    # Prevent user from clicking bottons until connected to server # Thulani Enhancement
    self.lock_screen = QWidget(self.grid_widget)
    self.lock_screen.setGeometry(0, 0, self.grid_widget.width(), self.grid_widget.height())
    lock_palette = QPalette()
    lock_palette.setColor(QPalette.Window, QColor(128, 128, 128, 160))
    self.lock_screen.setAutoFillBackground(True)
    self.lock_screen.setPalette(lock_palette)
    self.lock_label = QLabel("Connect to server \nto start playing", self.lock_screen)
    self.lock_label.setAlignment(Qt.AlignCenter)
    self.lock_label.setFont(QFont("Algerian", 16))
    lock_layout = QVBoxLayout(self.lock_screen)
    lock_layout.addWidget(self.lock_label, alignment=Qt.AlignCenter)
    QTimer.singleShot(0, self.align_overlay)
    self.lock_screen.show()    
    
    # show winner or tie when game is over and prompt user to play # Thulani Enhancement
    self.over_screen = QWidget(self.grid_widget)
    self.over_screen.setGeometry(0, 0, self.grid_widget.width(), self.grid_widget.height())
    game_palette = QPalette()
    game_palette.setColor(QPalette.Window, QColor(128, 128, 128, 160))
    self.over_screen.setAutoFillBackground(True)
    self.over_screen.setPalette(game_palette)
    self.game_over_label = QLabel("The game ended in a Tie", self.over_screen)
    # play again message to show
    self.play_again_label = QLabel("Do you want to play again ?", self.over_screen)
    self.yes_botton = QPushButton("Yes")
    self.no_botton = QPushButton("No")
    self.yes_botton.setFont(QFont("Algerian",10))
    self.no_botton.setFont(QFont("Algerian",10))
    self.yes_botton.setFixedWidth(150)
    self.no_botton.setFixedWidth(150)
    self.game_over_label.setAlignment(Qt.AlignCenter)
    self.play_again_label.setAlignment(Qt.AlignCenter)
    self.game_over_label.setFont(QFont("Algerian", 16))
    self.play_again_label.setFont(QFont("Algerian", 16))
    play_again_layout = QHBoxLayout()
    play_again_layout.addWidget(self.yes_botton)
    play_again_layout.addWidget(self.no_botton)
    # put them all together
    game_over_layout = QVBoxLayout(self.over_screen)
    game_over_layout.addWidget(self.game_over_label, alignment=Qt.AlignCenter)
    game_over_layout.addWidget(self.play_again_label, alignment=Qt.AlignCenter)
    game_over_layout.addLayout(play_again_layout)
    QTimer.singleShot(0, self.align_overlay)
    self.over_screen.hide()        
  
    # show the Score of Players
    count_layout = QVBoxLayout()
    self.current_player = None  # check if this player is captain or general
    self.prev_player_score = 0
    self.prev_enemy_score = 0    
    self.you_label = QLabel(f"You: {self.prev_player_score}           Enemy: {self.prev_enemy_score}")
    self.you_label.setFont(QFont("Algerian",10))
    self.you_label.setPalette(palette) 
    center_label = QLabel("Hit Count")
    center_label.setFont(QFont("Algerian",18))
    center_label.setPalette(palette) 
    center_label.setAlignment(Qt.AlignCenter)
    self.you_label.setAlignment(Qt.AlignCenter)
    count_layout.addWidget(center_label)
    count_layout.addWidget(self.you_label)
    main_layout.addLayout(count_layout)
    
    # The exit botton
    exit_button = QPushButton("Exit")
    exit_button.setFont(QFont("Algerian",10))
    exit_button.setFixedWidth(150)
    exit_layout = QHBoxLayout()
    exit_layout.addWidget(exit_button)
    main_layout.addLayout(exit_layout)        
    self.setLayout(main_layout)
    
    self.client = GameClient()
    
    self.loop_thread = LoopThread()
    self.loop_thread.signal.connect(self.handle_message)
    
    exit_button.clicked.connect(self.exit_clicked)
    connect_button.clicked.connect(self.connect)
    instruction_button.clicked.connect(self.open_instructions)
    self.yes_botton.clicked.connect(self.play_on)
    self.no_botton.clicked.connect(self.exit_clicked)
    
  # displays which botton is clicked on the textbox
  def handle_click(self, row, col):
    self.feedback_box.append(f"Button ({row}, {col}) was clicked.")
    self.play_game(row, col) 
    
  # send coordinates to play game
  def play_game(self, row, col):
    cordinates = f"{row},{col}"
    game.send_message(cordinates)
    
  #play again message
  def play_on(self):
    game.send_message("y")
    self.restart.show()
    self.over_screen.hide()
    
  # method to make music play endlessly
  def handle_music_status(self, status):
    if status == QMediaPlayer.EndOfMedia:
      self.media_player.play()  
    
  # method to control music using toggle
  def toggle_music(self):
    if self.checkbox.isChecked():
      self.media_player.play()
    else:
      self.media_player.pause()  
    
  # closes application
  def exit_clicked(self):
    self.media_player.pause() 
    self.close() 
  
  def closeEvent(self, event):
      self.media_player.stop()
      event.accept()
  
  def restart_game(self):
    self.feedback_box.clear()
    self.server_input.clear()

    # Reset scores
    self.prev_player_score = 0
    self.prev_enemy_score = 0
    self.you_label.setText(f"You: {self.prev_player_score}          Enemy: {self.prev_enemy_score}")
    
    # restard the bottons to blank and clear all botton colours
    for row_buttons in self.buttons:
      for btn in row_buttons:
        btn.setEnabled(True)
        btn.setStyleSheet("")  

  # times black screen so it fits correctly
  def align_overlay(self):
    self.overlay.setGeometry(self.grid_widget.rect()) 

  
  def handle_message(self, msg):
    self.msg = msg
    self.feedback_box.append(self.msg)
    
    #Showing player name
    self.message = self.msg.split(",")
    if self.message[0] == "new game":
      self.current_player = self.message[1]  # store current player
      self.lock_screen.hide() # remove lockscreen when both players are connected
      self.over_screen.hide() # remove play again once both players press play again
      # wait for other player to agree to restart
      self.restart_game()
      self.restart.hide()
  
      if self.current_player == "C":
        player_label_text = "CodeName: Captain"
      else: 
        player_label_text = "CodeName: General"
      self.player_label.setText(player_label_text)
      
    if self.message[0] == "play again":
      self.overlay.hide()
      
      
    
    # dictionary to store previous score of users
    self.prev_scores = {'C': 0, 'G': 0}
    # showing player scores and showing changes on board
    if self.message[0] == "valid move":
      # get botton clicked to change and disable so it can't be played again
      row = int(self.message[2])
      col = int(self.message[3])
      btn = self.buttons[row][col]
      
       # get players new score
      captain_score = int(self.message[4])
      general_score = int(self.message[5])
      if self.current_player == "C":
          your_score = captain_score
          enemy_score = general_score
      else:
          your_score = general_score
          enemy_score = captain_score
       
      # check who made the move
      mover = self.message[1]
      
      # check score to change botton color
      if mover == self.current_player:
        num = your_score - self.prev_player_score
        self.prev_player_score = your_score
      else:
        num = enemy_score - self.prev_enemy_score
        self.prev_enemy_score = enemy_score
       
      # this is to update score
      self.you_label.setText(f"You: {your_score}          Enemy: {enemy_score}")      

      # Change color of botton to show what happend
      # yellow = hit, green = sink, red = miss
      if num == 1:
        btn.setStyleSheet("background-color: yellow")
        if self.soundeffect_checkbox.isChecked():
          self.hitsound_effect.play()        
      elif num == 2:
        btn.setStyleSheet("background-color: green")
        if self.soundeffect_checkbox.isChecked():
          self.sinksound_effect.play()
      elif num == 0:
        btn.setStyleSheet("background-color: red")
        if self.soundeffect_checkbox.isChecked():
          self.misssound_effect.play()        
      btn.setEnabled(False)      
    
    # blocking player from player if not their move
    if self.message[0] == "opponents move":
        self.overlay.show()
    elif self.message[0] == "your move":
        self.overlay.hide()
        
    # when game is done show winner and prompt user to play again
    elif self.message[0] == "game over":
      if self.message[1] == "C":
        self.game_over_label.setText("The Winner is: Captain\nGood Match")
        self.over_screen.show()
      elif self.message[1] == "G":
        self.game_over_label.setText("The Winner is: General\nGood Match")
        self.over_screen.show()
      else:
        self.over_screen.show()
        
  # method to handle the sizing of the image/lockscreen dynamically # Thulani Enhancement
  def resizeEvent(self, event):
    self.bg_label.setPixmap(self.pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
    self.bg_label.setGeometry(0, 0, self.width(), self.height())
    self.overlay.setGeometry(self.grid_widget.rect())
    self.lock_screen.setGeometry(self.grid_widget.rect())
    self.over_screen.setGeometry(self.grid_widget.rect())
    self.restart.setGeometry(self.grid_widget.rect())
    super().resizeEvent(event)  
  
  def connect(self):
    server_name = self.server_input.text()
    try:
      game.connect_to_server(server_name)
      self.feedback_box.append("Connected to the server.")
      self.loop_thread.start()
    except:
      self.feedback_box.append("Failed to connect.")
      self.lock_screen.show()
      
  def open_instructions(self):
    self.instructions_window = InstructionManual()
    self.instructions_window.show()
      
      
class InstructionManual(QWidget):
    def __init__(self,parent = None):
      QWidget.__init__(self, parent)
      self.setWindowTitle("Battle Ship Instructions")
      self.setGeometry(100, 100, 300, 300)  
      
      self.setPalette(QPalette(QColor("darkblue")))
      self.setAutoFillBackground(True)      
      
      palette = QPalette()
      palette.setColor(QPalette.WindowText, QColor("lightgray"))
      
      instruction_layout = QVBoxLayout()
      
      mission_label = QLabel("Mission Briefing:")
      mission_label.setAlignment(Qt.AlignCenter)
      mission_label.setFont(QFont("Algerian", 18))
      
      mission_label.setPalette(palette)
      instruction_layout.addWidget(mission_label)
      
      
      instructions_text = ("\nAhoy, sailor! Welcome aboard the RSA Victory. Here’s what you need to know before setting sail:\n\n1. Prepare for Battle:\n  Your task is to outsmart and outlast your opponent.\n  Place your ships wisely on the grid; each one is a vital asset to the mission.\n\n2.Targets Locked:\n  On your turn, select a grid coordinate to fire upon.\n  You’ll either hit, miss, or destroy the enemy’s ship!\n\n   -Yellow Button: This indicates a 'hit', you've struck an enemy ship, but it's still afloat.\n\n    -Green Button: This indicates a 'sunk' ship, you've destroyed an enemy ship completely.\n\n    -Red Button: This means a 'miss', no ship was hit in this spot, but stay sharp, the battle isn't over yet!\n\n3. Enemy Strikes Back:\n  Be ready! Your opponent will counter with their own attacks.\n  Protect your fleet and anticipate their moves.\n\n4. Victory Awaits:\n  Sink all of the enemy’s ships before they sink yours.\n  May the best captain win!")
      
      
      instructions_label = QLabel(instructions_text)
      instructions_label.setFont(QFont("Algerian", 10))
      instructions_label.setPalette(palette)
      instruction_layout.addWidget(instructions_label)
      close_button = QPushButton("Close")
      close_button.setFont(QFont("Algerian",10))
      
      close_button.clicked.connect(self.exit_clicked)
      instruction_layout.addWidget(close_button, alignment=Qt.AlignCenter)

      self.setLayout(instruction_layout) 
      
    def exit_clicked(self):
        self.close()      


   
class LoopThread(QThread):
    signal = pyqtSignal(str)
    def __init__(self):
      QThread.__init__(self)

    def run(self):
      while True:
        msg = game.receive_message()
        if len(msg):
          self.signal.emit(msg)
        else:
          break                 


app = QApplication(sys.argv)
game = BattleShipGame()
game.show()
sys.exit(app.exec_())  