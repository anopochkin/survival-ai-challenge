import requests
import sys
import time

# --- CONFIGURATION ---
API_KEY = "YOUR_API_KEY_HERE" 
BASE_URL = "https://app.backboard.io/api"

# --- STATE VARIABLES ---
current_hp = 100
evaluator_id = None
evaluator_thread = None
solver_id = None
solver_thread = None

def create_agent(name, instructions):
    """Creates a Backboard Agent with specific instructions."""
    headers = {"X-API-Key": API_KEY}
    
    # 1. Create Assistant
    resp = requests.post(
        f"{BASE_URL}/assistants",
        json={"name": name, "description": instructions},
        headers=headers
    )
    if resp.status_code != 200:
        print(f"Error creating {name}: {resp.text}")
        sys.exit()
    a_id = resp.json()["assistant_id"]
    
    # 2. Create Thread
    resp_t = requests.post(
        f"{BASE_URL}/assistants/{a_id}/threads",
        json={},
        headers=headers
    )
    t_id = resp_t.json()["thread_id"]
    return a_id, t_id

def send_to_agent(thread_id, text, system_note=""):
    """Sends a message to the specific agent thread."""
    headers = {"X-API-Key": API_KEY}
    
    # Inject system note if provided (e.g., for low HP behavior)
    full_content = text
    if system_note:
        full_content = f"[SYSTEM INSTRUCTION: {system_note}] User Query: {text}"

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
            return response.json().get("content", "...")
        else:
            return "API Error"
    except:
        return "Network Error"

def init_system():
    global evaluator_id, evaluator_thread, solver_id, solver_thread
    print("Initializing System (Creating Agents)...")
    
    # 1. The Evaluator (Router)
    # Task: Output only SIMPLE or COMPLEX
    print("- Creating Evaluator Agent...")
    eval_prompt = "You are a cost estimator. Analyze user input. If it is simple chat/greeting, reply exactly 'SIMPLE'. If it requires knowledge or work, reply 'COMPLEX'."
    evaluator_id, evaluator_thread = create_agent("Evaluator", eval_prompt)
    
    # 2. The Solver (Main AI)
    print("- Creating Solver Agent...")
    solver_prompt = "You are a helpful assistant. Keep answers concise."
    solver_id, solver_thread = create_agent("Solver", solver_prompt)
    
    print("System Ready.")

def draw_hp_bar(hp):
    length = 20
    fill = int(length * hp / 100)
    bar = "█" * fill + "░" * (length - fill)
    print(f"\nHP: [{bar}] {hp}%")

# --- MAIN LOOP ---
init_system()

print("=== SURVIVAL AI: ROUTING ENABLED ===")

while True:
    draw_hp_bar(current_hp)
    
    if current_hp <= 0:
        print("Battery depleted. System Shutdown. Game Over.")
        break

    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # STEP 1: Evaluation (Routing)
    print("...Evaluating Cost (Routing)...")
    complexity = send_to_agent(evaluator_thread, user_input)
    complexity = complexity.strip().upper()
    
    cost = 0
    note = ""
    
    # Logic based on complexity
    if "COMPLEX" in complexity:
        cost = 15
        print(f"(!) High Cost Task detected. Cost: {cost} HP")
        confirm = input("Proceed? (y/n): ")
        if confirm.lower() != 'y':
            print("Action cancelled.")
            continue
    else:
        cost = 5
        print(f"(i) Low Cost Task. Cost: {cost} HP")

    # Deduct HP
    current_hp -= cost
    
    # STEP 2: Execution & Personality Shift
    if current_hp < 30:
        note = "WARNING: HP is critical (<30%). You are panicked, rude, and brief. Complain about low battery."
    elif current_hp > 80:
        note = "HP is full. Be extremely friendly and enthusiastic."
    else:
        note = "HP is normal. Be helpful and polite."

    print("Generating Answer...")
    answer = send_to_agent(solver_thread, user_input, note)
    print(f"AI: {answer}")