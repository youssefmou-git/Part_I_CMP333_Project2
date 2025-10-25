# minimax_agent.py
from agent_base import Agent
from game import GameState

class MinimaxAgent(Agent):
    def get_action(self, state: GameState, depth=None):
        _, action = self.minimax(state)
        return action

    def minimax(self, state, depth_limit=None):
        """
        Minimax basically looks ahead at all the possible game states.
        X is the maximizing player, O is the minimizing one.
        We go down the tree until the game is over and then bubble the values back up.
        """

        # 1) if the game already ended, just give back the utility score
        if state.is_terminal():
            return state.utility(), None

        # 2) if it's X’s turn, try to get the biggest value
        if state.to_move == 'X':
            best_val = float('-inf')
            best_act = None
            for a in state.get_legal_actions():
                # make the move and check what happens
                succ = state.generate_successor(a)
                val, _ = self.minimax(succ)
                if val > best_val:
                    best_val, best_act = val, a
            return best_val, best_act

        # 3) if it's O’s turn, try to make the value as small as possible
        else:
            best_val = float('inf')
            best_act = None
            for a in state.get_legal_actions():
                succ = state.generate_successor(a)
                val, _ = self.minimax(succ)
                if val < best_val:
                    best_val, best_act = val, a
            return best_val, best_act
