# FastAPI Project

## Setup

1. Create a virtual environment:
   ```sh
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the application

Run the development server:

```sh
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
You can view the interactive documentation at `http://127.0.0.1:8000/docs`.
