# ********************************** Imports ************************************* 
import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid  # To Generate a Dynamic Thread id


# ******************************* Utility Function *********************************

def generate_thread_id():
    thread_id = uuid.uuid4() # Generate a Random Thread id (UUID4)
    return thread_id

def reset_chat():
    thread_id = generate_thread_id() # Generate a new thread id
    st.session_state['thread_id']=thread_id # Store in session state
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = [] # reset(empty) message history

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id):
    return chatbot.get_state(config = {'configurable':{'thread_id': thread_id}}).values['messages']

# ***************************************** Session Setup ************************************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:                  # if thread_id is not in session state
    st.session_state['thread_id'] = generate_thread_id() # generating thread_id and adding in session state

if 'chat_threads' not in st.session_state:
    st.session_state['chatchat_threads'] = []
add_thread(st.session_state['thread_id'])



# ****************************************** Sidebar UI ****************************************************

st.sidebar.title('Langraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)): # display thread_id in sidebar which is stored in session state
           st.session_state['thread_id'] = thread_id
           messages= load_conversation(thread_id)

           temp_messages = []
           for msg in messages:
               if isinstance(msg,HumanMessage):
                   role = 'user'
                else:
                   role = 'assitant'
                temp_messages.append({'role':role,'content':msg.content})
            st.session_state['message_history']=temp_messages

 
# *************************************** Main UI *******************************************************   

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


    CONFIG = {'configurable' : {'thread_id': st.session_state['thread_id']}}

    # First add the Message to message_history
    with st.chat_message('assitant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content='what is recipie to make pasta')]},
                config = CONFIG,
                stream_mode= 'messages'
            )
        )
    st.session_state['message_history'].append({'role':'assitant','content':ai_message})


# Now Chatbot is ready , Remove streaming code from backend as manage at frontend