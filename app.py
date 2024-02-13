import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading
import gpt

thread_id = ''

def fetch_gpt_response(user_query):
    global thread_id
    gpt_json = gpt.generate_mail(user_query)
    thread_id = gpt_json['thread_id']
    response = gpt_json['messages'].data[0].content[0].text.value
    root.after(0, lambda: update_gpt_response(response))

def refresh_gpt_response():
    gpt_response.insert(tk.END, "Regenerating the response...\n正在重新生成邮件，请稍等...")
    response = gpt.regenerate(thread_id)
    root.after(0, lambda: update_gpt_response(response))

def update_gpt_response(response):
    gpt_response.delete(1.0, tk.END)
    gpt_response.insert(tk.END, response)
    update_refresh_button()

def submit_query():
    if to_entry.get() == '':
        gpt_response.delete(1.0, tk.END)
        gpt_response.insert(tk.END, "Please tell me who is this for...\n请告诉这是写给谁的...")    
        return
    if from_entry.get() == '':
        gpt_response.delete(1.0, tk.END)
        gpt_response.insert(tk.END, "Please tell me your name...\n请告诉我你的名字...")    
        return
    if user_input.get() == '':
        gpt_response.delete(1.0, tk.END)
        gpt_response.insert(tk.END, "Please tell me what you want first...\n请先告诉我你想要写什么...")    
        return
    user_query = f'This is a email from {from_entry.get()} to {to_entry.get()}, {user_input.get()}'
    print(f"Query submitted: {user_query}")    
    gpt_response.delete(1.0, tk.END)
    gpt_response.insert(tk.END, "Got it, please wait while I'm generating the response...\n正在生成邮件，请稍等...")
    user_input.delete(0, tk.END)
    threading.Thread(target=fetch_gpt_response, args=(user_query,)).start()

def update_refresh_button():
    if thread_id != '':
        refresh_button.place(relx=1, rely=1, x=-18, y=-4, anchor="se", in_=gpt_response)
    else:
        refresh_button.place_forget()

def resize_icon(path, new_width, new_height):
    image = Image.open(path)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

root = tk.Tk()
root.title("Tell me what to send")

root.columnconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.minsize(400, 300)
root.bind('<Return>', lambda event=None: submit_query())

# LOAD ICONS
refresh_icon = resize_icon('./Images/refresh.png', 24, 24)
submit_icon = resize_icon('./Images/enter.png', 24, 24)

# 'To' AND 'From' FIELDS
tk.Label(root, text="To:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
to_entry = tk.Entry(root)
to_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

tk.Label(root, text="From:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
from_entry = tk.Entry(root)
from_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

# GPT text generation field
gpt_response = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
gpt_response.grid(row=2, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
gpt_response.insert(tk.END, 'I will tell you what to send...\n我会告诉你怎么写...')

# Refresh button for GPT text field
refresh_button = tk.Button(root, image=refresh_icon, borderwidth=0, highlightthickness=0, bg='white', command=lambda: threading.Thread(target=refresh_gpt_response).start())

# update_refresh_button()

# User input field
user_input = tk.Entry(root)
user_input.grid(row=4, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

# Submit button for user input
submit_button = tk.Button(root, image=submit_icon, highlightthickness=0, command=submit_query)
submit_button.grid(row=4, column=2, sticky='e', padx=5, pady=5)

# Run the application
root.mainloop()