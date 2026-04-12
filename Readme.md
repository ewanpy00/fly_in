*This project has been created as part of the 42 curriculum by ipykhtin.*

# 🛸 Fly-In Drones: Pathfinding & Traffic Control

## 📝 Description
**Fly-In Drones** is a swarm management simulator operating in constrained airspace. The primary goal of the project is to guide a group of drones from starting hubs to their respective destinations (`end_hub`) while minimizing the total number of turns and respecting the capacity limits of each zone.

The project models complex navigation logic where path selection depends not only on geometric distance but also on "terrain" types (zone costs) and real-time traffic density.

---

## 🛠️ Instructions

### Installation
Python 3.10+ and the Pygame library are required.
```bash
make install
```

### Execution
Run the simulation on the deafult map that is set up in Makefile:
```bash
make run
```

Run a specific map with a custom speed:
```bash
make run MAP=<Map name> SPEED=<Speed from 1 to 5>
```

For manual/step-by-step control (press Space to advance turns):
```bash
make run-debug
```

### Linters
Run to check the linters
```bash
make lint
```

### Cleaner
To clean all the cache run:
```bash
make clean
```

## 🧠 Implementation Strategy

# 1. Pathfinding Algorithm

The project utilizes a modified Dijkstra's Algorithm. Instead of searching for the shortest geometric path, the algorithm identifies the path with the lowest "complexity cost" ($Cost$).The edge weight calculation formula is:

$$Cost_{total} = BaseCost_{zone} + (CurrentDrones \times 1)$$

# Zone Types and Their Impact:

| Zone Type | Base Cost ($BaseCost$) | Logic / Behavior |
| :--- | :--- | :--- |
| Priority | 0.5 | Preferred zone; attracts drones by lowering path cost. |
| Normal | 1.0 | Standard movement zone. |
| Restricted | 2.0 | High-sensitivity zone; crossing takes 2 turns. |
| Blocked | $\infty$ | Inaccessible zone; completely excluded from the graph. |

# 2. Movement & Interpolation

To achieve smooth drone transitions, Linear Interpolation (LERP) was implemented. This allows drones to glide between zone coordinates, providing high-quality visualization:

$$P(t) = P_{start} + t \times (P_{end} - P_{start})$$

where $t$ represents movement progress from 0 to 1.

### 3. The Restricted Zone Challenge

To implement the "2 turns per zone" mechanic, an animation interruption strategy was chosen:
* **First Turn:** The drone starts moving and reaches $t = 0.5$ (midpoint).
* **Pause Logic:** Its `is_moving` state is set to `False`, pausing the movement for that turn.
* **Second Turn:** The system "resumes" the drone's flight, allowing it to complete the remaining 50% of the path.
* **Accuracy:** This ensures accurate turn counting without the need to inject "ghost nodes" into the map data.

## 🎨 Visual Representation
The Pygame-based visualization significantly enhances the User Experience:

* **Interactivity:** Hovering over a zone triggers a Tooltip displaying the zone type, current drone count, and max capacity.
* **Color Coding:** Zones are color-coded based on metadata (e.g., Golden for Priority, Dull Red for Restricted).
* **Smoothness:** LERP-based movement helps the user understand the trajectory and logic behind why a drone chose a specific branch during high network congestion.

## 🏆 Performance & Benchmarks
**Challenger**
* The Impossible Dream = 42 turns (with little modification) 44 (Commited version)

**Easy**
* 01_linear_path = 4
* 02_simple_fork = 5
* 03_basic_capacity = 6

**Medium**
* 01_dead_end_trap = 8
* 02_circular_loop = 11
* 03_priority_puzzle = 7

**Hard**
* 01_maze_nightmare = 14
* 02_capacity_hell = 18
* 03_ultimate_challenge = 26

## 📚 Resources & AI Disclosure
References:

**Graph Theory:** Optimization using priority queues (heapq).
**Pygame Documentation:** Event handling and primitive rendering.
**Mathematics:** Principles of 2D Linear Interpolation.

# AI Usage Disclosure

Artificial Intelligence (Gemini/ChatGPT) was utilized as a technical consultant for the following tasks:

* **Logic & Debugging:** Debugging the complicated logical structures.
* **Architectural Iteration:** Refinement of the class structures and zone-handling logic
* **Code Quality:** Optimization of Python syntax and implementation of best practices for cleaner, more readable code.
* **Pygame Integration:** Researching efficient rendering techniques and event-loop management.
* **Mathematics & Mapping:** Developing the coordinate transformation logic to map configuration-file coordinates into screen pixels using linear scaling.

### Possible improvements
* **Simultaneous drones movement** If few drones move frome the same zone in a one directoin they overlap each other