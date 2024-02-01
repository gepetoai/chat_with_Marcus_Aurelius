from openai import OpenAI
from icecream import ic
import os

#########OPENAI API#########
openai = OpenAI(max_retries = 5)

def generate_response(messages, model):
    '''just getting a response from openai. try 5x'''
    
    try:
        response = openai.chat.completions.create(model=model, messages=messages, max_tokens=200, temperature=0)
        ic("......OpenAI Response Generated")
        return response
    
    except Exception as e:
        ic(f"Exception occurred: {e}")
        return False



#########LANGCHAIN EXAMPLES PULLER #########
from langchain_community.document_loaders import TextLoader #TexLoader loads a text file
from langchain.text_splitter import RecursiveCharacterTextSplitter #RecursiveCharacterSplitter chunks it up
from langchain_openai import OpenAIEmbeddings #OpenAIEmbeddings generates the embeddings
from langchain_community.vectorstores import FAISS #FAISS stores them for similarity search

def initialize_vdb():
    '''initialize an FAISS in-RAM vector database'''
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the .txt file, in this case, the book Meditations by Marcus Aurelius
    txt_file_path = os.path.join(dir_path, 'meditations.txt')

    loader = TextLoader(txt_file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function = len, is_separator_regex = False)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    db = FAISS.from_documents(docs, embeddings)
    ic("......Vector Database Initialized")
    return db


def find_examples(db, query, k=5):
    '''perform similarity search and return the k nearest stringified examples that match the query '''
    docs = db.similarity_search(query, k=k)

    examples = ""
    i = 1
    for doc in docs:
       examples += f'\n\nEXAMPLE {i}:\n' + doc.page_content
       i+=1
    ic("......Similarity Search Results Retreived")
    return examples





