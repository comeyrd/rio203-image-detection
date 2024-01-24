""" tiny backend for image detection"""
from typing import Annotated
import base64
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import subprocess
import requests
import re
app = FastAPI()
central_server = "https://parking-rio.rezel.net/"

def sendplaque(plaque,direction):
    central_server_url = central_server + "api/carDetected"  # Replace "endpoint" with the actual endpoint on the central server
    try:
        obj = {"plaque": plaque,"direction": direction}
        ans = requests.post(central_server_url, json=obj)
        ans.raise_for_status()
        return ans.json()
    except requests.exceptions.RequestException as err:
        return {"error":f"Server error : ${str(err)}"}


def most_p_plaque(output):
    if output:
        match = re.search(r'\b([A-Z0-9]+)\s+confidence:', output)
        if match:
            plate_number = match.group(1)
            return plate_number
        else :
            return "error"
    else : 
        return "error"

app.mount("/static", StaticFiles(directory="templates"), name="static")

IMG_NAME = "plaque.png"
COMMAND = f"bash -c 'source ~/.bashrc && alpr -c eu {IMG_NAME}'"

@app.post("/detection")
def image_detection(image: Annotated[str, Form()],direction: Annotated[str, Form()]):
    """do detection"""
    contents = image
    img = base64.b64decode(contents)
    with open(IMG_NAME, "wb") as fh:
        fh.write(img)
    result = subprocess.run(COMMAND, shell=True, check=True, text=True, capture_output=True)
    plaque = most_p_plaque(result.stdout)
    if plaque == "error":
        return {"message":"No License Plate Found"}
    else:
        json = sendplaque(plaque,direction)
        return {"message": plaque, "direction":direction,"srv":json}


@app.get("/", response_class=HTMLResponse)
async def render_index():
    """render index"""
    return FileResponse("templates/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    