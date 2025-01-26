import json
from typing import List, Dict, Any

def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Read JSON file and handle potential errors.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {str(e)}")
        return []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []

def format_list(items: List[str]) -> str:
    """
    Format a list of items into a bullet-pointed string.
    """
    if not items:
        return "Not specified"
    return "\n  - " + "\n  - ".join(items)

def format_interview_entry(entry: Dict[str, Any]) -> str:
    """
    Format a single interview entry into readable text.
    """
    template = """
Company: {company}
CGPA Cutoff: {cgpa}
Role: {role}
Salary: {salary}
Interview Experiences: {experiences}
Questions Asked: {questions}
Preparation Tips: {tips}
Key Focus Areas: {focus}
Common Pitfalls: {pitfalls}
"""
    return template.format(
        company=entry.get('Company Name', 'Not specified'),
        cgpa=entry.get('Cgpa Cutoff', 'Not specified'),
        role=entry.get('Role', 'Not specified'),
        salary=entry.get('Salary', 'Not specified'),
        experiences=entry.get('Interview Experiences', 'Not specified'),
        questions=format_list(entry.get('Questions asked', [])),
        tips=format_list(entry.get('Preparation Tips', [])),
        focus=format_list(entry.get('Key Focus Areas', [])),
        pitfalls=format_list(entry.get('Common Pitfalls', []))
    )

def convert_json_to_text(input_file: str, output_file: str) -> bool:
    """
    Convert JSON file to formatted text file.
    """
    try:
        # Read JSON data
        data = read_json_file(input_file)
        if not data:
            return False

        # Format each entry
        formatted_entries = []
        for entry in data:
            formatted_text = format_interview_entry(entry)
            formatted_entries.append(formatted_text)

        # Join entries with clear separation
        final_text = "\n\n" + "="*50 + "\n\n".join(formatted_entries) + "\n\n" + "="*50 + "\n\n"

        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_text)

        print(f"Successfully converted {len(data)} entries to {output_file}")
        return True

    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return False

def main():
    # File paths
    input_file = 'output.json'
    output_file = 'formatted_interviews.txt'

    # Convert files
    success = convert_json_to_text(input_file, output_file)

    if success:
        # Print some statistics
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"\nOutput file size: {len(content)} characters")
            print(f"Number of lines: {len(content.split('\n'))}")

if __name__ == "__main__":
    main()
