# chatbot-tester

---

# Knowledge Base & Q&A Generator – Usage Instructions

## Prerequisites

- **Python 3** (compatible with your project’s configuration, e.g., Python 3.13)
- **Virtual Environment Tools** (we'll use Python’s built-in `venv`)
- **OpenAI API Key** (obtain one from [OpenAI](https://platform.openai.com/account/api-keys))

## Steps to Set Up and Run

1. **Create a Virtual Environment**

   Open your terminal and run the following command to create a virtual environment named `venv`:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**

   Activate the virtual environment by running:

   ```bash
   source venv/bin/activate
   ```

3. **Install Poetry**

   Install Poetry within your activated environment:

   ```bash
   pip install poetry
   ```

4. **Install Project Dependencies**

   Use Poetry to install the dependencies defined in your `pyproject.toml`:

   ```bash
   poetry install
   ```

5. **Set Up Your OpenAI API Key**

   Export your OpenAI API key as an environment variable. Replace `"your_key"` with your actual key:

   ```bash
   export OPENAI_API_KEY="your_key"
   ```

6. **Install Your Package in Editable Mode**

   This step ensures your package is linked to the current source code. Run:

   ```bash
   pip install -e .
   ```

7. **Run the Knowledge Base Formatter and Q&A Generator**

   Finally, run your script to generate the formatted knowledge base and Q&A set:

   ```bash
   python3 src/ai_assistant_tester/knowledge_base/KnowledgeBaseFormatter.py
   ```

## Expected Output

- **example.md:** A formatted knowledge base generated from the scraped content.
- **qa_set.json:** A JSON file containing the generated question-answer pairs.

## Additional Notes

- Make sure your `pyproject.toml` is correctly set up with your dependencies.
- Ensure that the file paths in your commands match the structure of your repository.
- If you need to change the number of Q&A pairs, adjust the `num_pairs` parameter in the `generate_question_answer_set` call within your script.

