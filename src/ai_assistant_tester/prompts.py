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
{extracted_text}

Provide your final formatted content as a complete Markdown document.
"""
