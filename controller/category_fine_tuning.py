import openai
from openai import OpenAI
import os
from category_json_control import category_json_update
from dotenv import load_dotenv
load_dotenv()

def category_fine_tuning():
    file_id = category_json_update()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    job = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-4o-2024-08-06",
    )
    print(f'job :: {job}')
    return job

#category_fine_tuning()