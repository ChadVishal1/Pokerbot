# ----------- IMPORTS -----------
import random  # Importing the random module

# ----------- CONFIG.PY (Configuration Section) -----------
NUM_ROUNDS = 100
# Example configuration, modify as needed

# ----------- ACTIONS.PY (Actions Section) -----------
class Action():
    pass

class CallAction(Action):
    def __str__(self):
        return 'CallAction'

class CheckAction(Action):
    def __str__(self):
        return 'CheckAction'

class FoldAction(Action):
    def __str__(self):
        return 'FoldAction'

class BidAction(Action):
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f'BidAction({self.amount})'

# ----------- GAME STATES (formerly in stated.py) -----------
class GameState():
    def __init__(self, round_num):
        self.round_num = round_num

class RoundState():
    def __init__(self, auction, legal_actions):
        self.auction = auction
        self.legal_actions = legal_actions

    def __str__(self):
        return f"RoundState(auction={self.auction}, legal_actions={self.legal_actions})"

class TerminalState():
    def __init__(self, game_result):
        self.game_result = game_result

    def __str__(self):
        return f"TerminalState(game_result={self.game_result})"

# ----------- ENGINE.PY (Game Engine Section) -----------
class Engine():
    def __init__(self):
        self.game_state = None

    def run_round(self, bot, round_num):
        # Initialize game state for this round
        game_state = GameState(round_num)
        legal_actions = [CallAction, FoldAction, CheckAction]
        round_state = RoundState(auction=True, legal_actions=legal_actions)
        active = 0  # Assume player is always active

        # Handle new round start
        bot.handle_new_round(game_state, round_state, active)

        # Get action from the bot
        action = bot.get_action(game_state, round_state, active)
        print(f"Bot action: {action}")

        # Simulate the end of the round
        terminal_state = TerminalState(game_result=random.choice(["Win", "Lose", "Draw"]))
        bot.handle_round_over(game_state, terminal_state, active)

# ----------- PLAYER.PY (Player Section) -----------
class Player():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Player(name={self.name})"

# ----------- BOT.PY (Bot Logic Section) -----------
class Bot():
    '''
    The base class for a pokerbot.
    '''

    def __init__(self):
        self.wins = 0  # Initialize win counter
        self.losses = 0  # Initialize loss counter

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.
        '''
        print(f"Starting new round {game_state.round_num}")

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.
        '''
        print(f"Round over. Game result: {terminal_state.game_result}")
        
        # Increment win/loss counters based on the game result
        if terminal_state.game_result == "Win":
            self.wins += 1
        elif terminal_state.game_result == "Lose":
            self.losses += 1

        # Print current score
        print(f"Current Score - Wins: {self.wins}, Losses: {self.losses}")

    def get_action(self, game_state, round_state, active):
        '''
        This is where the bot decides its action.
        '''
        print(round_state)  # For debugging purposes

        if round_state.auction:
            return BidAction(2)  # Bidding a fixed amount during the auction phase
        elif CallAction in round_state.legal_actions:
            return CallAction()  # Calling if it's a legal action
        elif CheckAction in round_state.legal_actions:
            return CheckAction()  # Checking if it's a legal action
        else:
            return FoldAction()  # Default action: fold if no other options are available

# ----------- RUNNER.PY (Main Game Loop Section) -----------
def run_game():
    # Initialize the bot and game engine
    bot = Bot()
    engine = Engine()

    for round_num in range(1, NUM_ROUNDS + 1):
        engine.run_round(bot, round_num)

# ----------- MAIN.PY (Main Entry Point Section) -----------
if __name__ == "__main__":
    run_game()
