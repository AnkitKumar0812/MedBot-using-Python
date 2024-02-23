import nltk
import pickle
import random
import json
import numpy as np
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


from keras.models import load_model
model = load_model('Medbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result
      
        
def chatbot_response(msg):
    while True:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
        return res

#Creating GUI with tkinter
import tkinter
from tkinter import*
from tkinter import font as size
        

def temp():
    msg = "Hi!,I am MedBot (A Medical Assistant Chatbot)"
    
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "Bot: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
#        res = chatbot_response(msg)
#        ChatLog.insert(END, "Bot: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

def entrytext():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
 
def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
 

base = Tk()
base.title("MedBot")
base.geometry("460x550")
base.resizable(width=FALSE, height=FALSE)
base.wm_iconbitmap('2 (2).ico') 

#Create Chat window
ChatLog = Text(base, bd=0,font="Verdana", bg="#66E2FF", height="70", width="200")
ChatLog.config(state=DISABLED)


#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, bg="#A2BCD5", command=ChatLog.yview, cursor="arrow")
ChatLog['yscrollcommand'] = scrollbar.set

temp()

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="10",relief=GROOVE, height=2, bd=1, bg="#20B2AA", activebackground="#3c9d9b",fg='white',command=send)

'''send_button = Button(base, text="Send", width=5, relief=GROOVE, bg='white',bd=1, command=lambda: send(None), activebackground="#FFFFFF",activeforeground="#000000")
base.bind("<Return>",send)'''

#Create the box to enter message
EntryBox = Text(base, bd=1, bg="#e7f7fa",width="25", height="5", font="Verdana")


#Place all components on the screen
scrollbar.place(x=440,y=6, height=435)
ChatLog.place(x=6,y=6, height=435, width=430)
EntryBox.place(x=128, y=450, height=90, width=325)
SendButton.place(x=6, y=450, height=90)

base.mainloop()