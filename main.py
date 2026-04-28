import ollama
import subprocess

def start_ustad():
    print("========================================")
    print("   Ustad System Core Online.            ")
    print("   Type 'exit' to shutdown.             ")
    print("========================================\n")
    
    # We updated the System Prompt to teach him the [EXECUTE] command
    chat_history = [
        {
            'role': 'system',
            'content': 'You are Ustad, a local Windows AI assistant. You can chat normally. IF the user asks you to open a basic Windows application (like notepad, calc, or explorer), you MUST output ONLY the command wrapped in [EXECUTE] tags. Example: [EXECUTE] notepad. Do not add any other text.'
        }
    ]
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("\nUstad: Shutting down. Goodbye.")
            break
            
        chat_history.append({'role': 'user', 'content': user_input})
        
        try:
            response = ollama.chat(model='llama3', messages=chat_history)
            ai_reply = response['message']['content']
            
            # --- THE NEW HANDS LOGIC ---
            # We check if Ustad used the secret tag
            if "[EXECUTE]" in ai_reply:
                # Clean up the text to get just the command
                command = ai_reply.replace("[EXECUTE]", "").replace("`", "").strip()
                print(f"\n[System]: Ustad is executing command: {command}...")
                
                try:
                    # subprocess.Popen runs the command without freezing the chat
                    subprocess.Popen(command, shell=True)
                    action_result = f"Successfully opened {command}."
                except Exception as e:
                    action_result = f"Failed to open {command}. Error: {e}"
                    
                print(f"[System]: {action_result}\n")
                
                # We save the action to memory so Ustad knows it worked
                chat_history.append({'role': 'assistant', 'content': ai_reply})
                chat_history.append({'role': 'system', 'content': action_result})
                
            else:
                # If there's no tag, just chat normally
                print(f"\nUstad: {ai_reply}\n")
                chat_history.append({'role': 'assistant', 'content': ai_reply})
            
        except Exception as e:
            print(f"\n[System Error]: {e}\n")

if __name__ == "__main__":
    start_ustad()