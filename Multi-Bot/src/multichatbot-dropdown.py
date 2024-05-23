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
from code_bot import *
from finance_bot import *
from health_bot import *
from docu_bot import *
from utils import *
from s3_handling import *
from knowledgebase_handling import *
import boto3


def get_conversational_chain(option,suboption):
    if option == "Finance Chatbot":
        with open("finance_prompt.txt", "r") as file:
            prompt_template = file.read()
    elif option == "Health Chatbot":
        with open("health_prompt.txt", "r") as file:
            prompt_template = file.read()
    elif option == "Code Documentation Chatbot":
        if suboption =="Create Code Documentation":
            with open("code-docu-prompt.txt", "r") as file:
                prompt_template = file.read()
        elif suboption =="Add Comments to my Code":
            with open("code-comment-prompt.txt", "r") as file:
                prompt_template = file.read()
        elif suboption =="Explain the Architecture of my Code":
            with open("code-architecture-prompt.txt", "r") as file:
                prompt_template = file.read()                             

    model = Bedrock(model_id="meta.llama3-70b-instruct-v1:0",
                    model_kwargs={"max_gen_len":2048, "temperature":0.5},
                    streaming=True)
    
    if option == "Code Documentation Chatbot":
        prompt = PromptTemplate(template = prompt_template,input_variables = ["question"])
        chain = LLMChain(llm=model, prompt=prompt)
    else:
        prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question,option,suboption):

    if option == "Code Documentation Chatbot":
        chain = get_conversational_chain(suboption)
        response = chain(
            {"question": user_question}
            , return_only_outputs=True)
    else:
        if option == "Finance Chatbot":
            knowledge_base="OMNDAYJNHH"
        elif option == "Health Chatbot":
            knowledge_base="5QCOID5GYC"
        retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id=knowledge_base,
        retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},)
        docs = retriever.invoke(user_question)
        chain = get_conversational_chain(option)
        response = chain(
            {"input_documents":docs, "question": user_question}
            , return_only_outputs=True)

    return response

def handle_message(option,suboption):
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Bring it on!"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        print(prompt)
        print(type(prompt))

        message=st.session_state.messages
        print(message)
        print(type(message))
        user_question = next((item['content'] for item in reversed(message) if item['role'] == 'user'), None)

        if user_question:
            if option == "Code Chatbot":
                answer=user_input_codebot(user_question,suboption)
            elif option == "Finance Chatbot":
                answer=user_input_financebot(user_question,suboption)
            elif option == "Health Chatbot":
                answer=user_input_healthbot(user_question,suboption)
            elif option == "DocuBot":
                answer=user_input_docubot(user_question,suboption)                         
            st.session_state.messages.append({"role": "user", "content": user_question})
            print(answer)
            print(type(answer))
            if option == "Code Chatbot":
                msg = answer['text']
            else:
                msg = answer['output_text']
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)
    
def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF using 🌩️AWS Knowledge Sources💁")
    option = st.selectbox(
        'Which chatbot would you like to interact with?',
        ('Finance Chatbot', 'Health Chatbot', 'Code Chatbot', 'Docubot')
    )
    if option == 'Code Chatbot':
        suboption = st.radio(
            "What would you like to do with your code?🧐",
            ("Create Code Documentation", "Add Comments to my Code", "Explain the Architecture of my Code")
        )
        st.write('You selected:', suboption)
        print(suboption)

    if option == 'Finance Chatbot':
        suboption = st.radio(
            "What insights would you like to have about the Company?📈",
            ("Revenue Numbers", "Profit Numbers", "Debt Details")
        )
        st.write('You selected:', suboption)
        print(suboption)
    if option == 'Health Chatbot':
        suboption = st.radio(
            "Choose your datasource type?📜",
            ("pdf document", "web page")
        )    
        suboption = st.radio(
            "What insights would you like to have about your health Company?🩺",
            ("Cholesterol Levels", "Kidney Health", "Liver Health")
        )
        st.write('You selected:', suboption)
        print(suboption)
    if option == 'Docubot':
        suboption = st.radio(
            "Choose your datasource type?📜",
            ("pdf document", "web page")
        )
        st.write('You selected:', suboption)
        print(suboption)
        with st.sidebar:
            if suboption == "pdf document":
                st.subheader("Your pdfs")
                docs=st.file_uploader("Upload your PDF here and click on 'Process'",accept_multiple_files=True)
                if st.button("Process"):
                    with st.spinner("Processing"):
                        knowledgebase='knowledge-base-quick-start-lt9bk'
                        # Clean the bucket
                        delete_all_objects('knowledgebase-test-rohit')
                        update_knowledgebase(knowledgebase)
                        # Upload new documents
                        upload_new_documents(docs)
                        # refresh knowledge base
                        update_knowledgebase(knowledgebase)

            
                   


    # Output the choice of the user
    #st.write('You selected:', option, suboption)
    ##############handle_message(option,suboption)


if __name__ == "__main__":
    main()