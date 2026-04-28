from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import subprocess
import webbrowser  # NEW: Built-in library for controlling the browser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# UPDATED: Ustad's brain now understands multiple action types
chat_history = [
    {
        'role': 'system',
        'content': '''You are Ustad, a local Windows AI assistant. You have two action tags you can use:
1. Local Apps: If asked to open a basic app (notepad, calc), output ONLY: [EXECUTE] app_name
2. Web/YouTube: If asked to search YouTube, play a video, or open a website, construct the URL and output ONLY: [WEB] url
Example 1: User says "Search YouTube for Vue.js tutorials". You output: [WEB] https://www.youtube.com/results?search_query=Vue.js+tutorials
Example 2: User says "Open GitHub". You output: [WEB] https://github.com
If the user is just chatting, reply normally without tags.'''
    }
]

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_with_ustad(request: ChatRequest):
    user_input = request.message
    chat_history.append({'role': 'user', 'content': user_input})
    
    try:
        response = ollama.chat(model='llama3', messages=chat_history)
        ai_reply = response['message']['content']
        
        # 1. Check for Local OS Commands
        if "[EXECUTE]" in ai_reply:
            command = ai_reply.replace("[EXECUTE]", "").replace("`", "").strip()
            print(f"[System]: Executing {command}")
            try:
                subprocess.Popen(command, shell=True)
                action_result = f"Successfully opened {command}."
            except Exception as e:
                action_result = f"Failed to open {command}. Error: {e}"
            
            chat_history.append({'role': 'assistant', 'content': ai_reply})
            chat_history.append({'role': 'system', 'content': action_result})
            return {"reply": f"Opening {command} now.", "status": "executed"}
            
        # 2. Check for Web/Browser Commands (THE NEW LOGIC)
        elif "[WEB]" in ai_reply:
            url = ai_reply.replace("[WEB]", "").replace("`", "").strip()
            print(f"[System]: Opening Web URL {url}")
            try:
                webbrowser.open(url)
                action_result = f"Successfully opened the web browser to {url}."
            except Exception as e:
                action_result = f"Failed to open browser. Error: {e}"
                
            chat_history.append({'role': 'assistant', 'content': ai_reply})
            chat_history.append({'role': 'system', 'content': action_result})
            return {"reply": f"Opening your web request now.", "status": "web_opened"}
            
        # 3. Normal Chat
        else:
            chat_history.append({'role': 'assistant', 'content': ai_reply})
            return {"reply": ai_reply, "status": "success"}
            
    except Exception as e:
        return {"reply": f"System Error: {str(e)}", "status": "error"}