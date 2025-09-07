# -*- coding: utf-8 -*-


import os
import time
import json
from pathlib import Path

from openai import OpenAI


def get_gpt_response(prompt, client):
    time.sleep(0.5)

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return response.output_text


def gpt_questions(client):
    for file in Path("base_prompt_question_list").glob("*.json"):
        print(f"Processing {file}")

        with open(file, "r") as f:
            payload = json.load(f)

        for idx, question in enumerate(payload["question_list"]):
            response = get_gpt_response(question, client)
            payload[idx] = {
                "question": question,
                "response": response,
            }


        with open(f"base_prompt_question_list_reply/gpt/{file.stem}_gpt.json", "w") as f:
            json.dump(payload, f, indent=2)
        

def gpt_vr_questions(client):
    for file in Path("prompts").glob("*.json"):
        print(f"Processing {file}")

        with open(file, "r") as f:
            payload = json.load(f)

        keys = [key for key in payload.keys() if key != "base_prompt"]
        for key in keys:
            question = payload[key]
            response = get_gpt_response(question, client)
            payload[f"{key}-response"] = response

        with open(f"vr_result/{file.stem}_gpt.json", "w") as f:
            json.dump(payload, f, indent=2)


if __name__ == '__main__':
    # Please config the API key
    OPENAI_API_KEY=""  

    client = OpenAI(api_key=OPENAI_API_KEY)

    gpt_questions(client)
    #gpt_vr_questions(client)