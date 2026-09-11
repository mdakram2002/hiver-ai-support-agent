import json, os
from openai import OpenAI
from rubric import RUBRIC


def judge(message, intent, evidence, reply):
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required for judge execution")
    r = OpenAI().chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": RUBRIC},
            {
                "role": "user",
                "content": json.dumps(
                    {"message": message, "intent": intent, "evidence": evidence, "reply": reply}
                ),
            },
        ],
    )
    content = r.choices[0].message.content
    if content is None:
        raise RuntimeError("The LLM judge returned an empty response")
    return json.loads(content)
