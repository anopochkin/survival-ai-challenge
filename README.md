# 🛡️ Survival AI: The XP-Aware Agent 💰

Built for **Backboard.io Challenge**

---

## 🚀 One-Line Pitch

**Survival AI** is a cost-aware LLM agent that treats its API credits as **Experience Points (XP)** and dynamically decides whether it can afford to answer a request — or must refuse to survive.

---

## 🎥 Demo

👉 **[Watch the demo on Google Drive](https://drive.google.com/file/d/1B1wtBWNuB8DOOh_JMRBwEDDwzcXGE8NV/view?usp=sharing)**

### The demo shows:
- real-time XP tracking  
- task evaluation (cheap vs expensive)  
- dynamic model routing  
- personality changes as XP decreases  
- refusal behavior when survival is threatened  

---

## 💡 The Idea

Most AI agents ignore cost.  
**Survival AI doesn’t.**

This agent is aware that every token costs money.  
It actively manages its own “life” by deciding:

- Is this question worth my remaining XP?  
- Should I answer with a cheap model or a premium one?  
- Should I refuse to answer to stay alive longer?

This turns infrastructure constraints into **behavior, personality, and game-like interaction**.

---

## 🧠 Core Concept

- **API Credits = Experience Points (XP)**  
- Every response reduces XP  
- Complex questions **dynamically consume more XP**, sometimes a large fraction of total XP  
- Simple tasks cost ~0.01 XP  

When XP is low, the agent becomes:
- anxious  
- terse  
- dismissive  
- or refuses to answer entirely  

---

## ⚙️ How It Works (Backboard Integration)

The system uses multiple agents via **Backboard routing**.

### 1️⃣ Evaluator Agent (Cheap Model)
- Analyzes the user input  
- Classifies it as:
  - **LOW value** (greetings, jokes, spam)  
  - **HIGH value** (complex reasoning, deep tasks)

This step is intentionally cheap to save XP.

---

### 2️⃣ Solver Agent (Dynamic Routing)

Based on evaluation:

**LOW value**
- Routes to the cheapest available model  
- Short, dismissive, low-token response (~0.01 XP)

**HIGH value**
- Routes to a stronger model  
- Warns the user about potential XP cost (can consume large portion of XP)  
- Requests a **single confirmation**  
- Executes the task and deducts XP accordingly  

---

### 3️⃣ Stateful XP Tracking
- XP is stored as agent state  
- XP decreases with every response  
- Behavior changes dynamically as XP drops  

---

## 🧬 Personality System

| XP Level      | Behavior                          |
|---------------|----------------------------------|
| High XP       | Friendly, helpful, verbose       |
| Medium XP     | Neutral, cautious                |
| Low XP        | Rude, anxious, minimal           |
| Critical XP   | Refuses to answer                |

XP is now **dynamic**, so a single complex task may consume a large fraction of the agent’s total XP.

---

## 🛠️ Tech Stack

- Python 3  
- Backboard.io API  
  - Agents  
  - Routing  
  - Session-based state  
- `requests` (beginner-friendly)  

---

## 🧪 Why This Is Interesting

- Turns cost optimization into **agent behavior**  
- Demonstrates **dynamic routing based on task complexity**  
- Shows **stateful decision-making**  
- Makes invisible infrastructure user-facing  

This is not just an LLM — **it’s a survival-driven agent with XP mechanics**.

---

## 🔮 Future Work (Post-Alpha)

If extended with full Backboard features:
- Real credit balance instead of simulated XP  
- Persistent memory across sessions  
- Multi-agent cooperation (agents competing for shared XP)  
- Web UI with live XP bar  

---

## 🏁 Conclusion

**Survival AI** demonstrates how LLMs can reason not only about user input —  
but about their own **cost, limits, and survival strategy** in a gamified XP system.

