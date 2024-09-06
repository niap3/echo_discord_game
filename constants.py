BOT_TOKEN = 'MY_TOKEN'

IMAGE_TITLE = "https://i.postimg.cc/5yH2BBc2/Back.png"

IMAGE_JOKER = "https://i.postimg.cc/zfSbvF5m/Impostor.png"

# images for set 1
IMAGE_SETS = [
    {'normal': 'https://i.postimg.cc/fbhSMgGj/AGRICULTURE.png', 'impostor': 'https://i.postimg.cc/NMsyH2fK/WATER.png'},
    {'normal': 'https://i.postimg.cc/gcwhqRHh/Flood.png', 'impostor': 'https://i.postimg.cc/vHf6CsjH/Quake.png'},
    {'normal': 'https://i.postimg.cc/85xjnKm6/OldAge.png', 'impostor': 'https://i.postimg.cc/Y9vvRKY7/Black.png'},
    {'normal': 'https://i.postimg.cc/9XTMQBBL/Woman.png', 'impostor': 'https://i.postimg.cc/gjvktY0C/Inequality.png'},
    {'normal': 'https://i.postimg.cc/nhTMtc1Z/Sustainability.png', 'impostor': 'https://i.postimg.cc/MGTHZ2sB/Sanitation.png'},
    {'normal': 'https://i.postimg.cc/ncbX4Wz8/Poverty.png', 'impostor': 'https://i.postimg.cc/jqJWJTRQ/Homeless.png'},
]

# constant numbers
MAX_ROUNDS = 4
VOTING_TIMEOUT = 60
TIEBREAKER_INTERVAL = 30

# common strings
GAME_STARTED = "The game has started! Check your DMs."
TIMER_STARTED = "Timer has started. Voting will begin in 1 minute."
VOTING_STARTED = "Voting has started! Mention the player you think is the impostor."
VOTING_CLOSED_TIMEOUT = "Voting session closed due to timeout!"
GAME_ALREADY_STARTED = "The game has already started!"
GAME_ALREADY_HAS_4_PLAYERS = "The game already has 4 players!"
ADD_YOURSELF_FIRST = "You need to add yourself using /add first!"
NO_ONGOING_GAME = "There is no ongoing game to end."
GAME_ENDED = "The game has been ended. Thanks for playing. You can start a new game with /addecho."
NO_VOTES_CAST = "No votes were cast!"
INVALID_VOTE = "Invalid vote!"
SECONDS_REMAINING = "{} seconds remaining..."

ABOUT = """
**Game Mechanics:**
- **/addecho**: Add yourself to the game.
- **/voteecho @username**: Cast a vote for the impostor.
- **/endecho**: End the game and reset all players.
- **/scoreecho**: Display the current scores.
this:
- **/aboutecho**: Show game instructions and commands.
                           
One random player will be the impostor. The goal is to find the impostor through voting rounds.
"""