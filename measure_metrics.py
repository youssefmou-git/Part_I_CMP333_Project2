# measure_metrics.py

import time
import argparse

from game import GameState
from minimax_agent import MinimaxAgent
from alphabeta_agent import AlphaBetaAgent
from expectimax_agent import ExpectimaxAgent
from evaluation import betterEvaluationFunction  


def instrument_agent(agent):
    
    # pick the right recursive method name
    if hasattr(agent, "minimax"):
        search_attr = "minimax"
    elif hasattr(agent, "alphabeta"):
        search_attr = "alphabeta"
    elif hasattr(agent, "expectimax"):
        search_attr = "expectimax"
    else:
        raise AttributeError(f"Unknown agent type for instrumentation: {type(agent).__name__}")

    original_search = getattr(agent, search_attr)

    def counted_search(*args, **kwargs):
        # count every recursive invocation as one node expansion
        agent._nodes_this_move += 1
        return original_search(*args, **kwargs)

    setattr(agent, search_attr, counted_search)

    original_get_action = agent.get_action

    def timed_get_action(state, depth=None):
        # reset counter and time this decision
        agent._nodes_this_move = 0
        t0 = time.perf_counter()
        action = original_get_action(state, depth)
        t1 = time.perf_counter()
        agent._last_time_ms = (t1 - t0) * 1000.0
        agent._last_nodes = agent._nodes_this_move
        return action

    agent.get_action = timed_get_action  # monkey-patch
    agent._last_time_ms = 0.0
    agent._last_nodes = 0
    agent._nodes_this_move = 0
    return agent

def make_agent(name: str):
    if name == "MinimaxAgent":
        return instrument_agent(MinimaxAgent())
    if name == "AlphaBetaAgent":
        return instrument_agent(AlphaBetaAgent())
    if name == "ExpectimaxAgent":
        return instrument_agent(ExpectimaxAgent())
    raise ValueError(f"Unknown agent name: {name}")


def play_one_game(agentX, agentO, depth=None, quiet=False):
    state = GameState()
    totals = {"X_ms":0.0,"X_nodes":0,"X_moves":0,"O_ms":0.0,"O_nodes":0,"O_moves":0}

    while not state.is_terminal():
        current = state.to_move
        agent = agentX if current == 'X' else agentO

        action = agent.get_action(state, depth)
        state = state.generate_successor(action)

        # record metrics for this move
        if current == 'X':
            totals["X_ms"] += agent._last_time_ms
            totals["X_nodes"] += agent._last_nodes
            totals["X_moves"] += 1
            if not quiet:
                print(f"[X:{type(agentX).__name__}] move={action}  time={agent._last_time_ms:.3f} ms  nodes={agent._last_nodes}")
        else:
            totals["O_ms"] += agent._last_time_ms
            totals["O_nodes"] += agent._last_nodes
            totals["O_moves"] += 1
            if not quiet:
                print(f"[O:{type(agentO).__name__}] move={action}  time={agent._last_time_ms:.3f} ms  nodes={agent._last_nodes}")

    # compute averages
    X_avg_ms = (totals["X_ms"] / totals["X_moves"]) if totals["X_moves"] else 0.0
    O_avg_ms = (totals["O_ms"] / totals["O_moves"]) if totals["O_moves"] else 0.0
    X_avg_nodes = (totals["X_nodes"] / totals["X_moves"]) if totals["X_moves"] else 0.0
    O_avg_nodes = (totals["O_nodes"] / totals["O_moves"]) if totals["O_moves"] else 0.0

    winner = state.winner()
    outcome = "DRAW" if winner is None else f"{winner} wins"

    # concise summary line (easy to paste into results table)
    print(f"\nSUMMARY: X={type(agentX).__name__}  O={type(agentO).__name__}  outcome={outcome}")
    print(f"         X avg: {X_avg_ms:.3f} ms, {X_avg_nodes:.1f} nodes/move | "
          f"O avg: {O_avg_ms:.3f} ms, {O_avg_nodes:.1f} nodes/move")

    return {
        "outcome": outcome,
        "X_agent": type(agentX).__name__, "O_agent": type(agentO).__name__,
        "X_avg_ms": X_avg_ms, "O_avg_ms": O_avg_ms,
        "X_avg_nodes": X_avg_nodes, "O_avg_nodes": O_avg_nodes
    }

def main():
    parser = argparse.ArgumentParser(description="Measure decision time and nodes expanded per move (no dependency on run_game.py).")
    parser.add_argument("-p","--player", default="AlphaBetaAgent",
                        choices=["MinimaxAgent","AlphaBetaAgent","ExpectimaxAgent"],
                        help="Agent playing as X")
    parser.add_argument("--opp","--opponent", dest="opponent", default="ExpectimaxAgent",
                        choices=["MinimaxAgent","AlphaBetaAgent","ExpectimaxAgent"],
                        help="Agent playing as O")
    parser.add_argument("--depth", type=int, default=None, help="Optional depth limit")
    parser.add_argument("--games", type=int, default=1, help="Repeat games and average summaries")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-move lines")
    args = parser.parse_args()

    # create & instrument agents
    agentX = make_agent(args.player)
    agentO = make_agent(args.opponent)

    # run games
    sums = {"X_ms":0.0,"O_ms":0.0,"X_nodes":0.0,"O_nodes":0.0,"n":0}
    for g in range(args.games):
        if not args.quiet:
            print(f"\n=== GAME {g+1} | X={args.player}  O={args.opponent}  depth={'full' if args.depth is None else args.depth} ===")
        res = play_one_game(agentX, agentO, depth=args.depth, quiet=args.quiet)
        sums["X_ms"] += res["X_avg_ms"]; sums["O_ms"] += res["O_avg_ms"]
        sums["X_nodes"] += res["X_avg_nodes"]; sums["O_nodes"] += res["O_avg_nodes"]
        sums["n"] += 1

    if args.games > 1:
        print("\nOVERALL AVERAGES ACROSS GAMES:")
        print(f"X ({args.player}): {sums['X_ms']/sums['n']:.3f} ms | {sums['X_nodes']/sums['n']:.1f} nodes/move")
        print(f"O ({args.opponent}): {sums['O_ms']/sums['n']:.3f} ms | {sums['O_nodes']/sums['n']:.1f} nodes/move")

if __name__ == "__main__":
    main()
