# Import necessary libraries
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader

# Load environment variables
load_dotenv()

# Load documents from a directory (you can change this path as needed)
documents = SimpleDirectoryReader("data").load_data()

from openai import OpenAI
import json

from langchain.text_splitter import RecursiveCharacterTextSplitter

def recursive_character_splitting(text, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks

client = OpenAI()

# Function to generate questions and answers
def generate_qa(prompt, text, temperature=0.2):    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}],
        temperature=temperature,
    )
    
    print(response.choices[0].message.content)

    # Strip extraneous symbols from the response content
    content = response.choices[0].message.content.strip()
    
    # Remove potential JSON code block markers
    content = content.strip()
    if content.startswith('```'):
        content = content.split('\n', 1)[-1]
    if content.endswith('```'):
        content = content.rsplit('\n', 1)[0]
    content = content.strip()
    
    # Attempt to parse the cleaned content as JSON
    try:
        parsed_content = json.loads(content.strip())
        return parsed_content
    except json.JSONDecodeError:
        print("Error: Unable to parse JSON. Raw content:")
        print(content)
        return []

factual_prompt = """
You are an expert children's content creator tasked with generating questions about characters in stories based on the following document excerpt. These questions should focus on retrieving specific details, roles, characteristics, and educational content or lessons from the text.

Instructions:

- Generate **5** questions about the characters, each with a corresponding **expected_output**.
- Ensure all questions are directly related to the document excerpt.
- Present the output in the following structured JSON format:

[
  {
    "question": "What is the main goals of the story described in the document?",
    "expected_output": "To entertain young readers with fictional adventures which may also have an educational values."
  },
  {
    "question": "Who is the main character mentioned in the document?",
    "expected_output": "The Happy Prince"
  }
]
"""

# Generate dataset
import os
import json

dataset_file = 'qa_dataset.json'

if os.path.exists(dataset_file):
    # Load dataset from local file if it exists
    with open(dataset_file, 'r') as f:
        dataset = json.load(f)
else:
    # Generate dataset if local file doesn't exist
    dataset = []

    for doc in documents:
        # Split the text
        chunks = recursive_character_splitting(doc.text, 100, 0)
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}:\n{chunk}\n")
            qa_pairs = generate_qa(factual_prompt, chunk, temperature=0.2)
            dataset.extend(qa_pairs)
    
    # Write dataset to local file
    with open(dataset_file, 'w') as f:
        json.dump(dataset, f)

        
# Note: we're choosing to create the dataset in Langfuse below, but it's equally easy to create it in another platform.

from langfuse import Langfuse
langfuse = Langfuse()

dataset_name = "storyteller_qa_pairs"
langfuse.create_dataset(name=dataset_name);

for item in dataset:
  langfuse.create_dataset_item(
      dataset_name=dataset_name,
      input=item["question"],
      expected_output=item["expected_output"]
)
