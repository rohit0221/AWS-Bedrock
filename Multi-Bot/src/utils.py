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

def prepare_prompt_gen(prompt_template):
    prompt = PromptTemplate(template = prompt_template,input_variables = ["question"])    
    return prompt

def get_model_gen():
    model = Bedrock(model_id="meta.llama3-70b-instruct-v1:0",
                    model_kwargs={"max_gen_len":2048, "temperature":0.5},
                    streaming=True)
    return model