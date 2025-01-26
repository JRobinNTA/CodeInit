from langchain.llms import Ollama
import sys
import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .rag import query_search


def process_prompt(llm, prompt_text):
    """Process the prompt and return response"""
    try:
        response = llm.invoke(prompt_text)
        print(f"Response llm: {response}")
        return response

    except Exception as e:
        print(f"Error processing prompt: {e}")
        return None

def prompt_template(prompt_text,context,portfolio):
    """Template for generating prompts"""
    return f'''
    portfolio = {portfolio}
    context = {context}
    strictly following the context answer to the below prompt by user,
    the details of the user is given as portfolio use the relevant details from it to generate helpful response,
    use  natural language and cite the source which is the context
    prompt = {prompt_text}

'''


def initialize_llama():
    """Initialize the Llama model"""
    try:
        llm = Ollama(model="llama3.1" )
        return llm
    except Exception as e:
        print(f"Error initializing Llama model: {e}")
        sys.exit(1)
def main(prompt,portfolio):
    #prompt = input("Enter your prompt: ")
    context_got=query_search(prompt)
    llm_input = prompt_template(context=context_got,prompt_text=prompt,portfolio=portfolio)
    response=process_prompt(llm=initialize_llama(),prompt_text=llm_input)
    return response


if __name__ == "__main__":
    main(prompt="Hello",portfolio="jimmy")
