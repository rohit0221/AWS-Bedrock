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


def get_prompttemplate_financebot(suboption):
    if suboption =="Revenue Numbers":
        with open("../prompts/finance-bot/revenue-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption =="Profit Numbers":
        with open("../prompts/finance-bot/revenue-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption =="Debt Details":
        with open("../prompts/finance-bot/debt-prompt.txt", "r") as file:
            prompt_template = file.read() 
    return prompt_template            


def get_conversational_chain_financebot(suboption):
    prompt_template=get_prompttemplate_financebot(suboption)
    prompt = prepare_prompt_gen(prompt_template)
    model = get_model_gen()
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input_financebot(user_question,suboption):
    knowledge_base="OMNDAYJNHH"
    retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=knowledge_base,
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},)
    docs = retriever.invoke(user_question)   
    chain = get_conversational_chain_financebot(suboption)
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)
    return response