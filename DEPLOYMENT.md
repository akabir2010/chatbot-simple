# Chatbot Deployment Guide

This guide covers local setup and deployment of `chatbot.py`, a Streamlit app that uses the Groq API.

## Requirements

- Python 3.10 or later
- A Groq API key
- GitHub repository containing `chatbot.py` and `requirements.txt` for cloud deployment

Never commit API keys, `.env` files, or virtual environments. These are excluded by `.gitignore`. If an API key was committed or shared, revoke it and create a replacement.

## Run locally (Windows PowerShell)

From the project directory, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a local `.env` file from the sample and replace the placeholder with your Groq API key:

```powershell
Copy-Item .env.sample .env
```

Then start the app:

```powershell
streamlit run chatbot.py
```

The app loads `GROQ_API_KEY` from `.env` locally. Keep that file on your machine and do not upload it.

## Deploy to Render

1. Push the project to GitHub and create a **Web Service** in Render connected to the repository.
2. Set the service configuration:

   ```text
   Runtime: Python
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run chatbot.py --server.address 0.0.0.0 --server.port $PORT
   ```

3. Add `GROQ_API_KEY` as a secret environment variable in the Render dashboard.
4. Deploy the service and open its public URL when the deployment completes.

Render provides the port through `$PORT`; the start command must use it and bind to `0.0.0.0`.

## Deploy to Streamlit Community Cloud

1. Push the project to GitHub.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), create an app and select the repository, branch, and `chatbot.py` as the main file.
3. In the app's **Settings > Secrets**, add your key:

   ```toml
   GROQ_API_KEY = "your_groq_api_key"
   ```

4. Save the settings and deploy the app.

Do not add the key to the repository. Configure it through the app's Secrets settings.

## Deploy to DigitalOcean App Platform

1. Create an app in [DigitalOcean App Platform](https://cloud.digitalocean.com/apps) and connect the GitHub repository.
2. Configure a Python web service with:

   ```text
   Build Command: pip install -r requirements.txt
   Run Command: streamlit run chatbot.py --server.address 0.0.0.0 --server.port $PORT
   ```

3. Configure the service's HTTP port to match the port used by the app.
4. Add `GROQ_API_KEY` as a secret environment variable.
5. Deploy the app and open its generated URL.

## Optional: deploy to a DigitalOcean Droplet

On the Droplet, install Python and Git, clone the repository, and run:

```bash
sudo apt update
sudo apt install -y python3-venv git
cd <repository-directory>
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Set `GROQ_API_KEY` in the process environment without committing it, then start Streamlit:

```bash
streamlit run chatbot.py --server.address 0.0.0.0 --server.port 8501
```

For production, run Streamlit behind a reverse proxy such as Nginx and use a process manager such as systemd. Avoid putting the API key directly in shell commands, where it may be saved in shell history.

## Troubleshooting

- **Missing API key:** confirm `GROQ_API_KEY` is configured in the hosting provider's secret or environment-variable settings.
- **The app cannot be reached:** on Render or DigitalOcean, bind to `0.0.0.0` and use the port configured for the service.
- **Dependency installation fails:** check the deployment logs and confirm `requirements.txt` is present at the repository root.
- **Changes do not appear:** confirm the latest changes were pushed to the branch connected to the hosting provider, then review the deployment logs.
