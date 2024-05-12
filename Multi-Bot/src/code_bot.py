import streamlit as st
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()
from langchain_community.llms import Bedrock
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
from utils import *
def get_prompttemplate_codebot(code_suboption):
    if code_suboption =="Create Code Documentation":
        with open("../prompts/code-docu-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif code_suboption =="Add Comments to my Code":
        with open("../prompts/code-comment-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif code_suboption =="Explain the Architecture of my Code":
        with open("../prompts/code-architecture-prompt.txt", "r") as file:
            prompt_template = file.read() 
    return prompt_template            

def get_conversational_chain_codebot(code_suboption):
    prompt_template=get_prompttemplate_codebot(code_suboption)
    prompt = prepare_prompt_gen(prompt_template)
    model = get_model_gen()
    chain = LLMChain(llm=model, prompt=prompt)
    return chain

def user_input_codebot(user_question,code_suboption):
    chain = get_conversational_chain_codebot(code_suboption)
    response = chain(
        {"question": user_question}
        , return_only_outputs=True)
    return response