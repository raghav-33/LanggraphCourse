############################ Extra Feature Added : Streaming (TypeWriter Effect) ########################################### 

from langgraph.graph import StateGraph,START,END
from typing import TypedDict , Annotated
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import BaseMessage ,SystemMessage,HumanMessage,AIMessage

# Persistance Import
from langgraph.checkpoint.memory import MemorySaver  #kind of memory in langraph which store things in RAM
from dotenv import load_dotenv

load_dotenv()

# State Define
from langgraph.graph.message import add_messages
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages ]  # Base Messages : all types of messages is derived from it , it indicate here any type of message can be present either human , AI or system message

# add_messages: is a reducer function like operator.add in previous code.
# Why ?
# Because nature of state is when it get new value its old value (message) is deleted .
# therefore add_messages (reducer function) is  used to maintain conversational history, not forget previous messages or states.

# LLM define
llm = ChatOpenAI()


def chat_node(state: ChatState):
    # Take User Query From state
    messages = state['messages']

    # Send to llm
    response = llm.invoke(messages)

    # Response store state
    return {'messages' : [response]}


# Graph Define

checkpointer = MemorySaver()  # Persistance : memory

graph = StateGraph(ChatState)

# nodes add
graph.add_node('chat_node', chat_node)

# Edge add
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

# Compile
chatbot = graph.compile(checkpointer=checkpointer)

###################### Streaming Output ##############################
stream =chatbot.stream(
    {'messages': [HumanMessage(content='what is recipie to make pasta')]},
    config = {'configurable' : {'thread_id':'thread-1'}},
    stream_mode = 'messages'
)

print(type(stream))

# NOTE: (i) Here Stream Object return message_chunk and metadta
#       (ii) Above mention syntax code of Stream not mostly used , Given below Syntax is Used.


for message_chunk, metadata in chatbot.stream(
    {'messages': [HumanMessage(content='what is recipie to make pasta')]},
    config = {'configurable' : {'thread_id':'thread-1'}},
    stream_mode= 'messages'
):
  
  if message_chunk.content:
    print(message_chunk.content , end=" ", flush=True)  
      # flush=True forces Python to immediately write the output to the terminal instead of waiting. Normally, Python buffers output and prints it in chunks.
      # Why buffering is a problem in streaming ❌ ? 
    '''  In streaming LLM output:
          (i) Tokens arrive one by one
         (ii) You want to display them immediately
         (iii) Buffered output causes delay
         
         Without flush=True, Python may wait until:
          (i) Buffer is full
         (ii) Newline (\n) appears
         (iii) Program finishes.
      '''
      # With flush=True: Each token is printed as soon as it arrives . User sees real-time typing effect


# Chatbot Logic
thread_id= '1' # Basically at same time chatbot is used by many peoples . so thread id is chatbot kis people sai kya baat kr rha hai.
while True:
    user_message = input('Type Here')

    print("User:" , user_message)

    if user_message.strip().lower() in ['exit', 'quit' , 'bye']:
        break

    config = {'configurable': {'thread_id':thread_id}}
    response= chatbot.invoke({'messages': [HumanMessage(content=user_message)]},config=config)
    
    print('AI:', response['messages'[-1].content])