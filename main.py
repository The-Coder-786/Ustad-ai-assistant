import ollama

def test_brain():
    print("Sending message to Ustad...")
    
    # We send a simple prompt to the Llama 3 model
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': 'Hello! Are you ready to control this system?',
        },
    ])
    
    # Print the response from the AI
    print("\nUstad says:")
    print(response['message']['content'])

if __name__ == "__main__":
    test_brain()