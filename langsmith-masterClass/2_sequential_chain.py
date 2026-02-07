from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
load_dotenv()

# We need to change every time langsmith project name(which is mention) in .env file 
# so instead of every time change name by going to .env we directly set name using {os.environ[]}
os.environ['LANGCHAIN_PROJECT'] = 'Sequentail LLM APP'

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model = ChatOpenAI()

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

# To get your manpasand metadata and tags in trace instead of deafult langsmith
config = {
    'run_name': 'sequentialLLM' , # By deafult in dashboard of langsmith Name is shown of by langsmith to ,change that or set by user   use it.
    'tags' : ['llm app' , 'report generation' , 'summarization'],
    'metadata': {'model1' : 'gpt-4o-mini' , 'model1_temp':0.7 , 'parser' : 'stroutputparser'}
}


# Now set config 
result = chain.invoke({'topic': 'Unemployment in India'} , config=config)

print(result)
