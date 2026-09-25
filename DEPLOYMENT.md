# Chatbot Deployment Guide

This guide deploys `chatbot.py` as a Streamlit application on Render, Streamlit Community Cloud, or DigitalOcean.

## Before deploying

1. Rotate the current `GROQ_API_KEY` if it has ever been committed, uploaded, or shared. API keys must be treated as exposed once they leave your local machine.
2. Do not commit `.env`, API keys, `.venv`, or local databases.
3. Push the project to a GitHub repository. The repository should contain at least:

```text
chatbot.py
requirements.txt
```

The application reads this environment variable:

```text
GROQ_API_KEY
```

## Test locally

From the project directory:

```powershell
& .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run chatbot.py
```

Create `.env` locally only:

```text
GROQ_API_KEY=your_groq_api_key
```

## Deploy on Render

1. Open [Render](https://render.com/) and select **New > Web Service**.
2. Connect the GitHub repository and choose the branch to deploy.
3. Use these settings:

```text
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: streamlit run chatbot.py --server.address 0.0.0.0 --server.port $PORT
```

4. In **Environment > Environment Variables**, add:

```text
Key: GROQ_API_KEY
Value: your_groq_api_key
```

5. Choose a plan and select **Create Web Service**.
6. Open the public Render URL after the first deploy finishes.

Render supplies the `$PORT` value. The start command must use that value and bind Streamlit to `0.0.0.0`.

## Deploy on Streamlit Community Cloud

1. Push `chatbot.py` and `requirements.txt` to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and select **Create app**.
3. Select the repository, branch, and set **Main file path** to:

```text
chatbot.py
```

4. Before launching, open the app settings **Secrets** section and add:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

5. Click **Deploy**.

Streamlit Community Cloud injects the secret as an environment variable, so `load_dotenv()` does not need a `.env` file in the deployed repository.

## Deploy on DigitalOcean App Platform

1. Open [DigitalOcean](https://cloud.digitalocean.com/) and select **Create > Apps**.
2. Connect the GitHub repository and select the branch.
3. Configure the service as a Python web service:

```text
Build Command: pip install -r requirements.txt
Run Command: streamlit run chatbot.py --server.address 0.0.0.0 --server.port $PORT
HTTP Port: 8080
```

4. In **Environment Variables**, add `GROQ_API_KEY` as a **secret**.
5. Select **Deploy** and wait for the build to complete.
6. Use the generated DigitalOcean app URL to open the chatbot.

DigitalOcean App Platform commonly exposes port `8080`; using `$PORT` in the run command lets the platform provide the actual port when needed.

## Optional DigitalOcean Droplet deployment

For a Droplet, install Python and Git, clone the repository, and run:

```bash
sudo apt update
sudo apt install -y python3-venv git
cd SidharthGenAI
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="your_groq_api_key"
streamlit run chatbot.py --server.address 0.0.0.0 --server.port 8501
```

For a production Droplet, run Streamlit behind a reverse proxy such as Nginx and a process manager such as systemd. Do not leave the API key in shell history or commit it to the repository.

## Troubleshooting

- **Missing `GROQ_API_KEY`:** confirm the variable is configured in the provider's secrets/environment settings, then redeploy.
- **Application fails to start on Render or DigitalOcean:** confirm the start command uses `--server.address 0.0.0.0` and `--server.port $PORT`.
- **Dependency installation is slow or fails:** `requirements.txt` contains packages for other RAG examples as well as this chatbot. A smaller production requirements file containing `streamlit`, `python-dotenv`, `langchain-community`, and `langchain-groq` can reduce build time if only `chatbot.py` is deployed.
- **Changes are not visible:** push the latest commit to the branch selected by the hosting provider and check the deployment logs.
