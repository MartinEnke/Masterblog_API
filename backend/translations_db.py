# translations_db.py
from sqlalchemy import Column, Integer, String, UniqueConstraint, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from backend.db import Base, engine, session
from backend.models import Post
import os
from dotenv import load_dotenv
from openai import OpenAI
from backend.models import PostTranslation
load_dotenv()  # Loads .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# client = OpenAI(
#     api_key=os.getenv("TOGETHER_AI_KEY"),
#     base_url="https://api.together.xyz/v1"
# )


def init_db():
    Base.metadata.create_all(engine)

# Translation helpers
def get_translation(post_id, lang):
    return session.query(PostTranslation).filter_by(post_id=post_id, lang=lang).first()

def save_translation(post_id, lang, title, content, is_ai=True):
    try:
        existing = get_translation(post_id, lang)
        if existing:
            existing.title = title
            existing.content = content
            existing.is_ai_translation = is_ai
            existing.original_post_id = post_id
        else:
            new = PostTranslation(
                post_id=post_id,
                lang=lang,
                title=title,
                content=content,
                is_ai_translation=is_ai,
                original_post_id=post_id
            )
            session.add(new)

        session.commit()  # ← added this
    except Exception as e:
        print("❌ Error saving translation:", e)



def translate_text(text, lang):
    # 🔁 Replace with OpenAI or DeepL later
    return f"[{lang.upper()}] {text}"

def translate_post(title, content, target_lang):
    prompt = (
        f"Translate the following blog post into {target_lang.upper()}.\n\n"
        f"- Translate both the title and the content fully, even if they contain technical or stylized phrases.\n"
        f"- Do not skip words that seem like proper nouns unless they are truly universal (e.g., 'AI').\n"
        f"- Do not add explanations, credits, usernames, or translator notes.\n"
        f"- Do not expand short phrases or poetic lines.\n"
        f"- Maintain brevity, tone, and sentence structure.\n"
        f"- Your output must **only** include the translated title and content.\n\n"
        f"Title:\n{title}\n\nContent:\n{content}"
    )


    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        # response = client.chat.completions.create(
        #     model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0.7
        # )

        result = response.choices[0].message.content.strip()
        print("📤 AI raw response:\n", repr(result))

        # Look for multiple variants of "title" and "content"
        title_markers = ["Title:", "Titre :", "Título:", "Titel:"]
        content_markers = ["Content:", "Contenu :", "Contenido:", "Inhalt:"]

        for t in title_markers:
            if t in result:
                for c in content_markers:
                    if c in result:
                        new_title = result.split(t)[1].split(c)[0].strip()
                        new_content = result.split(c)[1].strip()
                        return new_title, new_content

        # Fallback to entire response
        return title, result

    except Exception as e:
        print("❌ AI translation failed:", e)
        return title, content

