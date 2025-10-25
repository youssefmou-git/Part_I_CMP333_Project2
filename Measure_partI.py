# Measure_partI.py

import time
import argparse

from game import GameState
from minimax_agent import MinimaxAgent
from alphabeta_agent import AlphaBetaAgent
from expectimax_agent import ExpectimaxAgent


def instrument_agent(agent, algo_attr_name):
    """
    Wrap the agent's recursive search method to count how many nodes are visited
    (one count per recursive call), and wrap get_action to time the decision.
    """
    # Wrap the recursive method used by this agent
    orig_algo = getattr(agent, algo_attr_name)

    def counted_algo(*args, **kwargs):
        # Increment per-move node counter on every recursive call
        agent._nodes_this_move += 1
        return orig_algo(*args, **kwargs)

    setattr(agent, algo_attr_name, counted_algo)

    # Wrap get_action to time the decision and reset counters per move
    orig_get_action = agent.get_action

    def timed_get_action(state, depth=None):
        agent._nodes_this_move = 0
        t0 = time.time()
        action = orig_get_action(state, depth)
        t1 = time.time()
        agent._last_time_ms = (t1 - t0) * 1000.0
        agent._last_nodes = agent._nodes_this_move
        return action

    agent.get_action = timed_get_action  # monkey-patch
    # Initialize attributes so they're always present
    agent._last_time_ms = 0.0
    agent._last_nodes = 0
    agent._nodes_this_move = 0

def make_agent(name):
    if name == "MinimaxAgent":
        a = MinimaxAgent()
        instrument_agent(a, "minimax")
        return a
    if name == "AlphaBetaAgent":
        a = AlphaBetaAgent()
        instrument_agent(a, "alphabeta")
        return a
    if name == "ExpectimaxAgent":
        a = ExpectimaxAgent()
        instrument_agent(a, "expectimax")
        return a
    raise ValueError(f"Unknown agent: {name}")

def print_board(state: GameState):
    b = [c if c is not None else " " for c in state.board]
    print(f"   {b[0]} | {b[1]} | {b[2]}")
    print("  -----------")
    print(f"   {b[3]} | {b[4]} | {b[5]}")
    print("  -----------")
    print(f"   {b[6]} | {b[7]} | {b[8]}")



def play_one_game(agentX, agentO, depth_limit=None, verbose=True):
    state = GameState()
    totals = {
        "X_time_ms": 0.0, "X_nodes": 0, "X_moves": 0,
        "O_time_ms": 0.0, "O_nodes": 0, "O_moves": 0
    }
    move_num = 1
    if verbose:
        print("\n=== NEW GAME ===")
        print(f"X: {type(agentX).__name__} | O: {type(agentO).__name__} | depth={depth_limit if depth_limit is not None else 'full'}")
        print("\nInitial board:")
        print_board(state)

    while not state.is_terminal():
        current = state.to_move
        agent = agentX if current == 'X' else agentO
        action = agent.get_action(state, depth_limit)
        state = state.generate_successor(action)

        if current == 'X':
            totals["X_time_ms"] += agent._last_time_ms
            totals["X_nodes"]   += agent._last_nodes
            totals["X_moves"]   += 1
        else:
            totals["O_time_ms"] += agent._last_time_ms
            totals["O_nodes"]   += agent._last_nodes
            totals["O_moves"]   += 1

        if verbose:
            print(f"\n--- MOVE {move_num} ({current}) ---")
            print(f"{type(agent).__name__} chose cell {action}")
            print(f"Decision time: {agent._last_time_ms:.2f} ms | Nodes expanded: {agent._last_nodes}")
            print_board(state)
            move_num += 1

    w = state.winner()
    outcome = "DRAW" if w is None else f"{w} wins"
    if verbose:
        print("\n=== GAME OVER ===")
        print(f"Outcome: {outcome}")

    # compute per-move averages
    X_avg_ms = (totals["X_time_ms"] / totals["X_moves"]) if totals["X_moves"] else 0.0
    O_avg_ms = (totals["O_time_ms"] / totals["O_moves"]) if totals["O_moves"] else 0.0
    X_avg_nodes = (totals["X_nodes"] / totals["X_moves"]) if totals["X_moves"] else 0.0
    O_avg_nodes = (totals["O_nodes"] / totals["O_moves"]) if totals["O_moves"] else 0.0

    summary = {
        "outcome": outcome,
        "X_agent": type(agentX).__name__,
        "O_agent": type(agentO).__name__,
        "X_avg_time_ms": X_avg_ms,
        "O_avg_time_ms": O_avg_ms,
        "X_avg_nodes": X_avg_nodes,
        "O_avg_nodes": O_avg_nodes,
    }
    return summary

def main():
    parser = argparse.ArgumentParser(description="Measure execution time and node counts (no changes to run_game.py).")
    parser.add_argument("-p", "--player", default="AlphaBetaAgent",
                        choices=["MinimaxAgent", "AlphaBetaAgent", "ExpectimaxAgent"])
    parser.add_argument("--opp", "--opponent", dest="opponent", default="ExpectimaxAgent",
                        choices=["MinimaxAgent", "AlphaBetaAgent", "ExpectimaxAgent"])
    parser.add_argument("--depth", type=int, default=None)
    parser.add_argument("--games", type=int, default=1)
    parser.add_argument("--quiet", action="store_true", help="Less verbose output")
    args = parser.parse_args()

    agentX = make_agent(args.player)
    agentO = make_agent(args.opponent)

    agg = {"X_ms":0.0,"O_ms":0.0,"X_nodes":0.0,"O_nodes":0.0,"games":0}
    for g in range(args.games):
        summary = play_one_game(agentX, agentO, depth_limit=args.depth, verbose=not args.quiet)
        print(f"\n[Summary Game {g+1}] Outcome={summary['outcome']}"
              f" | X={summary['X_agent']} avg {summary['X_avg_time_ms']:.2f} ms, {summary['X_avg_nodes']:.1f} nodes"
              f" | O={summary['O_agent']} avg {summary['O_avg_time_ms']:.2f} ms, {summary['O_avg_nodes']:.1f} nodes")
        agg["X_ms"] += summary["X_avg_time_ms"]
        agg["O_ms"] += summary["O_avg_time_ms"]
        agg["X_nodes"] += summary["X_avg_nodes"]
        agg["O_nodes"] += summary["O_avg_nodes"]
        agg["games"] += 1

    # overall averages across games
    if args.games > 1:
        print("\n===== OVERALL AVERAGES =====")
        print(f"X ({type(agentX).__name__}): {agg['X_ms']/agg['games']:.2f} ms | {agg['X_nodes']/agg['games']:.1f} nodes per move")
        print(f"O ({type(agentO).__name__}): {agg['O_ms']/agg['games']:.2f} ms | {agg['O_nodes']/agg['games']:.1f} nodes per move")

if __name__ == "__main__":
    main()
