# FlappyBird NEAT

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Pygame](https://img.shields.io/badge/Pygame-4BB83B?style=for-the-badge) ![NEAT Python](https://img.shields.io/badge/NEAT_Python-2596be?style=for-the-badge)

An autonomous agent that learns to play Flappy Bird using NeuroEvolution of Augmenting Topologies (NEAT), built entirely in Python.

[Insert Demo GIF / Video Recording Here]

## Background

This project was implemented to explore genetic algorithms and neural network evolution without relying on gradient descent-based backpropagation. The architecture and sensory inputs were modeled after Code Bullet's [A.I. Learns to play Flappy Bird](https://www.youtube.com/watch?v=WSW-5m8lRMs) experiment.

## Architecture & Logic

The system uses a feedforward neural network that evolves over consecutive generations. Instead of pre-defining the network topology, NEAT dynamically alters both the weights and the structure of the network (adding nodes and connections) to optimize for the fitness function.

### Neural Network Parameters

- **Population Size:** 15 genomes evaluated simultaneously per generation (running concurrently without collision).
- **Inputs (3):**
  1. Horizontal distance to the next incoming pipe (`x-diff`)
  2. Vertical distance to the bottom edge of the top pipe
  3. Vertical distance to the top edge of the bottom pipe
- **Output (1):** A single floating point value passed through a `tanh` activation function. If the output strictly exceeds `0.5`, the bird flaps.

### Fitness Function

The fitness logic avoids complex heuristics and relies purely on survival time scaled by the environment execution speed:
$$\text{Fitness} = (\text{Time}_\text{death} - \text{Time}_\text{spawn}) \times \text{game\_speed}$$

### Convergence & Training

Due to the relatively simple state space of the three inputs, the model achieves convergence rapidly. The agent typically discovers an infinite-play stratagem somewhere between **Generation 3 and 15**, which takes approximately 10 seconds of real-time training. Because training is so fast, the repository is designed for users to train the model from scratch rather than relying on a pre-trained serialized network.

### Core Components

- `main.py`: The entry point for the training phase. Initializes the population, calculates fitness, and manages generational speciation. You can manually save a winning genome to `winner.pkl` during runtime.
- `replay_best.py`: Deserializes and renders the playthrough of a saved genome (`winner.pkl`).
- `UserPlayer.py`: A manual execution script allowing human control to baseline physics and input latency.
- `config.txt`: Defines the NEAT configuration parameters, including population size (15), mutation rates, species stagnation thresholds, and node activation functions.

## Tech Stack

- **Python 3.x**
- **pygame:** Execution of the collision physics and graphical rendering.
- **neat-python:** Core library handling the generational genetic algorithm and structural mutations.

## Limitations & Scope

- **Deterministic State:** The environment physics are highly constrained. The neural network learns a specific mapping for this exact game configuration (gravity, pipe speed, gap size) and would require re-training if environment variables change.
- **Scope:** This is a localized script designed for personal exploration of evolutionary algorithms, not a generalized reinforcement learning framework.

## Local Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/qkanji/FlappyBirdAI
   cd FlappyBirdAI
   ```

2. **Install dependencies:**

   ```bash
   pip install pygame neat-python
   ```

3. **Execution:**
   - To train a new model from scratch:
     ```bash
     python main.py
     ```
     _Runtime Controls during training:_
     - `q`: Quit the execution safely.
     - `p`: Preserve the current leading genome (saves to `winner.pkl`).
     - `b`: Trigger a runtime breakpoint for debugging.
   - To view the pre-trained best genome (requires `winner.pkl` to be saved locally first):
     ```bash
     python replay_best.py
     ```
   - To play manually:
     ```bash
     python UserPlayer.py
     ```
