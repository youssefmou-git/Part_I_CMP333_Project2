# expectimax_agent.py
from agent_base import Agent
from game import GameState
from evaluation import betterEvaluationFunction

class ExpectimaxAgent(Agent):
    def get_action(self, state: GameState, depth=None):
        """
        Returns the best move index (0-8) using Expectimax search.
        Handles stochastic (non-optimal) opponent moves.
        """
        value, action = self.expectimax(state, depth_limit=depth, current_depth=0)
        # Safety fallback in case no action is found
        if action is None:
            legal = state.get_legal_actions()
            if legal:
                action = legal[0]
        return action

    def expectimax(self, state: GameState, depth_limit, current_depth):
        """
        Recursive Expectimax returning (value, best_action)
        """
        # Terminal check
        if state.is_terminal():
            return state.utility(), None
        # Cutoff check
        if depth_limit is not None and current_depth >= depth_limit:
            return betterEvaluationFunction(state), None
        # MAX node (X)
        if state.to_move == 'X':
            best_val = float('-inf')
            best_act = None
            for a in state.get_legal_actions():
                succ = state.generate_successor(a)
                val, _ = self.expectimax(succ, depth_limit, current_depth + 1)
                if val > best_val:
                    best_val, best_act = val, a
            return best_val, best_act

        # CHANCE node (O): average the outcomes
        else:
            actions = state.get_legal_actions()
            if not actions:
                return 0, None
            total = 0
            for a in actions:
                succ = state.generate_successor(a)
                val, _ = self.expectimax(succ, depth_limit, current_depth + 1)
                total += val
            return total / len(actions), None
