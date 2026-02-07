# MCP Code File 
''' 
(i)Here We Will Replace the Code of Custom Tool Write in tools file
With MCP Client and write code of that tools in Mcp servers.

(ii) Convert Normal toolcode file code to async Code:{parrallel execution}

(iii) Why Using Async code : because library we are going to use for MCPs (i.e : Fastmcp) is Work with Async code only.

'''
################################## Import ######################################################################
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

# Tools node and Tool conditions
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool  # for Custom tool
import asyncio # Async code
from langchain_mcp_adapters.client import MultiServerMCPClient # For Making MCP client

llm = ChatOpenAI()


#################################### MCP Client  #######################################################################

# MCP Client for local FastMCP Server
clinet = MultiServerMCPClient(
    {
        'airth':{                # airth: name of Mcp server
            'transport' : "stdio", # 2 type Of MCP server (i)local : stdio used (ii) Remote: streamable_http
            'command' :'python3',  # Command to run MCP server file from this file
            'args': '[E:\Generative Ai\LangGraph\9.mcp\mcp_server.py]'  # MCP server file path
        }
    }
)

########################################### Graph State ###################################################################

# state
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]



async def build_graph():
      
    # NOTE : write below 2 lines of code after creating MCP client here
    tools = await client.get_tools() # Fetch all tools from mcp server
    llm_with_tools = llm.bind_tools(tools) # Binding tool with llm
    
    # Nodes
    async def chat_node(state: ChatState):
        messages = state['messages']
        response = llm_with_tools.ainvoke(messages)
        return {"messages" :[response]}


    tool_node=ToolNode(tools) # Execute tool call


    # Defining graph and nodes
    graph = StateGraph(ChatState)

    # Nodes
    graph.add_node('chat_node',chat_node)
    graph.add_node('tool_node',tool_node)

    # Edges
    graph.add_edge(START,'chat_node')
    graph.add_conditional_edges("chat_node",tools_condition)
    graph.add_edge("tools" , "chat_node")

    # Compile graph
    chatbot = graph.compile()
    
    return chatbot

async def main():
    chatbot = await build_graph()
    result = await chatbot.ainvoke({'messages':[HumanMessage(content ="what is stock price of apple")]})
    print(result['messages'][-1].content)

    if __name__ == '__main__':
        asyncio.run(main())

    
 
#########################################################################
''' Above Mcp sever is used is local  (file Created locally)
what if MCP sever is Remote Or Deployed
Code Changes do:

client = MultiServerMCPClient(
    {      
        "expense": {   
            "transport": "streamable_http",  # if this fails, try "sse"
            "url": "https://splendid-gold-dingo.fastmcp.app/mcp" # uRL of MCp
        }
    }
)




 '''

