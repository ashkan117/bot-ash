# Prereqs

This project uses poetry, FastAPI, and ngrok
To download all the dependencies make sure that you [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) installed. 

```bash
# download dependencies
poetry shell
poetry install

# start the server
uvicorn bot-ash.main:app --reload --port 8000 --host 0.0.0.0

# start ngrok
ngrok http http://localhost:8000
```

Finally with all the plumbing in place you need to make sure you provide the
`WHIPPY_API_KEY` and `OPENAI_API_KEY`
