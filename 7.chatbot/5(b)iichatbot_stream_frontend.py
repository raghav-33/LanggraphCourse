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

    
    ############################# WITHOUT STREAMING CODE #########################
    #response=chatbot.invoke({'message':[HumanMessage(content=user_input)]}, config=CONFIG)
    # ai_message=response['messages'][-1].content

    # First add the message to message_history
    # st.session_state['message_history'].append({'role':'assitant','content':ai_message})
    
    ############## STREAMING CODE ##############################
    with st.chat_message('assitant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content='what is recipie to make pasta')]},
                config = {'configurable' : {'thread_id':'thread-1'}},
                stream_mode= 'messages'
            )
        )
    st.session_state['message_history'].append({'role':'assitant','content':ai_message})


# Now Chatbot is ready , Remove streaming code from backend as manage at frontend