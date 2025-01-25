import requests
import json
#import datastore
def treat_data(data):
    prompt =f'''
You are an expert data extraction and analysis assistant. Your task is to process raw text data from "Interview Diaries" and extract relevant, structured information for students preparing for interviews. Focus on company names, Cgpa cutoffs, roles, Salaries, interview experiences, question asked, preparation tips, and key focus areas.
Prompt:

Input Text:

[{data}]

Task Instructions:

    Identify and Extract the Following Information:
        Company Name: The company associated with the interview.
        Cgpa Cutoff: The minimum CGPA required for the interview.
        Role: The job role or position discussed in the diary.
        Salary: The compensation or salary or CTC details mentioned in the diary.
        Interview Experiences: Summarize the key stages of the interview process and challenges faced.
        Questions asked: List specific questions or types of questions mentioned in the diary.
        Preparation Tips: Extract specific advice or preparation strategies shared by the author.
        Key Focus Areas: Highlight the technical and soft skills emphasized for this interview.
        Common Pitfalls: Mention mistakes or areas to avoid as per the author's advice.

    Output Format (Structured JSON):

{{
  "Company Name": "<Extracted Company Name>",
  "Cgpa Cutoff": "<Extracted Cgpa Cutoff>",
  "Role": "<Extracted Job Role>",
  "Salary": "<Extracted Compensation Details>",
  "Interview Experiences": "<Summary of Interview Process>",
  "Questions asked": ["<Question 1>", "<Question 2>", "<Question 3>"],
  "Preparation Tips": ["<Tip 1>", "<Tip 2>", "<Tip 3>"],
  "Key Focus Areas": ["<Skill 1>", "<Skill 2>", "<Skill 3>"],
  "Common Pitfalls": ["<Mistake 1>", "<Mistake 2>"]
}}

Ensure that the extracted information is accurate, clear, concise and follows the json format. Skip irrelevant details.

Example Output:

{{
  "Company Name": "Google",
  "Cgpa Cutoff": "8.5",
  "Role": "Software Engineer",
  "Salary": "600000",
  "Interview Experiences": "The interview had 3 rounds: a coding assessment, a technical interview, and a behavioral round. The coding round focused on algorithms and data structures.",
  "Questions asked": ["What is the time complexity of quicksort?", "Design a parking lot system."],
  "Preparation Tips": ["Focus on system design questions.", "Brush up on dynamic programming.", "Be prepared for situational behavioral questions."],
  "Key Focus Areas": ["Algorithms", "System Design", "Behavioral Skills"],
  "Common Pitfalls": ["Underestimating time management during coding assessments.", "Not clarifying questions during technical interviews."]
}}

Note: If some details are missing from the text, indicate them as "Not mentioned" in the JSON. If you need to add a note to the response start it with a "#" character. Do not include the any other text to the response just give the json output and nothing else
'''

    url =  'http://localhost:11434/api/generate'

    headers ={
        'Content-Type': 'application/json'
    }

    data ={
        'model': 'llama3.1',
        'prompt': prompt,
        'stream':False,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_got = response.text
        data = json.loads(response_got)
        key= data.keys()
        output = data['response']
        print(output)
        with open('output.json', 'a') as f:
            f.write(f"{output}\n")
        # print(key)

    else:
        print(f'error: {response.status_code}')

#treat_data(datastore.data_returner())
