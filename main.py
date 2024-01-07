""" tiny backend for image detection"""
from typing import Annotated
import base64
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from lib.analyse import analyse

app = FastAPI()


app.mount("/static", StaticFiles(directory="templates"), name="static")


@app.post("/detection")
def image_detection(image: Annotated[str, Form()]):
    """do detection"""
    contents = image
    img = base64.b64decode(contents)
    with open("imageToSave.png", "wb") as fh:
        fh.write(img)
    res = analyse("imageToSave2.png")
    print(res)
    return {"message": res}


@app.get("/", response_class=HTMLResponse)
async def render_index():
    """render index"""
    return FileResponse("templates/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
