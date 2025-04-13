import json
import logging
import re
from typing import List, Optional
from urllib.parse import urlparse

import tiktoken
from openai import OpenAI
from openai.types.chat import ChatCompletion
from tqdm import tqdm

from ai_assistant_tester.prompts import format_knowledge_base_chunk
from ai_assistant_tester.scraping.WebCrawler import WebCrawler
from ai_assistant_tester.utils.utils import get_file_content, get_openai_api_key


class KnowledgeBaseFormatter:
    """
    A class to crawl a website, extract textual content, chunk it based on token limits,
    and reformat it using OpenAI's GPT models into a clean Markdown knowledge base.
    Also supports generation of a question-answer set with a specified number of pairs.
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        max_tokens_per_chunk: int = 1000,
        temperature: float = 0.0,
    ):
        """
        Initialize the formatter with OpenAI settings.

        Args:
            model (str): OpenAI model name.
            max_tokens_per_chunk (int): Max tokens per text chunk.
            temperature (float): Sampling temperature for generation.
        """
        self.model = model
        self.max_tokens = max_tokens_per_chunk
        self.temperature = temperature
        self.client = OpenAI(api_key=get_openai_api_key())
        self.encoding = tiktoken.encoding_for_model(model)
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You will help format a long knowledge base in small parts. Each part "
                    "continues the previous one. Maintain coherence and don't repeat what has been said."
                ),
            }
        ]

    def crawl_site(
        self,
        start_url: str,
        cli: bool = False,
        output_file: Optional[str] = None,
        max_depth: int = 2,
    ) -> str:
        """
        Crawl a website and return its full aggregated markdown content.

        Args:
            start_url (str): URL to start crawling from.
            cli (bool): Enable verbose output.
            output_file (Optional[str]): Optional file to write results to.
            max_depth (int): Max crawl depth.

        Returns:
            str: Aggregated raw content from all pages.
        """
        domain = urlparse(start_url).netloc
        crawler = WebCrawler(
            domain=domain,
            cli=cli,
            output_file=output_file,
            max_depth=max_depth,
        )
        crawler.crawl(start_url)

        return "\n\n".join(crawler.results.values())

    def _chunk_text(self, text: str) -> List[str]:
        """
        Chunk text by paragraphs while staying under token limit.

        Args:
            text (str): Full input text.

        Returns:
            List[str]: List of token-safe chunks.
        """
        paragraphs = text.split("\n\n")
        chunks, current_chunk = [], []

        for p in paragraphs:
            tentative = "\n\n".join(current_chunk + [p])
            if len(self.encoding.encode(tentative)) <= self.max_tokens:
                current_chunk.append(p)
            else:
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                current_chunk = [p]

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
        return chunks

    def _format_chunk(self, chunk: str, prompt: str) -> Optional[str]:
        """
        Format a single chunk using GPT.

        Args:
            chunk (str): Raw unformatted text.
            prompt (str): A prompt template with a placeholder {chunk_text}.

        Returns:
            str: Formatted output from GPT.
        """

        formatted_prompt = prompt.format(chunk_text=chunk)
        self.messages.append({"role": "user", "content": formatted_prompt})
        response: ChatCompletion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        formatted_message = response.choices[0].message.content
        if formatted_message:
            self.messages.append({"role": "user", "content": formatted_message})
        return formatted_message

    def format_knowledge_base(self, raw_text: str) -> str:
        """
        Format the full knowledge base by chunking and processing with OpenAI.

        Args:
            raw_text (str): The full, raw extracted content.

        Returns:
            str: The complete, formatted knowledge base.
        """
        chunks = self._chunk_text(raw_text)
        result = ""
        for chunk in chunks:
            formatted_chunk = self._format_chunk(chunk, format_knowledge_base_chunk)
            if formatted_chunk:
                result += "\n\n" + formatted_chunk

        return result

    def save_to_file(self, content: str, output_file: str = "output.md") -> None:
        """
        Save text content to file.

        Args:
            content (str): Text content to save.

        Returns:
            None
        """
        with open(output_file, "w") as f:
            f.write(content)

    def generate_question_answer_set(self, filepath: str, num_pairs: int = 10) -> dict:
        """
        Generate a set of question-answer pairs from a given knowledge base file.
        This method processes the file content by chunking it and, for each chunk,
        instructs the model to generate exactly `num_pairs` diverse Q&A pairs.
        Each call uses a fresh conversation context to avoid interference from prior messages.

        Args:
            filepath (str): The path to the knowledge base file.
            num_pairs (int): The number of Q&A pairs to generate per chunk.

        Returns:
            dict: A dictionary containing all Q&A pairs in the format {"qas": [...] }.
        """
        # Load and chunk the knowledge base text.
        knowledge_base = get_file_content(filepath)
        chunks = self._chunk_text(knowledge_base)

        # Define a prompt template for generating the Q&A pairs.
        qa_prompt_template = (
            "Based on the following knowledge base text, generate exactly {num_pairs} diverse "
            "question-answer pairs that test key concepts. "
            "Return the output strictly as a JSON object with a key 'qas' that is a list of exactly {num_pairs} objects, "
            "each with keys 'question' and 'answer'.\n\n"
            "Knowledge base text:\n{chunk_text}"
        )

        all_qas = []
        for i, chunk in enumerate(chunks):
            prompt = qa_prompt_template.format(num_pairs=num_pairs, chunk_text=chunk)
            logging.info(f"Processing chunk {i+1} of {len(chunks)}")
            # Create a fresh set of messages for each chunk to isolate context.
            qa_messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a highly experienced educational content generator. "
                        f"Your task is to generate exactly {num_pairs} diverse and high-quality question-answer pairs "
                        "based on the provided knowledge base text. "
                        "Return only valid JSON with a single key 'qas', whose value is a list of exactly "
                        f"{num_pairs} objects. Each object must have two keys: 'question' and 'answer'."
                    ),
                },
                {"role": "user", "content": prompt},
            ]

            logging.info("Waiting for OpenAI response...")
            response: ChatCompletion = self.client.chat.completions.create(
                model=self.model,
                messages=qa_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            resp_text = response.choices[0].message.content.strip()
            logging.debug(f"Raw response for chunk {i+1}: {resp_text}")

            # Remove markdown code fences if present.
            resp_text = re.sub(r"^```(?:\w+)?\s*", "", resp_text)
            resp_text = re.sub(r"\s*```$", "", resp_text)

            try:
                json_output = json.loads(resp_text)
                if "qas" in json_output and isinstance(json_output["qas"], list):
                    pairs = json_output["qas"]
                    # Trim extra Q&A pairs, or warn if not enough pairs.
                    if len(pairs) > num_pairs:
                        pairs = pairs[:num_pairs]
                    elif len(pairs) < num_pairs:
                        logging.warning(
                            f"Received only {len(pairs)} pairs instead of {num_pairs} in chunk {i+1}."
                        )
                    all_qas.extend(pairs)
            except Exception as e:
                logging.error(f"Error parsing JSON for chunk {i+1}: {e}")
                logging.debug("Response text was: " + resp_text)
                continue

        result = {"qas": all_qas}
        logging.info("Aggregated Q&A result generated.")
        return result


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    formatter = KnowledgeBaseFormatter(model="gpt-4o", max_tokens_per_chunk=1000)

    raw = formatter.crawl_site("https://example.com", cli=True)
    formatted = formatter.format_knowledge_base(raw)
    formatter.save_to_file(content=formatted, output_file="example.md")

    qa_set = formatter.generate_question_answer_set(filepath="example.md", num_pairs=10)
    with open("qa_set.json", "w") as f:
        json.dump(qa_set, f, indent=2)
