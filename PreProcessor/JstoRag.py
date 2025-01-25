import json
from typing import List, Dict, Any

def prepare_interview_data_for_rag(interviews_data: List[Dict[str, Any]]) -> str:
    """Convert structured data into searchable text format for RAG."""
    documents = []
    for entry in interviews_data:
        document = f"""
        Company: {entry['Company name']}
        Cgpa Cutoff: {entry['cgpa_cutoff']}
        Role: {entry['Role']}
        Salary: {entry['Salary']}
        Interview Experiences: {entry['Interview Experiences']}
        Preparation Tips: {entry['Preperation Tips']}
        Key Focus Areas: {entry['Key Focus Areas']}
        Common Pitfalls: {entry['Common Pitfalls']}
        """

        documents.append(document)
    return "\n\n---\n\n".join(documents)
