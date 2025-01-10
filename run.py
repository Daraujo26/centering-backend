from endpoints.routes import app
import os

# Set environment variable to avoid HuggingFace tokenizer parallelism warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=<PORT>, debug=True, use_reloader=False)
