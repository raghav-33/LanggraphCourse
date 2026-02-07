import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage


CONFIG = {'configurable' : {'thread_id':'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Loading Conversation History
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type Here')

if user_input:

    # First add the Message to message_history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    
    response=chatbot.invoke({'message':[HumanMessage(content=user_input)]}, config=CONFIG)
    ai_message=response['messages'][-1].content

    # First add the message to message_history
    st.session_state['message_history'].append({'role':'assitant','content':ai_message})
    with st.chat_message('assitant'):
        st.text(ai_message )

