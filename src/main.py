import os

import uvicorn
from fastapi import Request
from fastapi.responses import FileResponse
# from config.app import templates
from fastapi.templating import Jinja2Templates

from config import ROOT_DIR
from config.app import app

# from config.loguru_logger import logger
# from config.logging_confe3ig import logger


@app.get('/', tags=['root'])
async def root_index():
    return {
        "success": True,
        "service": "fb4s-automations",
        "router": "root"
    }


@app.get('/.env', tags=['root'], include_in_schema=False)
async def feel_free(request: Request):
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    templates = Jinja2Templates(directory=template_dir)
    return templates.TemplateResponse("feel_free.html", {"request": request}, status_code=402)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(ROOT_DIR, "src", "static", "favicon.ico")
    return FileResponse(favicon_path)


if __name__ == "__main__":
    # module : app
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    uvicorn.run("main:app", host="0.0.0.0", port=5003, reload=False)

#ghjk hjkl

