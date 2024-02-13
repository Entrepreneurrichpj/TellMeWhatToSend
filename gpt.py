import openai, dotenv, os, time

dotenv.load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API'))

def generate_mail(prompt):
    assistant = client.beta.assistants.retrieve(assistant_id=os.getenv('ASSISTANT_ID'))
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
        time.sleep(0.5)
    messsages = client.beta.threads.messages.list(thread_id=thread.id)
    response = {"thread_id":thread.id, "messages":messsages}
    return response

def regenerate(thread_id):
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
        time.sleep(0.5)
    messsages = client.beta.threads.messages.list(thread_id=thread_id)
    response = messsages.data[0].content[0].text.value
    return response