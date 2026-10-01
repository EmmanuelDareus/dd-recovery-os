import os
import subprocess
from pathlib import Path
import ollama

# Define your local workspace path
VAULT_PATH = Path(r"C:\Users\gamin\OneDrive\Desktop\Documents\Obsidian Vault")

def list_vault_notes() -> str:
    """Lists all markdown notes available in the Obsidian vault."""
    if not VAULT_PATH.exists():
        return "Error: Vault path not found."
    notes = [f.relative_to(VAULT_PATH).as_posix() for f in VAULT_PATH.glob("**/*.md")]
    return f"Found notes: {notes}"

def read_vault_note(filename: str) -> str:
    """Reads the contents of a specific markdown note."""
    file_path = VAULT_PATH / filename
    if not file_path.exists():
        return f"Error: Note '{filename}' does not exist."
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_vault_note(filename: str, content: str) -> str:
    """Creates or updates a markdown note in the vault."""
    file_path = VAULT_PATH / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Success: Wrote to {filename}"

def run_command(command: str) -> str:
    """Executes a local terminal command safely."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
        output = result.stdout if result.returncode == 0 else result.stderr
        return output.strip()
    except Exception as e:
        return f"Execution error: {str(e)}"

# Map available tool names to actual functions
TOOLS = {
    "list_vault_notes": list_vault_notes,
    "read_vault_note": read_vault_note,
    "write_vault_note": write_vault_note,
    "run_command": run_command
}

def main():
    print("--- VaultAgent Initialized (Local & Free) ---")
    model = "llama3" 
    
    messages = [
        {
            "role": "system", 
            "content": (
                "You are VaultAgent, a local AI assistant. You have direct access to Python functions "
                "to interact with the user's Obsidian vault and local terminal. "
                "When you need to use a tool, explain what you are doing."
            )
        }
    ]

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Shutting down VaultAgent. Goodbye!")
                break

            if not user_input.strip():
                continue

            messages.append({"role": "user", "content": user_input})

            response = ollama.chat(model=model, messages=messages)
            reply = response['message']['content']
            
            print(f"\nVaultAgent: {reply}")
            
            # Explicitly append the assistant response dictionary
            messages.append({"role": "assistant", "content": reply})

        except KeyboardInterrupt:
            print("\nExiting VaultAgent.")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
    