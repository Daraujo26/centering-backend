# Centering Backend

This repository contains the backend for the Centering Theory demo. It is built with Flask and integrates an AllenNLP-based coreference resolution model to process input text and extract discourse coherence attributes.

## Features

- **Coreference Resolution**: Identifies coreferences in text using an AllenNLP model.
- **Discourse Analysis**: Implements Centering Theory to analyze coherence across utterances.
- **RESTful API**: Provides a `/center` endpoint for developers to interact with. You can modify this in the endpoints file.

## Prerequisites

Before running the project, ensure you have the following:
- Python 3.8+
- Virtual environment tools (e.g., `venv` or `virtualenv`)
- AllenNLP installed and configured in the repository. (See the [AllenNLP Installation Guide](https://docs.allennlp.org/) for setup instructions.)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Daraujo26/centering-backend.git
   cd centering-backend

2. Set Up a Virtual Environment:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

3. Install Dependencies:
  ```
  pip install -r requirements.txt
  ```

4. Install AllenNLP:
  ```
  pip install allennlp
  ```
  Ensure you have downloaded the required model files (e.g., for coreference resolution). Follow the official AllenNLP Installation Guide.

Run the Flask App:
  ```
  python run.py
  ```

Access the API:
By default, the app runs on http://127.0.0.1:PORT. Set the port in run.py, then make post requests following this:

```
curl -X POST "http://127.0.0.1:5000/<PORT>" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your input text here"}'
```

### Key Files

app/centering.py: Implements Centering Theory concepts, such as backward-looking (Cb) and forward-looking (Cf) centers.

app/coref_model.py: Loads and uses the AllenNLP model for coreference resolution.

endpoints/routes.py: Defines the /center endpoint, integrating the centering and coreference functionality.

### Contributing
We welcome contributions! To get started:

Fork the repository.
Create a new branch for your feature or bug fix.
Submit a pull request.
