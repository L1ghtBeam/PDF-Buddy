# PDF-Buddy
Application with the goal of making studying easier for students and increasing
accessibility to generative AI. This program allows for the creation of "study
buddies" which when provided with study materials, such as class textbooks and
presentations, will provide the user with accurate information relevant to
their study. Study buddies will prioritize information from the provided class
materials, keeping their information more relevant than a normal generative AI
chatbot.

PDF-Buddy accepts many formats, not just PDFs like in the name. Acceptable
files formats include PDF, Powerpoint presentations, Word documents, various
programming languages, raw text files, and many other formats. All possible
formats which the study buddy can use are listed
[here in OpenAI documentation.](https://platform.openai.com/docs/assistants/tools/file-search/supported-files)

PDF-Buddy uses OpenAI's Assistants API to make generative AI calls and Vector
stores to store study material for easy access. Usage of this program will
require an OpenAI account and an initial payment of $5 to use their API. The 
program has been tested with GPT-4o and GPT-4o mini.

## Dependencies

* python >= 3.8
* openai-python == 1.40.8 (or latest if no breaking changes)
* python-dotenv >= 1.0.1

## Installation

* Clone this repository to your local machine
`git clone https://github.com/L1ghtBeam/PDF-Buddy.git`

* Setup a virtual environment to install dependencies into and activate the
venv:

```
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

* [Get an API key from the OpenAI dashboard here](https://platform.openai.com/api-keys).
It's recommended to create a new project before creating a new secret key. Usage
will require you add at least $5 worth of credits to your OpenAI credit
balance. A ChatGPT Plus subscription will not suffice.


* Create a `.env` file in the cloned repository with the following contents,
adding your API key after the equals sign:

```
OPENAI_API_KEY=
```

### Running

* Activate the virtual environment (if you haven't already)
`.venv\Scripts\activate`

* Run the program `python pdf_buddy.py`