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


def get_prompttemplate_healthbot(suboption2):

    # health report
    if suboption2 =="Cholesterol Levels":
        with open("../prompts/health-bot/health-report/cholesterol-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="Kidney Health":
        with open("../prompts/health-bot/health-report/kidney-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="Liver Health":
        with open("../prompts/health-bot/health-report/liver-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="Overall Summary":
        with open("../prompts/health-bot/health-report/overall-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="Have a specific question?":
        with open("../prompts/health-bot/health-report/specific-prompt.txt", "r") as file:
            prompt_template = file.read()
    # Fitness program

    elif suboption2 =="cardio":
        with open("../prompts/health-bot/fitness-program/cardio-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="strength training":
        with open("../prompts/health-bot/fitness-program/strength-training-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="flexibility and balance workout":
        with open("../prompts/health-bot/fitness-program/flexibility-and-balance-workout-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="high intensity interval training":
        with open("../prompts/health-bot/fitness-program/high-intensity-interval-training-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="group fitness plan":
        with open("../prompts/health-bot/fitness-program/group-fitness-plan-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="circuit training":
        with open("../prompts/health-bot/fitness-program/circuit-training-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="body weight workouts":
        with open("../prompts/health-bot/fitness-program/bodyweight-workouts-prompt.txt", "r") as file:
            prompt_template = file.read()
    #specific question
    elif suboption2 =="mental health":
        with open("../prompts/health-bot/general-query/mental-health-prompt.txt", "r") as file:
            prompt_template = file.read()
    elif suboption2 =="physical health":
        with open("../prompts/health-bot/general-query/physical-health-prompt.txt", "r") as file:
            prompt_template = file.read()            




    return prompt_template          


def get_conversational_chain_healthbot(suboption2):
    prompt_template=get_prompttemplate_healthbot(suboption2)
    prompt = prepare_prompt_gen(prompt_template)
    model = get_model_gen()
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input_healthbot(user_question,suboption,suboption2):
    #knowledge_base="5QCOID5GYC"# correct
    knowledge_base = os.getenv("KNOWLEDGE_BASE_HEALTH")
    retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=knowledge_base,
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},)
    docs = retriever.invoke(user_question)   
    chain = get_conversational_chain_healthbot(suboption2)
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)
    return response