import argparse
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"


def pre_rag(user_prompt):
    SUMMERY_TEMPLATE = f'''
            take this input and make this into clear key words and output just that nothing else
            no fullforms of words in the answer just keyword the below is the keyword to look for in user prompt will ```json
[
  "Stipend: 1,00,000",
  "Rounds: 4",
  "Test Round: 1",
  "Interview Rounds: 2",
  "HR Round: 1",
  "Round 1: Online test",
  "Coding questions: ball passing, logical operations (XOR)",
  "MCQs: OS, debugging, aptitude, English grammar",
  "Round 2: Interview 1",
  "DSA question: Alphabet representation (stack)",
  "General questions: Resume, projects, hackathons",
  "Round 3: Interview 2",
  "DSA question: String chain formation",
  "Puzzle: Gold boxes",
  "Array question: Repeated element > n/2",
  "Concepts: OOPS, Inheritance, Overriding",
  "Round 4: Interview 3",
  "Graph problem: Prerequisite checker",
  "Error detection in C code",
  "OOPS implementation: Cricket app",
  "Key skills: DSA, OS, OOPS, DBMS",
  "Resources: Leetcode, Neetcode series",
  "Preparation tips: Resume accuracy, honesty, readiness to learn",
  "Tech trends, behavioral questions"
]
u are a text summerizig and keyword finding machine act like it ur output is used fonr sematic search also keep words like ctc as it is no expansion

this is kind of key words to be taken care of 
```
            {user_prompt}

                        '''
    return SUMMERY_TEMPLATE

PROMPT_TEMPLATE = """
Answer the question based  on the following context:

{context}

---

from the above context aswer the question best suitably: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="enter prompt with starting")
    args = parser.parse_args()
    query_text = args.query_text
    model = Ollama(model='mistral')
    pre_rag_response = model.invoke(pre_rag(query_text))
    print(pre_rag_response)
    query_rag(pre_rag_response)




def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=15)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(context_text)
    print('*'*100)
    # print(prompt)

    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)
    # response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()
