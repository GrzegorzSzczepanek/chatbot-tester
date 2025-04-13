format_knowledge_base_chunk = """
Task: Format the following extracted text into a well-structured, coherent knowledge base for an AI assistant.

Guidelines:
1. Format the text into clear, organized Markdown.
2. Remove any unnecessary information or repetitive details.
3. Retain all critical and important information.
4. Merge similar pieces of information where applicable.
5. Do not omit any new or crucial details.
6. Ensure the output is complete and easy to read.

Extracted Text:
{chunk_text}

Provide your final formatted content as a complete Markdown document.
"""

generate_question_answer_pairs = """
Based on the following content, generate 10 to 20 (number of them depends on amount of content) question–answer pairs that test the reader's understanding of key concepts. Format the output as JSON with each pair containing a 'question' and an 'answer'. Ensure the questions are clear, concise, and cover both high-level ideas and specific details of the provided text.
Provided text:
{chunk_text}
"""
