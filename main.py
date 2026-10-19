import argparse
import os
import sys

from dotenv import load_dotenv

from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("could not retrieve API key")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()



from openai import OpenAI


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user","content": args.user_prompt},
]

#ex: bool = False
iter_num = 0

for _ in range(20):
    iter_num += 1
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,  # pyright: ignore[reportArgumentType]
        tools=available_functions,  # pyright: ignore[reportArgumentType]
    )

    message = response.choices[0].message
    messages.append(message)



    if response.usage is None:
        raise RuntimeError("No response was given")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            #if result_message['content'] == "":
            #    raise Exception("no content")  # noqa: TRY002
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
    else:
        print(message.content)
        break

        #raise Exception("no tests given")  # noqa: TRY002
if iter_num == 20:
    sys.exit(1)
