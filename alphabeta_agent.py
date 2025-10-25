# alphabeta_agent.py
from agent_base import Agent
from game import GameState
from evaluation import betterEvaluationFunction

class AlphaBetaAgent(Agent):
    def get_action(self, state: GameState, depth=None):
        """
        Returns the best move index (0-8) for Tic-Tac-Toe using Alpha-Beta pruning.
        """
        value, action = self.alphabeta(state, alpha=float('-inf'), beta=float('inf'),
                                       depth_limit=depth, current_depth=0)
        # Safety fallback (never return None)
        if action is None:
            legal = state.get_legal_actions()
            if legal:
                action = legal[0]
        return action

    def alphabeta(self, state: GameState, alpha, beta, depth_limit, current_depth):
        """
        Recursive alpha-beta search returning (value, best_action).
        """
        # 1) stop if game ended
        if state.is_terminal():
            return state.utility(), None
        # 2) stop if we hit the depth limit, use heuristic
        if depth_limit is not None and current_depth >= depth_limit:
            return betterEvaluationFunction(state), None

        # 3) maximizer turn
        if state.to_move == 'X':
            best_val = float('-inf')
            best_act = None
            for a in state.get_legal_actions():
                succ = state.generate_successor(a)
                val, _ = self.alphabeta(succ, alpha, beta, depth_limit, current_depth + 1)
                if val > best_val:
                    best_val, best_act = val, a
                alpha = max(alpha, best_val)
                if alpha >= beta:  # prune
                    break
            return best_val, best_act

        # 4) minimizer turn
        else:
            best_val = float('inf')
            best_act = None
            for a in state.get_legal_actions():
                succ = state.generate_successor(a)
                val, _ = self.alphabeta(succ, alpha, beta, depth_limit, current_depth + 1)
                if val < best_val:
                    best_val, best_act = val, a
                beta = min(beta, best_val)
                if beta <= alpha:  # prune
                    break
            return best_val, best_act
