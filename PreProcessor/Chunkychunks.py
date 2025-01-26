import re
from typing import List
from Dataprep import treat_data

def split_interviews(text: str) -> List[str]:
    """
    Split the text into individual interview experiences with proper header separation.
    Handles both formats:
    - YYYY | WEEK X | ISSUE Y
    - YYYY | ISSUE X | ARTICLE Y
    """
    # Pattern for both header formats
    pattern = r'(\d{4}\s*\|\s*(WEEK\s*\d+\s*\|\s*ISSUE|ISSUE\s*\d+\s*\|\s*ARTICLE)\s*\d+)'

    # Find all starting positions of headers
    header_positions = []
    for match in re.finditer(pattern, text):
        header_positions.append(match.start())

    # Split text into chunks using the positions
    chunks = []
    for i in range(len(header_positions)):
        start_pos = header_positions[i]
        # If this is not the last chunk, use next header position as end
        end_pos = header_positions[i + 1] if i < len(header_positions) - 1 else len(text)
        chunk = text[start_pos:end_pos].strip()
        chunks.append(chunk)

    # Clean up chunks
    cleaned_chunks = []
    for chunk in chunks:
        # Find the header
        header_match = re.match(pattern, chunk)
        if header_match:
            header = header_match.group(0)
            # Get the content after the header
            content = chunk[len(header):].strip()
            # Reconstruct with proper separation
            cleaned_chunk = f"{header}\n{content}"
            cleaned_chunks.append(cleaned_chunk)

    return cleaned_chunks

def validate_chunks(chunks: List[str]) -> bool:
    """
    Validate that each chunk starts with the expected pattern.
    Handles both formats.
    """
    pattern = r'^\d{4}\s*\|\s*(WEEK\s*\d+\s*\|\s*ISSUE|ISSUE\s*\d+\s*\|\s*ARTICLE)\s*\d+'
    return all(re.match(pattern, chunk.strip()) for chunk in chunks)

def process_interview_file(file_path: str) -> List[str]:
    """
    Process the interview file and return validated chunks.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        chunks = split_interviews(text)

        if not validate_chunks(chunks):
            print("Warning: Some chunks may not be properly formatted")

        return chunks

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return []

# Use the function
file_path = 'output.txt'
interview_chunks = process_interview_file(file_path)

# Print results
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

for i,chunk in enumerate(interview_chunks,1):
    print(f" Processing Interview {i}")
    treat_data(chunk)
