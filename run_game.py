# run_game.py
import argparse
import random
from game import GameState
from minimax_agent import MinimaxAgent
from alphabeta_agent import AlphaBetaAgent
from expectimax_agent import ExpectimaxAgent
from evaluation import betterEvaluationFunction


def play_game(agentX, agentO, depth_limit=None, verbose=True):
    """
    Runs a Tic-Tac-Toe game between two agents (X and O).
    Displays a clean, easy-to-read board layout.
    """
    state = GameState()

    def display_board(s: GameState):
        board = [c if c is not None else " " for c in s.board]
        print(f"\n   {board[0]} | {board[1]} | {board[2]} ")
        print("  -----------")
        print(f"   {board[3]} | {board[4]} | {board[5]} ")
        print("  -----------")
        print(f"   {board[6]} | {board[7]} | {board[8]} ")
        print("   0   1   2   (cell indices)")
        print()

    # Get agent names for display
    agent_x_name = type(agentX).__name__
    agent_o_name = type(agentO).__name__
    
    if verbose:
        print("\n" + "="*50)
        print("           TIC-TAC-TOE AI BATTLE")
        print("="*50)
        print(f"Player X: {agent_x_name}")
        print(f"Player O: {agent_o_name}")
        if depth_limit:
            print(f"Search Depth: {depth_limit}")
        else:
            print("Search Depth: Full search")
        print("\nInitial Board:")
        display_board(state)

    move_num = 1

    while not state.is_terminal():
        current_player = state.to_move
        agent = agentX if current_player == 'X' else agentO
        action = agent.get_action(state, depth_limit)

        # Safety fallback
        if action is None:
            import random
            legal = state.get_legal_actions()
            action = random.choice(legal)
            current_agent_name = agent_x_name if current_player == 'X' else agent_o_name
            print(f"[WARNING] {current_agent_name} returned None - using random move {action}")

        # Update state
        state = state.generate_successor(action)

        if verbose:
            print(f"\n--- MOVE {move_num} ---")
            current_agent_name = agent_x_name if current_player == 'X' else agent_o_name
            print(f"{current_agent_name} ({current_player}) chooses cell {action}")
            display_board(state)
            move_num += 1

    # Final outcome
    winner = state.winner()
    print("\n" + "="*50)
    print("             GAME RESULTS")
    print("="*50)
    
    if winner is None:
        print("Result: DRAW")
        print("Both algorithms played optimally!")
    else:
        winning_agent = agent_x_name if winner == 'X' else agent_o_name
        print(f"WINNER: {winning_agent} ({winner})")
        
    print(f"\nFinal Board:")
    display_board(state)
    print("="*50)



def main():
    parser = argparse.ArgumentParser(
        description="AI Tic-Tac-Toe Battle: Watch different algorithms compete!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Algorithm Descriptions:
  MinimaxAgent     - Classic minimax with perfect play
  AlphaBetaAgent   - Optimized minimax with alpha-beta pruning  
  ExpectimaxAgent  - Handles stochastic/random opponents

Example usage:
  python run_game.py -p AlphaBetaAgent --opp MinimaxAgent
  python run_game.py --depth 5
        """
    )
    parser.add_argument(
        "-p", "--player",
        default="AlphaBetaAgent",
        choices=["MinimaxAgent", "AlphaBetaAgent", "ExpectimaxAgent"],
        help="Algorithm for Player X (default: AlphaBetaAgent)"
    )
    parser.add_argument(
        "--opp", "--opponent",
        default="ExpectimaxAgent",
        choices=["MinimaxAgent", "AlphaBetaAgent", "ExpectimaxAgent"],
        help="Algorithm for Player O (default: ExpectimaxAgent)"
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=None,
        help="Maximum search depth (default: unlimited)"
    )
    args = parser.parse_args()

    agent_map = {
        "MinimaxAgent": MinimaxAgent(),
        "AlphaBetaAgent": AlphaBetaAgent(),
        "ExpectimaxAgent": ExpectimaxAgent(),
    }

    agentX = agent_map[args.player]
    agentO = agent_map[args.opp]

    play_game(agentX, agentO, depth_limit=args.depth, verbose=True)


if __name__ == "__main__":
    main()
