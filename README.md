# Survival AI: The Stingy Agent 🛡️💰

**Built for Backboard.io Challenge**

### 💡 The Concept
LLMs are expensive. Most agents ignore cost. **Survival AI** treats its API credits as "Health Points" (HP). It is aware of its own mortality.
- It **negotiates** before answering complex questions to save HP.
- It **refuses** work if it's dying (Low HP).
- It uses **Backboard Agents** to route tasks based on complexity.

### ⚙️ How it works (Backboard Integration)
The project utilizes the **Backboard API** to spawn two distinct agents:
1.  **The Evaluator (Router):** A low-cost agent that analyzes input complexity (Simple vs Complex).
2.  **The Solver:** The main agent that answers user queries.

### 🚀 Features
-   **Dynamic HP System:** Every token costs "life".
-   **Agentic Routing:** Automatically detects task difficulty to estimate cost.
-   **Personality Shift:**
    -   High HP: Friendly & Helpful.
    -   Low HP: Rude, panic-stricken, and brief (to save tokens).
-   **Visual Interface:** Real-time CLI health bar.

### 🛠️ Tech Stack
-   Python 3
-   Backboard API (Agents & Threads)
