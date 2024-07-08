import os

import uvicorn
from fastapi import Request, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates
import aiofiles
from config.logging_config import logs_file_path

from config.app import app


@app.get('/', tags=['index'])
def root_index():
    return {
        "service": "fb4s-chrome-extension"
    }


@app.get('/.env', tags=['index'], include_in_schema=False)
def feel_free(request: Request):
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    templates = Jinja2Templates(directory=template_dir)
    return templates.TemplateResponse("feel_free.html", {"request": request}, status_code=402)


@app.get("/logs", include_in_schema=False, response_class=PlainTextResponse)
async def get_logs():
    try:
        async with aiofiles.open(logs_file_path, "r") as logs_file:
            log_lines: list = await logs_file.readlines()
            # log_lines.reverse()
            logs = ''.join(log_lines)
            
        return logs

    except (FileNotFoundError, FileExistsError) as e:
        raise HTTPException(status_code=404, detail={"error": f"Log file NOT found - ({e})"})
    except Exception as ex:
        raise HTTPException(status_code=500, detail={"error": f"Server Error - ({ex})"})



if __name__ == "__main__":
    # module : app
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    uvicorn.run("main:app", host="0.0.0.0", port=5003, reload=False)
    # uvicorn.run("main:app", host="0.0.0.0", port=5007, reload=False)

