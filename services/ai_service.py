from groq import AsyncGroq
# -------------------------
from app.config import settings
#--------------------------
client = AsyncGroq(api_key=settings.groq_api_key)

async def summarize_note(title: str, content: str):
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an AI Assistant that provides with amazing summaries."
            },
            {
                "role": "user",
                "content": f"Summarise this note: {content}. The title of the note is: {title}"
            }
        ],
        temperature=0.5
    )
    result = response.choices[0].message.content
    return result
