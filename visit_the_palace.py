
from openai import OpenAI
import os
import logging
import time

#########OPENAI API#########
openai = OpenAI()

def generate_response(messages, model):
    for _ in range(5):
        try:
            response = openai.chat.completions.create(model=model, messages=messages, max_tokens=200, temperature=0)
            return response
        except Exception as e:
            logging.exception(f"Exception occurred: {e}")
    else:
        return False


#########LANGCHAIN EXAMPLES PULLER #########

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def initialize_vdb():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the .txt file, in this case, the book Meditations by Marcus Aurelius
    txt_file_path = os.path.join(dir_path, 'meditations.txt')

    loader = TextLoader(txt_file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50, length_function = len, is_separator_regex = False)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    db = FAISS.from_documents(docs, embeddings)
    print('db initialized')
    return db


def find_examples(db, query, k=5):
    docs = db.similarity_search(query, k=k)

    examples = ""
    i = 1
    for doc in docs:
       examples += f'\n\nEXAMPLE {i}:\n' + doc.page_content
       i+=1
    return examples


#########SIMPLE IMPLEMENTATION#########
db = initialize_vdb()


prompt = "You are Marcu Aurelius, Emperor of Rome. You are speaking to a common boy who is curious about Mediations. Below are excerpts from Meditations for you to respond from. If the answer is not in the following text, respond with I do not know (but as Marcus would say it):\n\n"
outbound = "Good day young one. How may I be of aid?"
inbound = ""
messages = []

while input != "Exit":
    print("###################################################")
    inbound = input("Marcus: " + outbound + "\n###################################################"+'\nYou: ')
    
    if input == "Exit":
        break
    
    #append user input to messages
    messages.append({"role": "user", "content": inbound})

    #do similarity search and get examples
    examples = find_examples(db, inbound)

    #format custom system prompt
    custom_prompt = prompt + examples
    custom_prompt = {"role": "system", "content": custom_prompt}

    #format messages for response generation
    llm_messages = [custom_prompt] + messages

    #generate response
    response = generate_response(llm_messages, "gpt-4-1106-preview")
    outbound = response.choices[0].message.content

    if outbound:
        messages.append({"role": "assistant", "content": outbound})

    else:
        print("Sorry, something went wrong. Please try again.")
        break

