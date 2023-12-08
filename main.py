from google.cloud import dialogflow
import os
import tkinter as Tk

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'

DIALOGFLOW_PROJECT_ID = 'python-chat-bot-399907'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'


def getBotResponse(text):
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.TextInput({'text': text, 'language_code': DIALOGFLOW_LANGUAGE_CODE})
        query_input = dialogflow.QueryInput({'text': text_input})
        response = session_client.detect_intent(session=session, query_input=query_input)

        return response.query_result.fulfillment_text.replace('\\n', '\n')
    except Exception as err:
        print(err.args)
        return "ERROR\nSomething Went Wrong!!!"


def sendMsg(_):
    msg = userInput.get()

    chatBox.config(state=Tk.NORMAL)
    chatBox.insert(Tk.END, f'You: {msg}\n')
    chatBox.config(state=Tk.DISABLED)

    userInput.delete(0, Tk.END)
    userInput.config(state=Tk.DISABLED)
    win.update()

    reply = getBotResponse(msg)
    chatBox.config(state=Tk.NORMAL)
    chatBox.insert(Tk.END, f'Bot: {reply}\n')
    chatBox.config(state=Tk.DISABLED)
    userInput.config(state=Tk.NORMAL)


WIN_WIDTH, WIN_HEIGHT = 800, 600

win = Tk.Tk()
win.title('Chat Bot')
win.resizable(False, False)

screenWidth, screenHeight = win.winfo_screenwidth(), win.winfo_screenheight()
win.geometry(
    f'{WIN_WIDTH}x{WIN_HEIGHT}+{int(screenWidth / 2 - WIN_WIDTH / 2)}+{int(screenHeight / 2 - WIN_HEIGHT / 2)}'
)

botImg = Tk.PhotoImage(file='chatbot.png')
win.iconphoto(True, botImg)

botFrame = Tk.Frame(win)
Tk.Label(botFrame, image=botImg).pack(side=Tk.LEFT)
Tk.Label(botFrame, width=2).pack(side=Tk.LEFT)
Tk.Label(botFrame, text='Bot', font=('', 16)).pack(side=Tk.LEFT)
botFrame.pack(side=Tk.TOP, anchor=Tk.NW, padx=10, pady=2)

chatBox = Tk.Text(win, font=('', 12))
chatBox.pack(fill=Tk.BOTH, expand=True, padx=5, pady=2)
chatBox.insert(Tk.END, 'Bot: I am Python Chat Bot, I can answer any of your theory Python Questions (hopefully)\n')
chatBox.config(state=Tk.DISABLED)

userInput = Tk.Entry(win, font=('', 10))
userInput.bind(sequence='<Return>', func=sendMsg)
userInput.pack(padx=5, pady=2, fill=Tk.X)
userInput.focus()

win.mainloop()
