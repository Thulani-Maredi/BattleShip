# BattleShip

A networked Battleship game built in Python. Two players connect to a shared server and play on a 6 x 6 board. The project includes a PyQt5 graphical client, a terminal client, and a socket-based game server.

## Highlights

- Real-time two-player play over TCP sockets
- PyQt5 graphical interface with score tracking and turn indicators
- Terminal client for lightweight gameplay and testing
- Random ship placement on a 6 x 6 board
- Hit, miss, and ship-sunk feedback
- Optional background music and sound effects
- Replay support after a match

## Project Layout

| File | Purpose |
| --- | --- |
| `BattleShipGameServer.py` | Starts the game server and manages matches |
| `Battle Ship Game GUI.py` | Starts the PyQt5 graphical client |
| `BattleShipTextClient.py` | Starts the terminal client |
| `GameServer.py` | Shared server networking and logging |
| `GameClient.py` | Shared client networking and logging |
| `GameIni.py` | Port, buffer, board, and game configuration |
| `Final Report.docx` | Project report |
| `logo.png` and `*.mp3` | Game artwork, music, and sound effects |

## Requirements

- Python 3.9 or newer
- PyQt5
- A local network connection when clients and server run on different machines

Install the Python dependency:

```bash
python -m pip install -r requirements.txt
```

## Run Locally

Open three terminal windows in the project directory.

1. Start the server:

   ```bash
   python BattleShipGameServer.py
   ```

2. Start the first client. For the graphical client:

   ```bash
   python "Battle Ship Game GUI.py"
   ```

   Or use the terminal client:

   ```bash
   python BattleShipTextClient.py
   ```

3. Start a second client and connect both clients to the server address. Use `localhost` when everything runs on one computer.

The server listens on port `12345`, configured in `GameIni.py`.

## How To Play

Each player is assigned the role of Captain or General. On your turn, enter a coordinate such as `2,4` or select a square in the GUI. Yellow indicates a hit, green indicates a sunk ship, and red indicates a miss. The first player to sink the opposing fleet wins.

## Technical Notes

The server is authoritative: it creates the board, validates moves, tracks scores, and broadcasts game events to both clients. Client and server activity is written to local log files during a run; generated logs are ignored by Git.

This is a university project demonstrating Python object-oriented programming, TCP networking, GUI development, concurrency, and client-server communication.
