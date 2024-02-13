import sys
import tkinter
import openai, dotenv, os, time

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

dotenv.load_dotenv(resource_path('.env'))

client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API'))



def generate_mail(prompt, gpt_response):
    try:
        assistant = client.beta.assistants.retrieve(assistant_id=os.getenv('ASSISTANT_ID'))
        print(assistant.id)
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role='user',
            content=prompt
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        while run.status != 'completed':
            run = client.beta.threads.runs.retrieve(
                thread_id = thread.id,
                run_id = run.id
            )
            gpt_response.insert(tkinter.END, f'\n{run.status}')
            time.sleep(0.5)
        messsages = client.beta.threads.messages.list(thread_id=thread.id)
        response = {"thread_id":thread.id, "messages":messsages}
        return response
    except openai.OpenAIError as e:
        print(e)
        return None


def regenerate(thread_id, gpt_response):
    try:
        assistant = client.beta.assistants.retrieve(assistant_id=os.getenv('ASSISTANT_ID'))
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role='user',
            content="can you regenerate this email in a different style?"
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant.id
        )
        while run.status != 'completed':
            run = client.beta.threads.runs.retrieve(
                thread_id = thread_id,
                run_id = run.id
            )
            gpt_response.insert(tkinter.END, f'\n{run.status}')
            time.sleep(0.5)
        messsages = client.beta.threads.messages.list(thread_id=thread_id)
        response = messsages.data[0].content[0].text.value
        return response
    except openai.OpenAIError as e:
        return None