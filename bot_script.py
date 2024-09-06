import discord
import random
import asyncio
import constants
from typing import List, Dict, Union

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)

# Game-related variables
players: List[Union[discord.Member, str]] = []
impostor: Union[discord.Member, str, None] = None
game_started = False
votes: Dict[Union[discord.Member, str], int] = {}
scores: Dict[Union[discord.Member, str], int] = {}
joker_round = random.randint(0, 3)
round_number = 0
pseudo_players = ["mina", "nayeon", "jeongyeon"]
used_image_sets = []

class GameHandler:
    @staticmethod
    async def start_game(channel: discord.TextChannel):
        global impostor, round_number
        current_image_set = random.choice([s for s in constants.IMAGE_SETS if s not in used_image_sets])
        used_image_sets.append(current_image_set)

        if round_number == joker_round:
            current_image_set['impostor'] = constants.IMAGE_JOKER

        impostor = random.choice(players)
        for player in players:
            if isinstance(player, str):
                await channel.send(f"{player}: {current_image_set['impostor'] if player == impostor else current_image_set['normal']}")
            else:
                await player.send(current_image_set['impostor'] if player == impostor else current_image_set['normal'])

        await channel.send(f"Round {round_number + 1} has started! Check your DMs.")
        await GameHandler.start_voting(channel)

    @staticmethod
    async def start_voting(channel: discord.TextChannel, is_tiebreaker: bool = False, tied_players: List[Union[discord.Member, str]] = None):
        global votes
        votes.clear()
        total_votes = 0

        if is_tiebreaker:
            await channel.send("A tie has occurred! There will be a 30-second interval before the tie-breaker voting begins.")
            await asyncio.sleep(constants.TIEBREAKER_INTERVAL)
            await channel.send("Tie-breaker voting session is now open. You have 30 seconds to vote!")
            await channel.send(f"Vote for one of: {', '.join(str(p) for p in tied_players)}")
        else:
            await channel.send("Voting session is now open. You have 60 seconds to vote!")

        async def handle_vote(voter, voted_player):
            nonlocal total_votes
            if (not is_tiebreaker and voted_player in players) or (is_tiebreaker and voted_player in tied_players):
                votes[voted_player] = votes.get(voted_player, 0) + 1
                total_votes += 1
                await channel.send(f"{voter} voted for {voted_player}")
                return True
            return False

        # Pseudo players vote immediately
        for pseudo_player in pseudo_players:
            if pseudo_player in players:
                if is_tiebreaker:
                    random_vote = random.choice(tied_players)
                else:
                    random_vote = random.choice([p for p in players if p != pseudo_player])
                await handle_vote(pseudo_player, random_vote)

        def check(m):
            return m.author in players and m.content.startswith("/voteecho")

        try:
            while total_votes < len(players):
                message = await client.wait_for('message', timeout=constants.VOTING_TIMEOUT, check=check)
                vote_target = message.content.split("/voteecho ")[1].strip()
                voted_player = message.mentions[0] if message.mentions else vote_target
                if await handle_vote(message.author.mention, voted_player):
                    if total_votes == len(players):
                        break
        except asyncio.TimeoutError:
            await channel.send(constants.VOTING_CLOSED_TIMEOUT)

        await GameHandler.show_results(channel, is_tiebreaker, tied_players)

    @staticmethod
    async def show_results(channel: discord.TextChannel, is_tiebreaker: bool = False, tied_players: List[Union[discord.Member, str]] = None):
        global round_number
        max_votes = max(votes.values())
        voted_out = [p for p, v in votes.items() if v == max_votes]
        
        if len(voted_out) > 1:
            if is_tiebreaker:
                await channel.send("The tie persists! Selecting a random player...")
                voted_player = random.choice(voted_out)
                await GameHandler.announce_winner(channel, voted_player)
            else:
                await channel.send(f"It's a tie between {', '.join(str(p) for p in voted_out)}!")
                await channel.send("A tie-breaker round will begin shortly!")
                await GameHandler.start_voting(channel, is_tiebreaker=True, tied_players=voted_out)
        else:
            voted_player = voted_out[0]
            await GameHandler.announce_winner(channel, voted_player)

    @staticmethod
    async def announce_winner(channel: discord.TextChannel, voted_player: Union[discord.Member, str]):
        global round_number
        await channel.send(f"{voted_player} {'was' if voted_player == impostor else 'was not'} the impostor!")
        if voted_player == impostor:
            # Award points to all players except the impostor
            for p in players:
                if p != impostor:
                    scores[p] = scores.get(p, 0) + 1
        else:
            # Award a point to the impostor
            scores[impostor] = scores.get(impostor, 0) + 1

        round_number += 1
        if round_number < constants.MAX_ROUNDS:
            await channel.send(f"Starting Round {round_number + 1}...")
            await asyncio.sleep(5)
            await GameHandler.start_game(channel)
        else:
            await GameHandler.end_game(channel)

    @staticmethod
    async def end_game(channel: discord.TextChannel):
        global players, impostor, game_started, round_number, used_image_sets, joker_round
        players.clear()
        impostor = None
        game_started = False
        round_number = 0
        used_image_sets.clear()
        joker_round = random.randint(0, 3)
        await channel.send(constants.GAME_ENDED)
        await GameHandler.show_scores(channel)

    @staticmethod
    async def show_scores(channel: discord.TextChannel):
        score_message = "\n".join([f"{p}: {s} points" for p, s in scores.items()])
        await channel.send(f"Current Scores:\n{score_message or 'No scores yet!'}")

    @staticmethod
    async def show_about(channel: discord.TextChannel):
        await channel.send(constants.IMAGE_TITLE)
        await channel.send(constants.ABOUT)

    @staticmethod
    async def test_game(channel: discord.TextChannel):
        global players, game_started

        if game_started:
            await channel.send(constants.GAME_ALREADY_STARTED)
            return

        current_player_count = len(players)
        pseudo_count = 4 - current_player_count

        # Add the required number of pseudo players to make total 4 players
        for i in range(pseudo_count):
            players.append(pseudo_players[i])
            await channel.send(f"{pseudo_players[i]} has been added to the game!")

        game_started = True
        await GameHandler.start_game(channel)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    global players, game_started

    if message.author == client.user:
        return

    if message.content.startswith('/addecho'):
        if not game_started:
            if message.author not in players:
                players.append(message.author)
                scores[message.author] = 0
                await message.channel.send(f"{message.author.mention} has been added to the game!")
            else:
                await message.channel.send(f"{message.author.mention} is already in the game!")
            if len(players) == 4:
                game_started = True
                await GameHandler.start_game(message.channel)
        else:
            await message.channel.send(constants.GAME_ALREADY_STARTED)

    elif message.content.startswith('/endecho'):
        if game_started:
            await GameHandler.end_game(message.channel)
        else:
            await message.channel.send(constants.NO_ONGOING_GAME)

    elif message.content.startswith('/scoreecho'):
        await GameHandler.show_scores(message.channel)

    elif message.content.startswith('/aboutecho'):
        await GameHandler.show_about(message.channel)

    elif message.content.startswith('/testecho'):
        if not game_started:
            await GameHandler.test_game(message.channel)
        else:
            await message.channel.send(constants.GAME_ALREADY_STARTED)

client.run(constants.BOT_TOKEN)