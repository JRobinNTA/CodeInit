# Django REST Framework API

This project provides a Django REST framework API for user registration, login, portfolio management, and processing prompts using an NLP module.

## Table of Contents

- [Installation](#installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [Register User](#register-user)
  - [Login User](#login-user)
  - [Get/Update Portfolio](#getupdate-portfolio)
  - [Process Prompt](#process-prompt)
- [License](#license)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/JRobinNTA/django-drf-api.git
   cd django-drf-api
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

### Summary

1. **Scraping the Website:** Extract links and data using `BeautifulSoup` or `Scrapy`.
2. **Processing and Formatting Data:** Clean and format the scraped data.
3. **Converting Data to JSON using LLM:** Use a language model to convert the data to JSON.
4. **Embedding Data in ChromaDB:** Store and index the JSON data in ChromaDB.
5. **Serving the Web Application with DRF and React:** Create a Django REST Framework API and a React frontend to serve and display the data.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
