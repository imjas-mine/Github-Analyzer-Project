---
description: Implementation plan for AI-powered repository analysis with OpenAI
---

# 🎯 Repository Analysis Feature - Implementation Plan

## Overview
Analyze a GitHub repository to:
1. Detect frameworks/technologies from file structure & config files
2. Generate a description if the repo doesn't have one
3. Handle empty repos gracefully
4. For multi-contributor repos, isolate and summarize a specific user's contributions

---

## Phase 1: OpenAI Service Setup

### Step 1.1: Create the OpenAI Service
**File:** `app/services/openai_service.py`

**What to do:**
1. Create a new service class `OpenAIService`
2. Import `openai` library and your settings
3. Initialize with the API key from `settings.OPENAI_API_KEY`
4. Create a base method `send_prompt(system_prompt, user_prompt)` that:
   - Calls OpenAI's Chat Completions API
   - Uses `gpt-4o-mini` for cost-efficiency (or `gpt-4o` for better results)
   - Handles errors and rate limits

**Dependencies to install:**
```bash
pip install openai
```

---

## Phase 2: GitHub Service Enhancements

### Step 2.1: Add Missing Service Methods
**File:** `app/services/github_service.py`

**Add these methods:**

#### `get_directory_tree(owner, name, path="HEAD:")`
- Uses: `QueryNames.DIRECTORY_TREE`
- Returns the file/folder structure at a given path
- Needed for deeper project analysis

#### `get_user_contributions(owner, name, author_id)`
- Uses: `QueryNames.USER_CONTRIBUTIONS`  
- Returns user's commits, PRs, and issues
- Notes: `author_id` is the GitHub user's ID (from user profile query)

#### `get_contribution_stats(owner, name, username)`
- Uses: `QueryNames.CONTRIBUTION_STATS`
- Quick check to see if user has contributed to this repo

### Step 2.2: Add Empty Repo Detection
**In `get_repository_details` method:**

Add logic to check if repo is empty by looking at:
- `defaultBranchRef` is `null` → repo is empty
- `rootTree.entries` is empty or `null` → repo is empty

Return an `is_empty` flag in the response.

---

## Phase 3: Repository Analyzer Service (Core Logic)

### Step 3.1: Create the Analyzer Service
**File:** `app/services/repo_analyzer_service.py`

**What to do:**
1. Create class `RepoAnalyzerService` that depends on:
   - `GitHubService` (for fetching data)
   - `OpenAIService` (for AI analysis)

2. Main method: `analyze_repository(owner, name, username)`

### Step 3.2: Implement Analysis Flow

```python
async def analyze_repository(self, owner: str, name: str, username: str):
    # 1. Fetch repository details
    repo_details = await self.github.get_repository_details(owner, name)
    
    # 2. Check if empty
    if self._is_empty_repo(repo_details):
        return {"error": "Repository is empty", "is_empty": True}
    
    # 3. Prepare data for OpenAI
    analysis_context = self._build_analysis_context(repo_details)
    
    # 4. Generate project analysis via OpenAI
    project_analysis = await self._analyze_project(analysis_context)
    
    # 5. Get user's contributions
    user_contributions = await self._get_user_contributions(owner, name, username)
    
    # 6. Generate contribution summary via OpenAI (if user has contributions)
    contribution_summary = None
    if user_contributions and user_contributions.total_commits > 0:
        contribution_summary = await self._summarize_contributions(
            repo_details, user_contributions
        )
    
    # 7. Return combined response
    return {
        "repository": repo_details,
        "project_analysis": project_analysis,
        "user_contributions": user_contributions,
        "contribution_summary": contribution_summary,
    }
```

---

## Phase 4: OpenAI Prompt Engineering

### Step 4.1: Framework Detection Prompt
**Method:** `_analyze_project(context)`

**System Prompt:**
```
You are a software project analyzer. Given repository metadata, config files, 
and file structure, identify:
1. Project type (Web App, API, Library, CLI, Mobile App, etc.)
2. Frameworks and technologies used (with confidence scores)
3. A concise description if one isn't provided
4. Key features based on the structure
5. Complexity score (1-10)

Respond in JSON format matching the provided schema.
```

