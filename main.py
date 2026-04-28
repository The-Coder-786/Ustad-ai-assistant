import ollama

def start_ustad():
    print("========================================")
    print("   Ustad System Core Online.            ")
    print("   Type 'exit' to shutdown.             ")
    print("========================================\n")
    
    # The System Prompt tells the AI who it is and how to behave
    chat_history = [
        {
            'role': 'system',
            'content': 'You are Ustad, a highly intelligent and concise AI assistant running locally on a Windows laptop. Your goal is to help the user manage their system, write code, and solve technical problems. Keep your answers brief, professional, and directly to the point.'
        }
    ]
    
    # The Infinite Loop keeps the conversation going
    while True:
        # 1. Get your input
        user_input = input("You: ")
        
        # 2. Check if you want to quit
        if user_input.lower() in ['exit', 'quit']:
            print("\nUstad: Shutting down. Goodbye.")
            break
            
        # 3. Add your message to the memory
        chat_history.append({'role': 'user', 'content': user_input})
        
        # 4. Send the memory to the Brain
        try:
            response = ollama.chat(model='llama3', messages=chat_history)
            ai_reply = response['message']['content']
            
            # 5. Print Ustad's reply
            print(f"\nUstad: {ai_reply}\n")
            
            # 6. Add Ustad's reply to the memory so he remembers it for next time
            chat_history.append({'role': 'assistant', 'content': ai_reply})
            
        except Exception as e:
            print(f"\n[System Error]: {e}\n")

if __name__ == "__main__":
    start_ustad()