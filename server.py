import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "API funcionando correctamente en Railway"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """ Permite subir un archivo y genera una URL para acceder a él """
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_url": f"https://web-production-82ea.up.railway.app/files/{file.filename}"}

@app.get("/files/{filename}")
async def get_file(filename: str):
    """ Descarga el archivo almacenado """
    file_path = f"{UPLOAD_DIR}/{filename}"
    
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    return FileResponse(file_path, media_type="text/csv", filename=filename)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Usa el puerto que asigna Railway
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")
