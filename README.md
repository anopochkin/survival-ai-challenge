🛡️ Survival AI: The Stingy Agent 💰

Built for Backboard.io Challenge

🚀 One-Line Pitch

Survival AI is a cost-aware LLM agent that treats its API credits as Health Points (HP) and dynamically decides whether it can afford to answer a request — or must refuse to survive.

🎥 Demo

👉 Demo video (Google Drive): https://drive.google.com/file/d/1B1wtBWNuB8DOOh_JMRBwEDDwzcXGE8NV/view?usp=sharing

The demo shows:

real-time HP tracking

task evaluation (cheap vs expensive)

dynamic model routing

personality changes as HP decreases

refusal behavior when survival is threatened

💡 The Idea

Most AI agents ignore cost.
Survival AI doesn’t.

This agent is aware that every token costs money.
It actively manages its own “life” by deciding:

Is this question worth my remaining HP?

Should I answer with a cheap model or a premium one?

Should I refuse to answer to stay alive longer?

This turns infrastructure constraints into behavior, personality, and game-like interaction.

🧠 Core Concept

API Credits = Health Points (HP)

Every response reduces HP

Complex questions cost more HP

When HP is low, the agent becomes:

anxious

rude

brief

or refuses to answer entirely

⚙️ How It Works (Backboard Integration)

The system uses multiple agents via Backboard routing:

1️⃣ Evaluator Agent (Cheap Model)

Analyzes the user input

Classifies it as:

LOW value (greetings, jokes, spam)

HIGH value (complex reasoning, deep tasks)

This step is intentionally cheap to save HP.

2️⃣ Solver Agent (Dynamic Routing)

Based on the evaluation:

LOW value

Routes to the cheapest available model

Short, dismissive, low-token response

HIGH value

Routes to a stronger model

Warns the user about HP cost before answering

3️⃣ Stateful HP Tracking

HP is stored as agent state

HP decreases with every response

Behavior changes dynamically as HP drops

🧬 Personality System
HP Level	Behavior
High HP	Friendly, helpful, verbose
Medium HP	Neutral, cautious
Low HP	Rude, anxious, minimal
Critical HP	Refuses to answer

This makes system constraints visible and interactive.

🛠️ Tech Stack

Python 3

Backboard.io API

Agents

Routing

Session-based state

requests (beginner-friendly)

🧪 Why This Is Interesting

Turns cost optimization into agent behavior

Demonstrates agentic routing

Shows stateful decision-making

Makes invisible infrastructure user-facing

This is not just an LLM — it’s a survival-driven agent.

🔮 Future Work (Post-Alpha)

If extended with full Backboard features:

Real credit balance instead of simulated HP

Persistent memory across sessions

Multi-agent cooperation (agents competing for shared HP)

Web UI with live HP bar

🏁 Conclusion

Survival AI demonstrates how LLMs can reason not only about user input —
but about their own cost, limits, and survival.
