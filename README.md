# Interview Processor and Web Application

This project is designed to process interview experiences from a text file, split them into individual chunks, validate their format, and perform data treatment using the `treat_data` function from the `Dataprep` module. The processed data is then embedded in ChromaDB and served through a web application using Django REST Framework (DRF) and React.

## Table of Contents

- [Installation](#installation)
- [Running the Server](#running-the-server)
- [Workflow Overview](#workflow-overview)
- [API Endpoints](#api-endpoints)
  - [Register User](#register-user)
  - [Login User](#login-user)
  - [Get/Update Portfolio](#getupdate-portfolio)
  - [Process Prompt](#process-prompt)
- [Functions](#functions)
- [Example](#example)
- [License](#license)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/JRobinNTA/interview-processor.git
   cd interview-processor
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**

   ```bash
   python manage.py createsuperuser
   ```

## Running the Server

To run the Django development server, use the following command:

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`.

## Workflow Overview

1. **Scraping the Website**
2. **Processing and Formatting Data**
3. **Converting Data to JSON using LLM**
4. **Embedding Data in ChromaDB**
5. **Serving the Web Application with DRF and React**

### 1. Scraping the Website

**Objective:** Extract links and data from a target website.

**Steps:**
- Use a web scraping library like `BeautifulSoup` or `Scrapy` to scrape the website.
- Identify and extract the relevant links and data from the HTML content.

### 2. Processing and Formatting Data

**Objective:** Clean and format the scraped data for further processing.

**Steps:**
- Clean the extracted data to remove any unwanted characters or HTML tags.
- Format the data into a structured format (e.g., dictionary).

### 3. Converting Data to JSON using LLM

**Objective:** Use a language model (LLM) to convert the cleaned data into JSON format.

**Steps:**
- Pass the cleaned data to the LLM to generate JSON.
- Use the generated JSON for further processing.

### 4. Embedding Data in ChromaDB

**Objective:** Embed the JSON data into ChromaDB for efficient retrieval.

**Steps:**
- Use ChromaDB to store and index the JSON data.
- Ensure the data is properly embedded for efficient querying.

### 5. Serving the Web Application with DRF and React

**Objective:** Serve the processed data through a web application using Django REST Framework (DRF) and React.

**Steps:**
- Create a Django REST Framework API to serve the data.
- Create a React frontend to interact with the API and display the data.

## API Endpoints

### Register User

**Endpoint:** `/api/register/`
**Method:** `POST`
**Description:** Register a new user.

**Request Body:**

```json
{
  "username": "your_username",
  "password": "your_password",
  "email": "your_email@example.com"
}
```

**Response:**

```json
{
  "token": "user_token"
}
```

### Login User

**Endpoint:** `/api/login/`
**Method:** `POST`
**Description:** Login an existing user.

**Request Body:**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**

```json
{
  "token": "user_token"
}
```

### Get/Update Portfolio

**Endpoint:** `/api/portfolio/`
**Method:** `GET` or `PUT`
**Description:** Get or update the user's portfolio. Requires authentication.

**Request Headers:**

```http
Authorization: Token user_token
```

**GET Response:**

```json
{
  "username": "your_username",
  "year": "your_year",
  "branch": "your_branch",
  "skills": ["skill1", "skill2"]
}
```

**PUT Request Body:**

```json
{
  "year": "new_year",
  "branch": "new_branch",
  "skills": ["new_skill1", "new_skill2"]
}
```

**PUT Response:**

```json
{
  "username": "your_username",
  "year": "new_year",
  "branch": "new_branch",
  "skills": ["new_skill1", "new_skill2"]
}
```

### Process Prompt

**Endpoint:** `/api/process_prompt/`
**Method:** `POST`
**Description:** Process a prompt using the user's portfolio and the NLP module. Requires authentication.

**Request Headers:**

```http
Authorization: Token user_token
```

**Request Body:**

```json
{
  "prompt": "your_prompt"
}
```

**Response:**

```json
{
  "response": "NLP_response"
}
```

## Functions

### `split_interviews(text: str) -> List[str]`

Splits the text into individual interview experiences with proper header separation. Handles both formats:
- `YYYY | WEEK X | ISSUE Y`
- `YYYY | ISSUE X | ARTICLE Y`

- **Parameters:**
  - `text`: The text containing multiple interview experiences.

- **Returns:**
  - A list of individual interview chunks.

### `validate_chunks(chunks: List[str]) -> bool`

Validates that each chunk starts with the expected pattern. Handles both formats.

- **Parameters:**
  - `chunks`: A list of interview chunks.

- **Returns:**
  - `True` if all chunks are properly formatted, `False` otherwise.

### `process_interview_file(file_path: str) -> List[str]`

Processes the interview file and returns validated chunks.

- **Parameters:**
  - `file_path`: The path to the text file containing interview experiences.

- **Returns:**
  - A list of validated interview chunks.

### `treat_data(chunk: str)`

Processes the individual interview chunk using the `treat_data` function from the `Dataprep` module.

- **Parameters:**
  - `chunk`: The individual interview chunk to be processed.

## Example

Here's an example of how to use the script:

```python
from your_module import process_interview_file, treat_data

file_path = 'output.txt'
interview_chunks = process_interview_file(file_path)

for i, chunk in enumerate(interview_chunks, 1):
    print(f"\n=== Interview {i} ===")
    lines = chunk.split('\n')
    print(f"Header: {lines[0]}")
    print("Content preview:", ' '.join(lines[1:])[:150] + "...")
    print("Length:", len(chunk))
    print("---")
    with open('midway.txt', 'a') as f:
        f.write(f"{chunk}\n")

# Optional: Print year distribution to verify both formats are captured
years = [re.search(r'(\d{4})', chunk.split('\n')[0]).group(1)
         for chunk in interview_chunks
         if re.search(r'(\d{4})', chunk.split('\n')[0])]
print("\nYear distribution:")
for year in sorted(set(years)):
    count = years.count(year)
    print(f"Year {year}: {count} interviews")

for i, chunk in enumerate(interview_chunks, 1):
    print(f"Processing Interview {i}")
    treat_data(chunk)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
