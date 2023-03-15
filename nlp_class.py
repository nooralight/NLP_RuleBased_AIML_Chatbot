import nltk
import random
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')


# read in and preprocess data
with open('dataset.txt', 'r', encoding='utf8', errors='ignore') as f:
    raw_data = f.read().lower()

sent_tokens = nltk.sent_tokenize(raw_data)
word_tokens = nltk.word_tokenize(raw_data)

lemmatizer = nltk.stem.WordNetLemmatizer()

def lem_tokens(tokens):
    return [lemmatizer.lemmatize(token) for token in tokens]

remove_punc_dict = dict((ord(punct), None) for punct in string.punctuation)

def lem_normalize(text):
    return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punc_dict)))

# define greeting and goodbye messages
GREETING_INPUTS = ['hi', 'hello', 'hey', 'greetings', 'sup', 'what\'s up', 'yo']
GREETING_RESPONSES = ['hello', 'hi', 'hey', 'hi there', 'hello!', 'I am glad! You are talking to me']

GOODBYE_INPUTS = ['bye', 'goodbye', 'see you', 'cya']
GOODBYE_RESPONSES = ['Goodbye, take care!', 'Bye! Have a great day.', 'See you later.', 'Nice talking to you. Bye!']

# define function to generate response
def get_response(user_input):
    chatbot_response = ''
    
    # add user input to sentence tokens
    sent_tokens.append(user_input)
    
    #stop_words = set(nltk.corpus.stopwords.words('english'))

    # create TfidfVectorizer object
    TfidfVec = TfidfVectorizer(tokenizer=lem_normalize, stop_words=None)
    
    # create tfidf matrix
    tfidf = TfidfVec.fit_transform(sent_tokens)
    
    # get cosine similarity of user input and all sentence tokens
    vals = cosine_similarity(tfidf[-1], tfidf)
    
    # get index of most similar sentence
    idx = vals.argsort()[0][-2]
    
    # sort the cosine similarities
    flat = vals.flatten()
    flat.sort()
    
    # get the most similar sentence to the user input
    req_tfidf = flat[-2]
    if(req_tfidf == 0):
        chatbot_response = chatbot_response + "I am sorry! I don't understand you"
        return chatbot_response
    else:
        # concatenate sentences until punctuation mark is encountered
        while idx < len(sent_tokens) - 1 and sent_tokens[idx+1][-1] not in string.punctuation:
            chatbot_response += sent_tokens[idx+1] + ' '
            idx += 1
        chatbot_response += sent_tokens[idx+1]
        return chatbot_response



# define function to handle chatbot
def chatbot(msg):
    #print('Hello! My name is Chatbot. Ask me anything or say goodbye to exit.')
    response=""
    user_input = msg
    if user_input.lower() in GOODBYE_INPUTS:
        response = random.choice(GOODBYE_RESPONSES)
    else:
        if user_input.lower() in GREETING_INPUTS:
            response = random.choice(GREETING_RESPONSES)
        else:
            response = get_response(user_input)
    return response
                
# start chatbot
###chatbot()