**User Prompt includes:**
- Languages detected (from GraphQL)
- Repository topics
- Config file contents (package.json, requirements.txt, etc.)
- Root directory structure
- README (if available)
- Existing description (if any - note if missing)

### Step 4.2: Contribution Summary Prompt
**Method:** `_summarize_contributions(repo, contributions)`

**System Prompt:**
```
You are analyzing a developer's contributions to a GitHub repository.
Based on their commits, PRs, and issues, provide:
1. Their relationship to the project (Owner, Core Contributor, Contributor)
2. Primary areas of contribution (Frontend, Backend, Docs, etc.)
3. A 2-3 sentence summary of their work
4. Notable contributions or patterns

Respond in JSON format matching the provided schema.
```

**User Prompt includes:**
- Repository name and description
- User's commits (messages, dates, additions/deletions)
- User's PRs (titles, states, impact)
- User's issues (titles, states)
- Comparison with total repo activity

---

## Phase 5: API Endpoints

### Step 5.1: Create Analysis Endpoint
**File:** `app/api/v1/endpoints.py`

**Add endpoint:** `POST /api/v1/analyze`

**Request body:**
```python
class AnalyzeRequest(BaseModel):
    owner: str
    repo: str
    username: str
```

**Response:** `RepositoryAnalysisResponse` (already defined in schemas.py)

### Step 5.2: Error Handling
- Return 404 if repository not found
- Return appropriate message if repo is empty
- Return 400 if user has no contributions (with empty contribution summary)

---

## Phase 6: Response Transformation

### Step 6.1: Create Data Transformers
**File:** `app/services/transformers.py`

**Purpose:** Transform raw GraphQL responses into Pydantic models

**Methods:**
- `transform_repo_details(raw_data) -> RepositoryDetails`
- `transform_user_contributions(raw_data, username) -> UserContributions`
- `parse_openai_analysis(json_str) -> ProjectAnalysis`
- `parse_openai_summary(json_str) -> ContributionSummary`

---

## File Structure After Implementation

```
app/
├── services/
│   ├── github_service.py      # ✅ Exists - Add new methods
│   ├── openai_service.py      # 🆕 Create
│   ├── repo_analyzer_service.py # 🆕 Create
│   └── transformers.py        # 🆕 Create
├── api/
│   └── v1/
│       └── endpoints.py       # ✅ Exists - Add analyze endpoint
├── models/
│   └── schemas.py             # ✅ Exists - Already has needed models
└── graphql/
    └── queries/               # ✅ Complete - All queries exist
```

---

## Execution Order (Step by Step)

### 🔵 Session 1: OpenAI Setup
1. Install openai package
2. Create `openai_service.py` with basic `send_prompt` method
3. Test with a simple prompt

### 🔵 Session 2: GitHub Service Enhancement
4. Add `get_directory_tree` method
5. Add `get_user_contributions` method  
6. Add `get_contribution_stats` method
7. Add empty repo detection logic

### 🔵 Session 3: Core Analyzer
8. Create `transformers.py` with data transformation logic
9. Create `repo_analyzer_service.py` with main flow
10. Implement `_is_empty_repo` helper
11. Implement `_build_analysis_context` helper

### 🔵 Session 4: AI Integration
12. Create framework detection prompt and method
13. Create contribution summary prompt and method
14. Add JSON parsing for AI responses

### 🔵 Session 5: API & Testing
15. Add `/analyze` endpoint
16. Test full flow with various repos
17. Handle edge cases (empty repos, no contributions, private repos)

---

## Edge Cases to Handle

| Scenario | How to Handle |
|----------|---------------|
| Empty repository | Return `is_empty: true` with message |
| No description | Generate via OpenAI |
| User is sole contributor | Skip contribution percentage |
| User has no contributions | Return empty contribution summary |
| Private repo (no access) | Return 403 with message |
| Rate limited by GitHub | Retry with backoff |
| Rate limited by OpenAI | Retry with backoff |
| Large repo (many files) | Limit directory traversal depth |

---

## Notes

- **Token Usage:** Be mindful of OpenAI token usage. Truncate large config files/READMEs if needed.
- **Caching:** Consider caching OpenAI responses for the same repo (descriptions don't change often).
- **Cost:** `gpt-4o-mini` is ~20x cheaper than `gpt-4o`. Start with mini.
