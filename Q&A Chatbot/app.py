import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

#Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot"


#Promt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful massistant . Please  repsonse to the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,engine,temperature,max_tokens):
    os.environ["GROQ_API_KEY"] = api_key
    llm = ChatGroq(model_name=engine)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({'question':question})
    return answer
    
# Title of the app
st.title("Enhanced Q&A Chatbot")

# Siderbar for setting
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your API Key:",type = 'password')

engine = st.sidebar.selectbox("Select Model",["meta-llama/llama-4-maverick-17b-128e-instruct","meta-llama/llama-4-scout-17b-16e-instruct","llama-3.3-70b-versatile"])

# Adjust response parameter
temperature = st.sidebar.slider("Temperature",min_value=0.0,max_value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50,max_value=150)

# Main interface for user input
st.write("Goe ahead and ask any question")
user_input = st.text_input("You:")

if user_input and api_key:
    response = generate_response(user_input,api_key,engine,temperature,max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter the aPi Key in the sider bar")
else:
    st.write("Please provide the user input")
    