import streamlit as st
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.llms import Bedrock
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever

def get_conversational_chain_finance(option):
    if option == "Finance Chatbot":
        with open("finance_prompt.txt", "r") as file:
            prompt_template = file.read()
    elif option == "Health Chatbot":
        with open("health_prompt.txt", "r") as file:
            prompt_template = file.read()

    model = Bedrock(model_id="meta.llama3-70b-instruct-v1:0")

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question,option):
    if option == "Finance Chatbot":
        knowledge_base="OMNDAYJNHH"
    elif option == "Health Chatbot":
        knowledge_base="5QCOID5GYC"
    retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=knowledge_base,
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},)
    docs = retriever.invoke(user_question)
    chain = get_conversational_chain_finance(option)
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    return response

def handle_message(option):
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

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
            answer=user_input(user_question,option)
            st.session_state.messages.append({"role": "user", "content": user_question})
            print(answer)
            print(type(answer))


            msg = answer['output_text']
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg) 

    
def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF using 🌩️AWS Knowledge Sources💁")
    option = st.selectbox(
        'Which chatbot would you like to interact with?',
        ('Finance Chatbot', 'Health Chatbot')
    )

    # Output the choice of the user
    st.write('You selected:', option)    
    handle_message(option)


if __name__ == "__main__":
    main()