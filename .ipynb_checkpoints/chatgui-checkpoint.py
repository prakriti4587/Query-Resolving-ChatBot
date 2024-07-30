{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "93963852-6715-44ac-b79b-fc90501f4810",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING:absl:Compiled the loaded model, but the compiled metrics have yet to be built. `model.compile_metrics` will be empty until you train or evaluate the model.\n"
     ]
    }
   ],
   "source": [
    "import nltk, json, random, pickle\n",
    "from nltk.stem import WordNetLemmatizer\n",
    "lemmatizer = WordNetLemmatizer()\n",
    "import pickle\n",
    "import numpy as np\n",
    "from tensorflow.keras.models import load_model\n",
    "model = load_model('chatbot_model.h5')\n",
    "intents = json.loads(open('intents.json').read())\n",
    "words = pickle.load(open('words.pkl','rb'))\n",
    "classes = pickle.load(open('classes.pkl','rb'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "d2b362f6-fb57-4e25-baee-c33db02963f0",
   "metadata": {},
   "outputs": [],
   "source": [
    "import nltk\n",
    "from nltk.stem import WordNetLemmatizer\n",
    "import numpy as np\n",
    "\n",
    "lemmatizer = WordNetLemmatizer()\n",
    "\n",
    "def clean_up_sentence(sentence):\n",
    "    # tokenize the pattern - split words into array\n",
    "    sentence_words = nltk.word_tokenize(sentence)\n",
    "    # stem each word - create short form for word\n",
    "    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]\n",
    "    return sentence_words\n",
    "\n",
    "# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence\n",
    "def bow(sentence, words, show_details=True):\n",
    "    # tokenize the pattern\n",
    "    sentence_words = clean_up_sentence(sentence)\n",
    "    # bag of words - matrix of N words, vocabulary matrix\n",
    "    bag = [0]*len(words)  \n",
    "    for s in sentence_words:\n",
    "        for i, w in enumerate(words):\n",
    "            if w == s: \n",
    "                # assign 1 if current word is in the vocabulary position\n",
    "                bag[i] = 1\n",
    "                if show_details:\n",
    "                    print(\"found in bag: %s\" % w)\n",
    "    return np.array(bag)\n",
    "\n",
    "def predict_class(sentence, model, words, classes):\n",
    "    # filter out predictions below a threshold\n",
    "    p = bow(sentence, words, show_details=False)\n",
    "    res = model.predict(np.array([p]))[0]\n",
    "    ERROR_THRESHOLD = 0.25\n",
    "    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]\n",
    "    # sort by strength of probability\n",
    "    results.sort(key=lambda x: x[1], reverse=True)\n",
    "    return_list = []\n",
    "    for r in results:\n",
    "        return_list.append({\"intent\": classes[r[0]], \"probability\": str(r[1])})\n",
    "    return return_list\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "73bb784d-a645-4f98-a8f0-15b3b2e2e69d",
   "metadata": {},
   "outputs": [],
   "source": [
    "def getResponse(ints, intents_json):\n",
    "    tag = ints[0]['intent']\n",
    "    list_of_intents = intents_json['intents']\n",
    "    for i in list_of_intents:\n",
    "        if(i['tag']== tag):\n",
    "            result = random.choice(i['responses'])\n",
    "            break\n",
    "    return result\n",
    "def chatbot_response(text):\n",
    "    ints = predict_class(text, model)\n",
    "    res = getResponse(ints, intents)\n",
    "    return res"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "c22c3506-894f-486a-9058-750ecfded654",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Creating GUI with tkinter\n",
    "import tkinter\n",
    "from tkinter import *\n",
    "def send():\n",
    "    msg = EntryBox.get(\"1.0\",'end-1c').strip()\n",
    "    EntryBox.delete(\"0.0\",END)\n",
    "    if msg != '':\n",
    "        ChatLog.config(state=NORMAL)\n",
    "        ChatLog.insert(END, \"You: \" + msg + '\\n\\n')\n",
    "        ChatLog.config(foreground=\"#442265\", font=(\"Verdana\", 12 ))\n",
    "        res = chatbot_response(msg)\n",
    "        ChatLog.insert(END, \"Bot: \" + res + '\\n\\n')\n",
    "        ChatLog.config(state=DISABLED)\n",
    "        ChatLog.yview(END)\n",
    "base = Tk()\n",
    "base.title(\"Hello\")\n",
    "base.geometry(\"400x500\")\n",
    "base.resizable(width=FALSE, height=FALSE)\n",
    "#Create Chat window\n",
    "ChatLog = Text(base, bd=0, bg=\"white\", height=\"8\", width=\"50\", font=\"Arial\",)\n",
    "ChatLog.config(state=DISABLED)\n",
    "#Bind scrollbar to Chat window\n",
    "scrollbar = Scrollbar(base, command=ChatLog.yview, cursor=\"heart\")\n",
    "ChatLog['yscrollcommand'] = scrollbar.set\n",
    "#Create Button to send message\n",
    "SendButton = Button(base, font=(\"Verdana\",12,'bold'), text=\"Send\", width=\"12\", height=5, bd=0, bg=\"#32de97\", activebackground=\"#3c9d9b\",fg='#ffffff', command= send )\n",
    "#Create the box to enter message\n",
    "EntryBox = Text(base, bd=0, bg=\"white\",width=\"29\", height=\"5\", font=\"Arial\")\n",
    "#EntryBox.bind(\"<Return>\", send)\n",
    "#Place all components on the screen\n",
    "scrollbar.place(x=376,y=6, height=386)\n",
    "ChatLog.place(x=6,y=6, height=386, width=370)\n",
    "EntryBox.place(x=128, y=401, height=90, width=265)\n",
    "SendButton.place(x=6, y=401, height=90)\n",
    "base.mainloop()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3b768d8e-e0eb-4f41-9ed5-4977d10d0487",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
