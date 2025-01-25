# CodeInit
Interview Diaries Assistant. This repo is built as an answer to the statement "Your challenge is to build an end-to-end Scraping and Advice System that empowers students to make informed decisions by leveraging data from "Interview Diaries."

# Chunkychunks.py
This code processes a text file containing interview experiences and splits them into individual sections based on specific header patterns. It validates and cleans 
the extracted chunks to ensure proper formatting. 
1 *Chunk Splitting*- Detects headers using flexible regular expressions.- Handles both supported formats:
  - `YYYY | WEEK X | ISSUE Y`
  - `YYYY | ISSUE X | ARTICLE Y`
2 *Validation*- Ensures all chunks conform to the expected header format.
3 *Error Handling*- Catches exceptions during file reading and processing.
                  - Prints meaningful error messages
4 *Year Distribution Analysis*- Extracts and counts the year of each interview for reporting.


