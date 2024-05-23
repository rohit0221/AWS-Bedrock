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
        
        # with st.sidebar:
        #     if suboption == "pdf document":
        #         st.subheader("Your pdfs")
        #         docs=st.file_uploader("Upload your PDF here and click on 'Process'",accept_multiple_files=True)
        #         if st.button("Process"):
        #             with st.spinner("Processing"):
        #                 knowledgebase='knowledge-base-quick-start-lt9bk'
        #                 delete_all_objects('knowledgebase-test-rohit')
        #                 update_knowledgebase(knowledgebase)
        #                 upload_new_documents(docs)
        #                 update_knowledgebase(knowledgebase)
    # Output the choice of the user
    st.write('You selected:', option, suboption)
    handle_message(option,suboption)


if __name__ == "__main__":
    main()