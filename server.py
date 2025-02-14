import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
import shutil

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "API para subir archivos y generar incidentes en ServiceNow"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """ Permite subir un archivo y genera una URL para acceder a él """
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_url": f"https://web-production-82ea.up.railway.app/files/{file.filename}"}

@app.get("/files/{filename}")
async def get_file(filename: str):
    """ Genera la URL del archivo almacenado """
    return {"download_url": f"https://web-production-82ea.up.railway.app/files/{filename}"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Usa el puerto dinámico de Railway
    uvicorn.run(app, host="0.0.0.0", port=port)
