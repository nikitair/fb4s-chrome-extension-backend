import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index_view():
    return {
        "service": "FB4S Automations",
        "success": True
    }

if __name__ == "__main__":
    # test server launcher
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
