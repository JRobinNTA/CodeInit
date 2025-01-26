from langchain.llms import Ollama
import sys
import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag import query_search


def process_prompt(llm, prompt_text):
    """Process the prompt and return response"""
    try:
        response = llm.invoke(prompt_text)
        print(f"Response llm: {response}")
        return response
        
    except Exception as e:
        print(f"Error processing prompt: {e}")
        return None

def prompt_template(prompt_text,context):
    """Template for generating prompts""" 
    return f'''
    context = {context}
    strictly following the context aswer to the below prompt by user 
    use  natural language and cite the source which is the context 
    prompt = {prompt_text}

'''


def initialize_llama():
    """Initialize the Llama model"""
    try:
        llm = Ollama(model="mistral" )
        return llm
    except Exception as e:
        print(f"Error initializing Llama model: {e}")
        sys.exit(1)
def main():
    prompt = input("Enter your prompt: ")
    context_got=query_search(prompt)
    llm_input = prompt_template(context=context_got,prompt_text=prompt)
    process_prompt(llm=initialize_llama(),prompt_text=llm_input)
    
   

if __name__ == "__main__":
    main()
