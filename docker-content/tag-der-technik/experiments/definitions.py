import re
from typing import Optional

from openai import OpenAI

client = OpenAI(api_key="blah", base_url="https://llm.srv.webis.de/v1")


def fetch_completion(systemprompt: Optional[str], userprompt: str, examples: list[tuple[str, str]] = []):
    messages = [{"role": "system", "content": systemprompt}] if systemprompt is not None else []
    for input, output in examples:
        messages.extend([{"role": "user", "content": input}, {"role": "assistant", "content": output}])
    messages.append({"role": "user", "content": userprompt})
    completion = client.chat.completions.create(
        model="default",
        messages=messages,
        # temperature=0,
        max_completion_tokens=200,
    )
    return completion.choices[0].message.content


def fetch_response(inp: str) -> str:
    resp = fetch_completion(None, inp)
    try:
        resp = extract_between(resp, "<Response>", "</Response>")
    except:
        pass
    return resp


def extract_between(input: str, left_delim: str, right_delim: str):
    return re.findall(rf'{left_delim}(.*?){right_delim}', input, re.MULTILINE | re.DOTALL)[0]