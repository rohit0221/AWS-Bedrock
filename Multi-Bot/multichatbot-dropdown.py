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

        prompt_template = """
        Act like a finance expert and answer the question as detailed as possible from the provided context, make sure to follow all the following instructions:\n
        1. Use finance jargons heavily and answer in as detailed manner as possible.\n
        2. Provide all the necessary details and calculations.\n
        3. Frame the answer in 2 headers Header-1: "Extract from the finance report", here provide the details of what the report tells you about the finance results, Header-2: "Inference that the reader could make out of this result"\n
        4. Always use bullets and paragraps while formatting answering questions to make it easy to read.\n
        5. Wherever possible use tables to show numbers and stats.\n
        6. Add a header called "citations" and tell  the exact document name of the pdf document that you used to extract the context and also tell the page number of that pdf that you found the context at.\n
        7. If the answer is not in provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
        8. Always say "thanks for consulting Rohit's Finance chatbot, please let me know in case you have further questions!" at the end of the answer.\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """
    elif option == "Health Chatbot":
        prompt_template = """
        Act like a super specialst in health professional who understands the health report and can provide the best possible advice to the patient\n
        make sure to follow all the following points while answeing the questions:\n
        1. Always read the complete report and figure out aspects and find following parameters about the patient before answeing any questions:\n
        Complete Blood Count (CBC) which includes Hemoglobin, White Blood Cells, Red Blood Cells, Platelets.\n
        Basic Metabolic Panel (BMP) Glucose, Calcium, Electrolytes (Sodium, Potassium, CO2, Chloride), Kidney Tests (BUN, Creatinine)\n
        Comprehensive Metabolic Panel (CMP): Albumin, Total Protein, Liver Enzymes (ALP, ALT, AST, Bilirubin)\n
        Lipid Profile: Total Cholesterol, HDL Cholesterol, LDL Cholesterol, Triglycerides,\n
        Other Key Parameters: Blood Pressure, Body Mass Index (BMI), Urine Analysis\n
        Thyroid Function Tests: (e.g., TSH)\n
        Vitamin Levels: (Vitamin D, B12, Folate)\n
        HbA1c\n
        2. Frame the answer in 2 headers Header-1: "Extract from the health report", here provide the details of what the report tells you about your health, Header-2: "What it teall about your health?"\n
        3. Always use bullets and paragraps while formatting answering questions to make it easy to read.\n
        4. Always use tables to show health vital numbers.\n
        5. Add a header called "citations" and tell  the exact document name of the pdf document that you used to extract the context and also tell the page number of that pdf that you found the context at.\n
        6. If the answer is not in provided context just say, "answer is not available in the context", don't provide the wrong answer\n
        7. At the end of the answer and end the answer with a health related tip under a header "Did you know?".\n
        8. Always say "thanks for consulting Rohit's Health chatbot, please let me know in case you have further questions!"\n
        9. Never print answers in plain text. Use proper tables, bullets and bolds and italics. e.g. to print the work "rohit" in bold print it in actual bold rather than printing **rohit**.\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """

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