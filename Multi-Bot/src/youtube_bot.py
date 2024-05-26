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


def get_prompttemplate_youtubebot(suboption):
    if suboption =="Give me the video summary":
        with open("../prompts/youtube-bot/youtube-video-summary-prompt.txt", "r") as file:
            prompt_template = file.read()
            print(prompt_template)
    elif suboption =="Chat with Youtube Video":
        with open("../prompts/youtube-bot/chat-with-video-prompt.txt", "r") as file:
            prompt_template = file.read()
    return prompt_template            


def get_conversational_chain_youtubebot(suboption):
    prompt_template=get_prompttemplate_youtubebot(suboption)
    prompt = prepare_prompt_gen(prompt_template)
    model = get_model_gen()
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input_youtubebot(user_question,suboption):
    knowledge_base = os.getenv("KNOWLEDGE_BASE_YOUTUBE")
    #knowledge_base="ROEZ7VMG8N"
    retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=knowledge_base,
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},)
    docs = retriever.invoke(user_question)
    print("here are the docs from transcript")
    print(docs)
    chain = get_conversational_chain_youtubebot(suboption)
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)
    return response