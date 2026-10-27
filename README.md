# Chatbot Simple

A Streamlit chatbot that uses a Groq-hosted language model. The app reads `GROQ_API_KEY` from a local `.env` file, an environment variable, or Streamlit secrets.

## Requirements

- Python 3.10 or later
- A [Groq API key](https://console.groq.com/keys)

## Run locally (Windows PowerShell)

From the project directory, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a local `.env` file from the sample:

```powershell
Copy-Item .env.sample .env
```

Edit `.env` and replace the placeholder with your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key
```

Start the app:

```powershell
streamlit run chatbot.py
```

Streamlit prints a local URL (usually `http://localhost:8501`) where you can open the chatbot.

## Deploy

See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment instructions for Render, Streamlit Community Cloud, and DigitalOcean.

## Keep secrets safe

Do not commit `.env`, API keys, or the `.venv` directory. They are excluded by `.gitignore`. If an API key was exposed, revoke it and create a replacement.
