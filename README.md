# scheherazade-ai-storyteller
scheherazade is an AI storyteller. It uses LLMs to generate a short bedtime story for kids based on a given prompt. It is named after the storyteller of the Arabian Nights.

## Features

## Prerequisites

- Python 3.7+
- API keys for OpenAI and/or RunPod (depending on chosen model) and LangSmith (for running evaluation on datasets)

## Installation and Setup

1. **Clone the Repository**:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. **API Keys**: 
   - Copy the `.env.sample` file and rename it to `.env`
   - Replace the placeholder values with your actual API keys and Runpod endpoints
   - Note: Runpod keys are optional

2. **Model Selection**:
   - Choose the desired model by setting the `config_key` variable in `app.py`.

3. **System Prompts Context**:
   - Adjust the `ENABLE_SYSTEM_PROMPT`.

4. **Customize Prompts**:
   - Modify the prompt templates in the `prompts.py` file to suit your context.

## Running the Application

1. **Activate the Virtual Environment** (if not already activated):
   ```sh
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

2. **Run the Chainlit App**:
   ```sh
   chainlit run app.py -w
   ```

3. Open your browser and navigate to the URL displayed in the terminal.

4. **Evaluation**:
   ```sh
   python3 eval.py
   ```
   Use this command to use LangSmith to evaluate the model's performance. Modify the prompt in "evaluation_prompt" to change how the evaluations are done

## Usage

- Start a conversation with the Scheherazade by giving it some information about a story you want to be created and the age of the audience.
- The application will process your input, generate a story and return it to you.
- You can converse with the application and ask it to modify the story in any way you like, refine it, add or remove elements and even convert it into a poem!

## Key Components

- `app.py`: Main application file containing the Chainlit setup and message handling logic.
- `prompts.py`: Contains prompt templates for the model instructing it to create a story.
- `eval.py`: Contains prompt templates evaluations which can be run on LangSmith to verify and evaluate the model ouptuts

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License.
