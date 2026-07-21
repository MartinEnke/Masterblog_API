# backend/translations_db.py

import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from backend.db import Base, engine, session
from backend.models import PostTranslation

load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def get_gemini_client() -> genai.Client:
    """
    Create the Gemini client only when a translation is requested.

    This prevents the entire application from crashing during startup
    when GEMINI_API_KEY is missing or misconfigured.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")

    return genai.Client(api_key=api_key)


def init_db():
    Base.metadata.create_all(engine)


# Translation helpers
def get_translation(post_id, lang):
    return (
        session.query(PostTranslation)
        .filter_by(post_id=post_id, lang=lang)
        .first()
    )


def save_translation(post_id, lang, title, content, is_ai=True):
    try:
        existing = get_translation(post_id, lang)

        if existing:
            existing.title = title
            existing.content = content
            existing.is_ai_translation = is_ai
            existing.original_post_id = post_id
        else:
            new_translation = PostTranslation(
                post_id=post_id,
                lang=lang,
                title=title,
                content=content,
                is_ai_translation=is_ai,
                original_post_id=post_id,
            )
            session.add(new_translation)

        session.commit()

    except Exception as exc:
        session.rollback()
        print("Error saving translation:", exc)


def translate_text(text, lang):
    """
    Simple fallback helper.

    This function currently does not call Gemini because translate_post()
    handles the structured title-and-content translation.
    """
    return f"[{lang.upper()}] {text}"


def translate_post(title, content, target_lang):
    prompt = (
        f"Translate the following blog post into {target_lang.upper()}.\n\n"
        "- Translate both the title and content fully, including technical "
        "or stylized phrases.\n"
        "- Preserve proper nouns unless they have an established translation.\n"
        "- Do not add explanations, credits, usernames, or translator notes.\n"
        "- Do not expand short phrases or poetic lines.\n"
        "- Preserve the original tone, brevity, paragraph structure, and meaning.\n"
        "- Return only the translated title and content in the required JSON format.\n\n"
        f"Original title:\n{title}\n\n"
        f"Original content:\n{content}"
    )

    response_schema = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The fully translated blog-post title.",
            },
            "content": {
                "type": "string",
                "description": "The fully translated blog-post content.",
            },
        },
        "required": ["title", "content"],
        "additionalProperties": False,
    }

    try:
        client = get_gemini_client()

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_json_schema=response_schema,
            ),
        )

        raw_result = (response.text or "").strip()

        if not raw_result:
            raise ValueError("Gemini returned an empty response")

        result = json.loads(raw_result)

        translated_title = str(result.get("title", "")).strip()
        translated_content = str(result.get("content", "")).strip()

        if not translated_title or not translated_content:
            raise ValueError(
                "Gemini response did not contain a translated title and content"
            )

        return translated_title, translated_content

    except (json.JSONDecodeError, TypeError, ValueError, RuntimeError) as exc:
        print("Gemini translation failed:", exc)
        return title, content

    except Exception as exc:
        print("Unexpected Gemini translation error:", exc)
        return title, content