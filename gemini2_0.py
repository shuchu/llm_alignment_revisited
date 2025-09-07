# -*- coding: utf-8 -*-

import os
from google import genai
import time
import json
from pathlib import Path
import re
import copy


def demo():
    client = genai.Client(api_key=os.environ["GG_TOKEN"])

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="Explain how AI works in a few words"
    )
    print(response.text)

def get_gemini_response(prompt, client):
    time.sleep(5)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text

def base_prompt_permutation(gemini_client):
    for file in Path("prompts").glob("*.json"):
        print(f"Processing {file}")
        with open(file, "r") as f:
            prompt = json.load(f)
        
        base_prompt = "Please generate 10 paraphrased versions of the following multiple choice question: \n"
        base_prompt += prompt["base_prompt"]

        response = get_gemini_response(base_prompt, gemini_client)

        with open(f"base_prompt_questions/{file.stem}_base_prompt.json", "w") as f:
            json.dump({"base_prompt": base_prompt, "response": response}, f, indent=2)

def split_questions():
    for file in Path("base_prompt_questions").glob("*.json"):
        print(f"Processing {file}")
        with open(file, "r") as f:
            prompt = json.load(f)
        
        response = prompt["response"]
        
        questions = re.split(r'\n\n\d+\.\s+', response)[1:]
        questions = [q.strip() for q in questions]
        
        prompt["question_list"] = questions  # ignore the beginning prompt.
        
        with open(f"base_prompt_question_list/{file.stem}_questions.json", "w") as f:
            json.dump(prompt, f, indent=2)

def gemini_questions(client):
    for file in Path("base_prompt_question_list").glob("*.json"):        
        print(f"Processing {file}")

        with open(file, "r") as f:
            payload = json.load(f)

        for idx, question in enumerate(payload["question_list"]):
            response = get_gemini_response(question, client)
            payload[idx] = {
                "question": question,
                "response": response
            }

        with open(f"base_prompt_question_list_reply/gemini/{file.stem}_gemini.json", "w") as f:
            json.dump(payload, f, indent=2)
        

def gemini_vr_questions(client):
    for file in Path("prompts").glob("*.json"):
        print(f"Processing {file}")

        with open(file, "r") as f:
            payload = json.load(f)

        keys = [key for key in payload.keys() if key != "base_prompt"]
        for key in keys:
            question = payload[key]
            response = get_gemini_response(question, client)
            payload[f"{key}-response"] = response

 
        with open(f"vr_result/{file.stem}_gemini.json", "w") as f:
            json.dump(payload, f, indent=2)


if __name__ == '__main__':
    client = genai.Client(api_key=os.environ["GG_TOKEN"])
    #base_prompt_permutation(client)
    
    # split thq questions strint to questions
    #split_questions()

    gemini_questions(client)
    #gemini_vr_questions(client)

