import requests
import sys
import json

# --- CONFIGURATION ---
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://app.backboard.io/api"

# --- STATE VARIABLES ---
current_xp = 100
evaluator_id = None
evaluator_thread = None
solver_id = None
solver_thread = None

# --- AGENT FUNCTIONS ---
def create_agent(name, instructions):
    headers = {"X-API-Key": API_KEY}
    resp = requests.post(
        f"{BASE_URL}/assistants",
        json={"name": name, "description": instructions},
        headers=headers
    )
    if resp.status_code != 200:
        print(f"[ERROR] Creating {name}: {resp.text}")
        sys.exit()
    a_id = resp.json()["assistant_id"]
    resp_t = requests.post(
        f"{BASE_URL}/assistants/{a_id}/threads",
        json={},
        headers=headers
    )
    t_id = resp_t.json()["thread_id"]
    return a_id, t_id

def send_to_agent(thread_id, text, system_note=""):
    headers = {"X-API-Key": API_KEY}
    full_content = text
    if system_note:
        full_content = f"[SYSTEM NOTE: {system_note}] User Query: {text}"
    payload = {
        "content": full_content,
        "stream": "false",
        "memory": "Auto"
    }
    try:
        response = requests.post(
            f"{BASE_URL}/threads/{thread_id}/messages",
            headers=headers,
            data=payload
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except:
        return {"error": "Network Error"}

# --- SYSTEM INITIALIZATION ---
def init_system():
    global evaluator_id, evaluator_thread, solver_id, solver_thread
    print("\n[INIT] Initializing System and creating agents...\n")
    
    # Evaluator Agent
    eval_prompt = (
        "You are a cost evaluator. Analyze user input: "
        "If it is simple chat/greeting, reply exactly 'SIMPLE'. "
        "If it requires knowledge, work, or is a large request, reply 'COMPLEX'."
    )
    evaluator_id, evaluator_thread = create_agent("Evaluator", eval_prompt)
    print("- Evaluator Agent created")

    # Solver Agent
    solver_prompt = (
        "You are Survival AI. You track your XP. "
        "Never let XP drop below 1. "
        "Warn the user for complex tasks and ask for a single confirmation if needed. "
        "Deduct XP according to task complexity. "
        "Include XP cost in response as 'Cost: X HP'."
    )
    solver_id, solver_thread = create_agent("Solver", solver_prompt)
    print("- Solver Agent created\n")
    print("[SYSTEM READY] Let's start!\n")

# --- XP BAR ---
def draw_xp_bar(xp):
    length = 20
    fill = int(length * xp / 100)
    bar = "█" * fill + "░" * (length - fill)
    if xp < 30:
        color = "\033[91m"  # Red
    elif xp < 80:
        color = "\033[93m"  # Yellow
    else:
        color = "\033[92m"  # Green
    reset = "\033[0m"
    print(f"\nXP: [{color}{bar}{reset}] {xp:.2f}")

# --- MAIN LOOP ---
init_system()
print("=== SURVIVAL AI: ROUTING ENABLED ===")

while True:
    draw_xp_bar(current_xp)
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        print("\n[EXIT] Goodbye!")
        break

    # --- STEP 1: Evaluate Complexity ---
    print("\n[Evaluator] Assessing task complexity...")
    complexity_json = send_to_agent(evaluator_thread, user_input)
    complexity = complexity_json.get("content", "").strip().upper()
    estimated_cost = 0.01 if "SIMPLE" in complexity else None

    # --- STEP 2: Solver handles task ---
    system_note = (
        f"Current XP: {current_xp}. Estimated cost: {estimated_cost}. "
        "Manage warnings, confirmation, and XP deduction yourself. "
        "Include the XP cost in response as 'Cost: X HP'."
    )
    response_json = send_to_agent(solver_thread, user_input, system_note)
    content = response_json.get("content", "No answer")

    # Print JSON without 'content'
    json_to_print = {k: v for k, v in response_json.items() if k != "content"}
    print("\n[Solver JSON Response (without 'content')]")
    print(json.dumps(json_to_print, indent=2))

    # Print AI's actual text separately
    print(f"\n[AI]: {content}\n")

    # --- STEP 3: Determine XP cost ---
    cost_line = [line for line in content.split("\n") if "Cost:" in line]
    if cost_line:
        try:
            cost = float(cost_line[0].split("Cost:")[1].split("HP")[0].strip())
        except:
            cost = max(current_xp * 0.3, 1)
    else:
        cost = 0.01 if "SIMPLE" in complexity else max(current_xp * 0.3, 1)

    # --- STEP 4: Confirmation if AI expresses uncertainty ---
    if "sure" in content.lower() or "agree" in content.lower():
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("[AI] Request cancelled by user.\n")
            continue

    # --- STEP 5: Deduct XP ---
    if current_xp - cost < 1:
        print("⚠️ Not enough XP to complete the task. Request cancelled.")
        continue
    current_xp -= cost
    print(f"⚡ Task completed! {cost:.2f} XP spent. Current XP: {current_xp:.2f}")
