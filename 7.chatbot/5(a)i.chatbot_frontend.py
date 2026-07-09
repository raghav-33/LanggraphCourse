import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

# Like in Normally to maintain Converstaion history , we make empty list named 'history'(i.e: history=[]) then we append user message and assitant message in dict format{'role':user/ai,content:user_message) then load entire history by loop before starting new connversation
# But Problem in this in streamlit it got refreshed/vanish on pressing enter , But streamlit provide this type of dict known as session_state
# session_state is special type of dict in streamlit that not got refreshed / vanish on  pressing enter , only erase when manully refresh


CONFIG = {'configurable' : {'thread_id':'thread-1'}}

# Creating session_state dict in not exist already (message_history is name of dict)
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Loading Conversation History then start new conversation
for message in st.session_state['message_history']:
    # It make Chat Dialog box in chatbot with human avatar if role : user & robot avater if role : assitant
    with st.chat_message(message['role']):    ## This is PreBuilt Function in Streamlit help to make you Chatbot like interface 
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

