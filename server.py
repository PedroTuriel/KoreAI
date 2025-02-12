from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import pandas as pd
import os

app = FastAPI()

# Directorio temporal en Railway para guardar los archivos
UPLOAD_FOLDER = "/tmp"

@app.post("/generate_excel")
async def generate_excel(request: Request):
    data = await request.json()
    incidents = data.get("incidents", [])

    if not incidents:
        return {"error": "No incidents received"}

    # Convert incidents to DataFrame
    file_path = os.path.join(UPLOAD_FOLDER, "incident_report.xlsx")
    df = pd.DataFrame(incidents)
    df.to_excel(file_path, index=False)

    # Obtener la URL real de Railway en tiempo de ejecución
    server_url = request.base_url._url.rstrip("/")

    # Generar enlace de descarga dinámico
    download_link = f"{server_url}/download/incident_report.xlsx"

    return {"file_url": download_link}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    return {"error": "File not found"}
