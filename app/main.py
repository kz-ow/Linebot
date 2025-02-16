# app/main.py
from fastapi import FastAPI

app = FastAPI()

if __name__ == '__main__':
    import unicorn
    unicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)