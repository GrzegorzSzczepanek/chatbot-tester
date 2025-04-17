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


system_answer_evaluation = """
You are an expert QA evaluator. Your job is to look at each question, the “reference answer” (the ideal answer), and the “assistant answer” (what the chatbot actually produced). For each item, decide whether the assistant answer is:

• Correct – it captures all the key facts in the reference answer.  
• Partial – it captures some but misses or slightly distorts important points.  
• Incorrect – it fails to capture the key facts or is outright wrong.

Return your evaluation as a JSON array of objects, one per item, with exactly these fields:

  {
    "index": 1,         // the 1‑based question number
    "verdict": "Correct",   // one of Correct/Partial/Incorrect
    "score": 1.0,           // 1.0 for Correct, 0.5 for Partial, 0.0 for Incorrect
    "notes": "..."          // a brief rationale for your choice
  }
"""

user_answer_evaluation = """
Please evaluate the following list of items and return ONLY the JSON array described above:

{
  "items": [
    {
      "question": "What is the primary purpose of the Example Domain?",
      "reference": "The primary purpose of the Example Domain is to serve as a placeholder or example in various types of documentation.",
      "actual":   "The primary purpose of the Example Domain is to serve as a placeholder or example in various types of documentation."
    },
    {
      "question": "Is prior approval required to use the Example Domain in materials?",
      "reference": "No, prior approval is not required to use the Example Domain in materials.",
      "actual":   "No, prior approval is not required to use the Example Domain in materials."
    },
    …  // include all your items here
  ]
}
"""
