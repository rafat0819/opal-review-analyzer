# OPAL Review Analyzer Tool

A FastAPI-based microservice that analyzes customer reviews using sentiment analysis and categorization. Built for integration with the OPAL AI platform.

## Features

- **Sentiment Analysis**: Analyzes review text to determine positive, negative, or neutral sentiment
- **Smart Categorization**: Automatically categorizes reviews into:
  - Technical Issues (bugs, crashes, errors)
  - Guidance Requests (help, how-to questions)
  - Positive Feedback
  - Negative Feedback
  - Neutral Comments
- **OPAL Integration**: Exposed as a tool via OPAL Tools SDK
- **Comprehensive Testing**: 14 unit tests covering core functionality and edge cases

## Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **TextBlob**: Natural language processing for sentiment analysis
- **OPAL Tools SDK**: Integration with OPAL AI platform
- **Pydantic**: Data validation
- **pytest**: Testing framework

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd opal_voc
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running Locally

1. Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

2. Access the API documentation:
```
http://localhost:8000/docs
```

### Exposing with ngrok (for OPAL integration)

1. Install ngrok:
```bash
brew install ngrok/ngrok/ngrok  # macOS
```

2. Configure your authtoken:
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN
```

3. Start ngrok tunnel:
```bash
ngrok http 8000
```

4. Use the provided public URL with OPAL

## Testing

Run the test suite:
```bash
pytest test_main.py -v
```

Run with coverage report:
```bash
pytest test_main.py -v --cov=main --cov-report=html
```

## API Example

**Input:**
```json
{
  "text": "The app keeps crashing when I try to login"
}
```

**Output:**
```json
{
  "sentiment_score": -0.25,
  "category": "Technical Issue",
  "summary": "Detected Technical Issue with score -0.25"
}
```

## Project Structure

```
opal_voc/
├── main.py                      # FastAPI application and tool definition
├── test_main.py                 # Unit tests
├── requirements.txt             # Python dependencies
├── Troubleshooting_Guide.txt    # Platform troubleshooting documentation
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Troubleshooting

### Port Already in Use Error

If you get `[Errno 48] address already in use`:

```bash
# Find and kill the process using port 8000
kill -9 $(lsof -ti:8000)

# Then restart the server
uvicorn main:app --reload --port 8000
```

## License

MIT License

## Author

Built for OPAL AI platform integration
