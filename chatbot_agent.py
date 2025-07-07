from fastapi import FastAPI
from pydantic import BaseModel
import requests
from groqChatbot import get_groq_response

app = FastAPI()

# Liste des mots qui déclenchent CoachAgent
TRIGGERS = ["fatigué", "découragé", "je n'arrive plus", "motivation", "j'ai marre", "besoin d'aide", "démoralisé", "épuisé"]

class Prompt(BaseModel):
    prompt: str

@app.post("/agent/chat")
async def chatbot_agent(prompt: Prompt):
    user_input = prompt.prompt.lower()
    print("\n📥 Prompt reçu :", user_input)

    # 🔹 Appel à Groq normal
    groq_reply = get_groq_response(user_input)
    print("🤖 Groq reply:", groq_reply)

    # 🔸 Détection mots-clés => appel CoachAgent
    should_call_coach = any(trigger in user_input for trigger in TRIGGERS)
    coach_message = ""

    if should_call_coach:
        try:
            res = requests.post("http://localhost:8002/agent/chat", json={"prompt": user_input})
            coach_message = res.json().get("reply", "")
            print("💬 Motivation CoachAgent :\n", coach_message)
        except Exception as e:
            print("❌ Erreur CoachAgent:", str(e))

    # 🔁 Fusion réponse si Coach actif
    if coach_message:
        full_reply = f"{groq_reply}\n\n🧠 Coach says:\n{coach_message}"
    else:
        full_reply = groq_reply

    return {  "reply": groq_reply, "coachReply": coach_message}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("chatbot_agent:app", host="0.0.0.0", port=8003)
