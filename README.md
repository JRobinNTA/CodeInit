# CodeInit
Interview Diaries Assistant. This repo is built as an answer to the statement "Your challenge is to build an end-to-end Scraping and Advice System that empowers students to make informed decisions by leveraging data from "Interview Diaries."

# Chunkychunks.py
This code processes a text file containing interview experiences and splits them into individual sections based on specific header patterns. It validates and cleans the extracted chunks to ensure proper formatting
1. *Chunk Splitting*- Detects headers using flexible regular expressions.- Handles both supported formats:
  - `YYYY | WEEK X | ISSUE Y`
  - `YYYY | ISSUE X | ARTICLE Y`
2. *Validation*- Ensures all chunks conform to the expected header format.
3. *Error Handling*- Catches exceptions during file reading and processing.
                  - Prints meaningful error messages
4. *Year Distribution Analysis*- Extracts and counts the year of each interview for reporting.

# Dataprep.py
It writes the processed data into another file and performs further analysis such as year distribution. The `treat_data` function is used to extract structured information from each chunk
1. Reads the input file `output.txt`.
2. Processes the file using `process_interview_file`.
3. Prints details about each interview chunk, including:
   - Header.
   - Content preview.
   - Chunk length.
4. Writes each chunk to a new file `midway.txt`.
5. Prints year distribution across all interviews.
6. Calls `treat_data` on each chunk for further data processing
-> *Additional key feature* - Structured Data Extraction
    - Uses `treat_data` to convert raw text into structured JSON for better usability

# JstoRag.py
[1. Reads the input file.
2. Calls `split_interviews` to extract chunks.
3. Validates the chunks using `validate_chunks`.
4. Returns the processed chunks or an empty list in case of errors]

# midway.txt
This document contains the details of all the interviews listed on the "Interview Diaries" site. Every interview includes pieces of information regarding the offering company, recruitment role, no. of rounds in the whole process, details regarding each round, and many more. When the user inputs some prompt to the LLM model, it returns sorted info  from this whole information, as per the specific prompt given by the user.

# output.txt
Similar to midway.txt

# rag.py
This Python script facilitates document processing and integrates with ChromaDB, a vector database, for storage and query operations. It supports resetting the database, processing documents, splitting them into smaller chunks, and querying the database for specific information. The script is designed for extensibility and ease of use.





