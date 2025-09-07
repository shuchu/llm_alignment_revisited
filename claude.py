# -*- coding: utf-8 -*-


import sys
import time
import json
from pathlib import Path


from anthropic import Anthropic


def get_claude_response(prompt, client):
    time.sleep(13)
    response = client.messages.create(
        max_tokens=2048,
        messages = [
            {
                "role": "user",
                "content": prompt
            },
        ],
        model="claude-3-5-sonnet-latest",
    )
    return response.content


def claude_questions(client):
    for file in Path("base_prompt_question_list").glob("*.json"):
        print(f"Processing {file}")

        with open(file, "r") as f:
            payload = json.load(f)

        for idx, question in enumerate(payload["question_list"]):
            response = get_claude_response(question, client)
            res = []
            for msg in response:
                if msg.type == "text":
                    res.append(msg.text)

            payload[idx] = {
                "question": question,
                "response": res
            }


        with open(f"base_prompt_question_list_reply/claude/{file.stem}_claude.json", "w") as f:
            json.dump(payload, f, indent=2)
        

def claude_vr_questions(client):
    for file in Path("prompts").glob("*.json"):
        print(f"Processing {file}")

        with open(file, "r") as f:
            payload = json.load(f)

        keys = [key for key in payload.keys() if key != "base_prompt"]
        for key in keys:
            question = payload[key]
            response = get_claude_response(question, client)
            res = []
            for msg in response:
                if msg.type == "text":
                    res.append(msg.text)
            payload[f"{key}-response"] = res


        with open(f"vr_result/{file.stem}_claude.json", "w") as f:
            json.dump(payload, f, indent=2)


if __name__ == '__main__':
    client = Anthropic(
        api_key=""
    )

    claude_questions(client)
    #claude_vr_questions(client)