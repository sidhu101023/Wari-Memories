from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
import uuid

from search_memories import find_memories


app = FastAPI(title="Wari Memories API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------
# Folders
# -----------------------------

PHOTO_FOLDER = "../photos"
UPLOAD_FOLDER = "../uploads"

os.makedirs(PHOTO_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# Serve Wari photos
# -----------------------------

app.mount(
    "/photos",
    StaticFiles(directory=PHOTO_FOLDER),
    name="photos"
)


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "Welcome to Wari Memories",
        "status": "Backend is running"
    }


# -----------------------------
# Photographer Upload
# -----------------------------

@app.post("/upload-photo")
async def upload_photo(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    filepath = os.path.join(
        PHOTO_FOLDER,
        filename
    )

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "Photo uploaded successfully",
        "filename": filename,
        "photo_url": f"/photos/{filename}"
    }


# -----------------------------
# Find Wari Memories
# -----------------------------

@app.post("/find-memories")
async def find_my_memories(
    file: UploadFile = File(...)
):

    extension = os.path.splitext(file.filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    # Save selfie
    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    print("\n🔍 Searching Wari memories...")

    try:

        # Search the face database
        results = find_memories(filepath)

        # Add URL for every matching photo
        for result in results:

            result["photo_url"] = (
                f"/photos/{result['filename']}"
            )

        return {

            "message": "Memories found",

            "count": len(results),

            "memories": results

        }

    except Exception as e:

        return {

            "message": "Could not process selfie",

            "error": str(e)

        }