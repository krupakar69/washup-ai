from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from enhance import enhance_image
from colorize import colorize_image
from removebg import remove_background

app = FastAPI()

# Allow React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def root():
    return {"message": "WashUp AI is running!"}

@app.post("/api/enhance")
async def enhance(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = enhance_image(image_bytes)
    return Response(content=result, media_type="image/png")

@app.post("/api/colorize")
async def colorize(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = colorize_image(image_bytes)
    return Response(content=result, media_type="image/png")

@app.post("/api/removebg")
async def removebg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = remove_background(image_bytes)
    return Response(content=result, media_type="image/png")