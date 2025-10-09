# Tic-Tac-Toe AI Project

This project introduces students to adversarial search in artificial intelligence through the implementation of several game-playing agents. The objective is to develop intelligent agents that can play Tic-Tac-Toe optimally or near-optimally using classical AI search algorithms.

## Overview

In this project, you will implement and compare three AI agents that make decisions in a competitive environment. Each agent follows a different decision-making strategy to simulate varying levels of intelligence and performance. The project demonstrates how search depth, pruning, and stochastic behavior affect game outcomes and efficiency.

## Objectives

- Understand and implement core adversarial search algorithms.  
- Analyze the effect of pruning and heuristics on game performance.  
- Experiment with deterministic and stochastic decision-making.  
- Compare outcomes and performance across multiple algorithms.

## Project Structure

```
project2_student/
├── agent_base.py          # Base class for all agents (given)
├── alphabeta_agent.py     # Alpha-Beta pruning (to implement)
├── evaluation.py          # Heuristic evaluation function (given)
├── expectimax_agent.py    # Expectimax algorithm (to implement)
├── game.py                # Game state and logic (given)
├── minimax_agent.py       # Classic Minimax algorithm (to implement)
├── run_game.py            # Command-line interface (given)
└── README.md              # Project documentation
```

Files labeled as "given" should not be modified. They ensure consistent behavior across all student submissions.

## Implement the Following

### Minimax Agent
Implement the **MinimaxAgent** in `minimax_agent.py`.  
Use recursion to explore all possible moves until terminal states are reached. Alternate between maximizing (X) and minimizing (O) turns. Return both the best value and the corresponding action.

**Command:**
```
python run_game.py -p MinimaxAgent
```

---

### Alpha-Beta Agent
Implement the **AlphaBetaAgent** in `alphabeta_agent.py`.  
Extend your minimax implementation by incorporating alpha-beta pruning to improve efficiency. Maintain two parameters:  
- **alpha (α):** Best value found so far for the maximizing player.  
- **beta (β):** Best value found so far for the minimizing player.  
Prune branches whenever the current node cannot influence the final decision.

**Command:**
```
python run_game.py -p AlphaBetaAgent
```

---

### Expectimax Agent
Implement the **ExpectimaxAgent** in `expectimax_agent.py`.  
Replace minimizing nodes with chance nodes that compute the average of all possible outcomes. This algorithm models an opponent that plays randomly instead of optimally.

**Command:**
```
python run_game.py -p ExpectimaxAgent
```

---

### Evaluation Function
A prewritten heuristic evaluation function has been provided in `evaluation.py`.  
This function estimates the utility of non-terminal states when the search is depth-limited. It rewards center control, corner occupancy, and open lines while penalizing blocked positions. Students are not required to modify this file.

---

## Running the Game

### Getting Help
To see all available options and commands:
```
python run_game.py --help
```

### Default Command
Runs the default setup (AlphaBetaAgent vs ExpectimaxAgent):
```
python run_game.py
```

### Choose Specific Algorithms
```
# AlphaBeta vs Minimax
python run_game.py -p AlphaBetaAgent --opp MinimaxAgent

# Minimax vs Expectimax
python run_game.py -p MinimaxAgent --opp ExpectimaxAgent

# Expectimax vs AlphaBeta
python run_game.py -p ExpectimaxAgent --opp AlphaBetaAgent
```

### Depth-Limited Search
You may restrict the search depth for performance testing:
```
python run_game.py -p AlphaBetaAgent --depth 3
```

### Self-Play
To test how an algorithm performs against itself:
```
python run_game.py -p AlphaBetaAgent --opp AlphaBetaAgent
```

### Human vs AI
Play against any of the AI agents interactively. The game randomly chooses who starts first (human or AI):
```
# Play against Alpha-Beta agent
python run_game.py --human AlphaBetaAgent

# Play against Minimax agent
python run_game.py --human MinimaxAgent

# Play against Expectimax agent
python run_game.py --human ExpectimaxAgent

# Play against AI with depth limit
python run_game.py --human AlphaBetaAgent --depth 3
```

In human vs AI mode:
- Choose your moves by entering numbers 0-8 corresponding to board positions
- The grid reference shows: `0 | 1 | 2` (top row), `3 | 4 | 5` (middle row), `6 | 7 | 8` (bottom row)
- The AI and human symbols (X or O) are assigned randomly at the start

## Command-Line Options

| Option | Description | Default |
|--------|--------------|----------|
| `-p, --player` | Agent for player X | AlphaBetaAgent |
| `--opp, --opponent` | Agent for player O | ExpectimaxAgent |
| `--depth` | Maximum search depth | Full search |
| `--human` | Play against chosen AI agent | None (AI vs AI mode) |

## Output Format

Each game prints the board state after every move, along with which agent made the move. The final output displays the winner and the result summary.

### Example Output

```
------------------------------
    GAME START
Initial Board:

   |   |   
---+---+---
   |   |   
---+---+---
   |   |   

----- MOVE 1 -----
Player X -> cell 4

   |   |   
---+---+---
   | X |   
---+---+---
   |   |   

----- MOVE 2 -----
Player O -> cell 0

 O |   |   
---+---+---
   | X |   
---+---+---
   |   |   

------------------------------
        GAME OVER
Result: Draw
```

Do not modify:
- `game.py`  
- `agent_base.py`  
- `evaluation.py`  
- `run_game.py`  

Your implementation must work with the provided files as-is.

---

## Deliverables

1. **Completed Python files** (`minimax_agent.py`, `alphabeta_agent.py`, `expectimax_agent.py`).  
2. **Project Report** summarizing your implementation and observations.  
3. **Google Colab File Link** named `Group_x_Proj2.ipynb`.  
   (File → Save a copy in Drive → Share → Change to "Anyone with the link" → Copy link)

---

