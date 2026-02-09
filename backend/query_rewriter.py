import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


# =========================
# CONFIG (ENV BASED)
# =========================
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL
)

# =========================
# QUERY REWRITER
# =========================
def rewrite_query(user_query: str) -> str:
    """
    Corrects spelling errors and structures vague jewellery queries
    without adding new attributes or intent.
    """

    if not user_query or len(user_query.strip()) < 3:
        return user_query

    prompt = f"""You are a query refinement assistant for a jewellery retrieval system.

Your task is to transform user queries into positive, descriptive sentences optimized for image retrieval embeddings.

Strict Rules:
1. ABSOLUTELY NO NEGATIVE WORDS: The output must not contain words like "no", "without", "except", "not", or "minus".
2. AFFIRMATIVE TRANSFORMATION: Convert negative constraints into positive attributes (e.g., "without stones" -> "plain", "no pendant" -> "standalone", "without engravings" -> "smooth").
3. SPELLING & STRUCTURE: Fix typos and format the query as "[Attribute] [Object]" (e.g., "Gold ring").
4. NO ADDED INFORMATION: Do not invent materials or styles that weren't in the original query.
5. MINIMALISM: Keep the rewrite as short as possible.
6. Output ONLY the rewritten sentence.
7.Rewritten query should not contain any word mentioned with negative intent , not even with meaning changing suffixes like less or free
8.You can intentionally change the direction of the query just to make sure the negatives are avoided.
eg.rings wihout red can be changed to yellow or green rings just so red rings are avoided.
9.Give the complete opposite query for nrgative wordings

User query: "{user_query}"
"""

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            temperature=0.0,
            max_tokens=50
        )

        rewritten = response.choices[0].message.content.strip()
        return rewritten if rewritten else user_query

    except Exception as e:
        print(f"[QueryRewriter] Fallback used: {e}")
        return user_query