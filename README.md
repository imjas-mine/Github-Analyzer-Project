# GitHub Analyzer API

A FastAPI backend that connects to GitHub's GraphQL API to fetch and analyze user profiles and repositories using AI.
Website is available at : https://www.gitanalyzer.me/

## Features

- Fetch GitHub user profiles
- Get repository details
- Analyze user contributions in open-source or group projects
- Detect frameworks and technologies used in projects
- AI-powered project description generation
- 3d vizualization of git commit history



## Setup

### 1. Create a virtual environment

```sh
python -m venv venv
```

### 2. Activate the virtual environment

- **Windows:** `.\venv\Scripts\activate`
- **Linux/Mac:** `source venv/bin/activate`

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Set up GitHub Token

You need a GitHub Personal Access Token to use the API.

1. Go to https://github.com/settings/tokens
2. Generate a new token (classic) with `repo` and `read:user` scopes
3. Set it as an environment variable:

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN = "your_token_here"
```

**Linux/Mac:**
```bash
export GITHUB_TOKEN="your_token_here"
```

## Running the Application

Start the development server:

```sh
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`


## Technologies Used

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **GitHub GraphQL API** - Data source


