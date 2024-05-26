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
from youtube_handler import *
from knowledgebase_handling import *
from youtube_bot import *
import boto3


def handle_message(option,suboption,suboption2):
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
                answer=user_input_healthbot(user_question,suboption,suboption2)
            elif option == "Document Chatbot":
                answer=user_input_docubot(user_question,suboption)
            elif option == "Chat with YouTube Video":
                answer=user_input_youtubebot(user_question,suboption)                                                    
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
    st.header("Welcome to Rohit's Multibot powered by 🌩️AWS Knowledge Sources💁")
    option = st.radio(
        'Which chatbot would you like to interact with?',
        ('Finance Chatbot', 'Health Chatbot', 'Code Chatbot', 'Document Chatbot','Chat with YouTube Video')
    )
    if option == 'Code Chatbot':
        suboption = st.selectbox(
            "What would you like to do with your code?🧐",
            ("Create Code Documentation", "Add Comments to my Code", "Explain the Code", "Create Architecture Diagram")
        )
        st.write('You selected:', suboption)
        print(suboption)
        suboption2 ="Code Chatbot"

    if option == 'Finance Chatbot':
        suboption = st.selectbox(
            "What insights would you like to have about the Company?📈",
            ("Revenue Numbers", "Profit Numbers", "Debt Details")
        )
        st.write('You selected:', suboption)
        print(suboption)
        suboption2 ="Finance Chatbot"
        with st.sidebar:
            st.subheader("Your company's financial report")
            docs=st.file_uploader("Upload your company's financial report here and click on 'Process'",accept_multiple_files=True)
            if st.button("Process"):
                with st.spinner("Processing"):
                    knowledgebaseid=os.getenv("KNOWLEDGE_BASE_FINANCE")
                    datasourceid=os.getenv("DATASOURCE_FINANCE")
                    bucketname=os.getenv("BUCKET_FINANCE")
                    delete_all_objects(bucketname)
                    update_knowledgebase(knowledgebaseid,datasourceid)
                    upload_new_documents(docs,bucketname)
                    update_knowledgebase(knowledgebaseid,datasourceid)          
        
    if option == 'Health Chatbot':  
        suboption = st.selectbox(
            "What can I do for you to improve your fitness?🤸🏼‍♂️",
            ("General Health related query","Prepare a Diet Plan", "Create an fitness program", "Analyse my health report")
        )
        st.write('You selected:', suboption)
        print(suboption)
        if suboption == "General Health related query":
            suboption2 = st.radio(
                "Alright! How can I help you?",
                ("mental health", "physical health")
            )  
            st.write('Sure thing! Please go ahead and type in your question in the chat')
        elif suboption == "Prepare a Diet Plan": 
            suboption2 = st.radio(
                "Alright! What type of food plan do you wish to follow?🥗",
                ("vegetarian", "non vegetarian", "vegan", "ketogenic", "intermittent fasting","mediterranean", "calorie deficit", "detox","paleo diet")
            )  
        elif suboption == "Create an fitness program": 
            suboption2 = st.radio(
                "Okayyy...What type of workouts do you like?🏋️‍♂️",
                ("cardio", "strength training", "flexibility and balance workout", "high intensity interval training", "group fitness plan","circuit training", "body weight workouts")
            )
        elif suboption == "Analyse my health report": 
            suboption2 = st.radio(
                "Thats a good way to start being healthy! What insights do you want from your health report?🩺",
                ("Cholesterol Levels", "Kidney Health", "Liver Health", "Overall Summary", "Have a specific question?")
            )                       
               

        with st.sidebar:
            if suboption == "Analyse my health report":
                st.subheader("Your health report")
                docs=st.file_uploader("Upload your health report here and click on 'Process'",accept_multiple_files=True)
                if st.button("Process"):
                    with st.spinner("Processing"):
                        knowledgebaseid=os.getenv("KNOWLEDGE_BASE_HEALTH")
                        datasourceid=os.getenv("DATASOURCE_HEALTH")
                        bucketname=os.getenv("BUCKET_HEALTH")
                        delete_all_objects(bucketname)
                        update_knowledgebase(knowledgebaseid,datasourceid)
                        upload_new_documents(docs,bucketname)
                        update_knowledgebase(knowledgebaseid,datasourceid)
            elif suboption == "Prepare a Diet Plan":
                            st.subheader("Lets, prepare a diet plan for you!")
                            st.write('Perfect! 🌯🍱🍜🍲You selected:', suboption)
                            st.write('''\n
                                     🌮🍕🥪\n
                                     In order for me to fine-tune your diet plan,\n
                                     please provide your diet preferences \n
                                     in the following format \n
                                     and send it to me:\n
                                     👉 Calorie Limit:______________\n
                                     👉 Favourite Items to prepare the food:______________\n
                                     👉 Average Cooking time:______________''')
            elif suboption == "Create an fitness program":
                            st.subheader("Lets, prepare a fitness program for you!")
                            st.write('Great🧘‍♀️! You selected:', suboption)
                            st.write('''\n
                                     🏃🏋️🤾\n
                                     In order for me to create a plan that\n
                                     you are likely to love and follow,\n
                                     please provide your workout preferences\n
                                     in the following format\n
                                     and send it to me:\n
                                     👉 Time that you can spend on workouts each day:______________\n
                                     👉 Intensity level:______________\n
                                     👉 Indoor/Outdoor:______________''')
            elif suboption == "General Health related query":
                            st.subheader("Lets, help you!")
                            st.write('Great❤️! You selected:', suboption)
                            
                            st.write('''\n
                                     🙋‍♂️📜🙌💭\n
                                     In order for me to help you\n
                                     please provide your question in\n
                                     as detailed way as possible\n
                                     and send it to me:\n''')
    if option == 'Document Chatbot':  
        suboption = st.radio(
            "Choose your datasource type?📜",
            ("pdf document", "web page")
        )
        st.write('You selected:', suboption)
        print(suboption)
        suboption2 ="Document Chatbot"
        with st.sidebar:
            if suboption == "pdf document":
                st.subheader("Your pdfs")
                docs=st.file_uploader("Upload your PDF here and click on 'Process'",accept_multiple_files=True)
                if st.button("Process"):
                    with st.spinner("Processing"):
                        knowledgebaseid=os.getenv("KNOWLEDGE_BASE_DOCUBOT")
                        datasourceid=os.getenv("DATASOURCE_DOCUBOT")
                        bucketname=os.getenv("BUCKET_DOCUBOT")
                        #knowledgebase='knowledge-base-quick-start-lt9bk'
                        delete_all_objects(bucketname)
                        update_knowledgebase(knowledgebaseid,datasourceid)
                        upload_new_documents(docs,bucketname)
                        update_knowledgebase(knowledgebaseid,datasourceid)        
    if option == 'Chat with YouTube Video':  
        suboption = st.selectbox(
            "What insights do you want from the youtube video?🎬",
            ("Give me the video summary", "Chat with Youtube Video")
        )
        st.write('You selected:', suboption)
        print(suboption)
        suboption2 ="Chat with YouTube Video"
        with st.sidebar:
            if (suboption == "Give me the video summary") or (suboption == "Chat with Youtube Video"):
                st.subheader("Your YouTube Video")
                video_url = st.text_input("Enter the YouTube Video link here and press 'Enter'' 👇")
                if video_url:
                    if st.button("Consume my YouTube video!"):
                        create_transcript_file(video_url)
                        knowledgebaseid=os.getenv("KNOWLEDGE_BASE_YOUTUBE")
                        datasourceid=os.getenv("DATASOURCE_YOUTUBE")
                        bucketname=os.getenv("BUCKET_YOUTUBE")
                        #knowledgebase='knowledge-base-quick-start-lt9bk'
                        delete_all_objects(bucketname)
                        update_knowledgebase(knowledgebaseid,datasourceid)
                        upload_youtube_transcript(bucketname)
                        update_knowledgebase(knowledgebaseid,datasourceid)


    # Output the choice of the user
    st.write('You selected:', option, suboption,suboption2)
    handle_message(option,suboption,suboption2)


if __name__ == "__main__":
    main()