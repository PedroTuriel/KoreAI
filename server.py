from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import os

app = FastAPI()

# Directorio seguro en Railway para guardar archivos temporalmente
UPLOAD_FOLDER = "/tmp"

@app.post("/generate_excel")
async def generate_excel(request: Request):
    try:
        data = await request.json()
        incidents = data.get("body", {}).get("result", [])

        if not incidents:
            return JSONResponse(status_code=400, content={"error": "No incidents received"})

        # Convert incidents to DataFrame
        df = pd.DataFrame(incidents)

        # Ruta del archivo
        file_path = os.path.join(UPLOAD_FOLDER, "incident_report.xlsx")

        # Guardar en formato Excel
        df.to_excel(file_path, index=False, engine='openpyxl')

        # Generar enlace de descarga desde Railway
        download_link = f"https://koreai-production.up.railway.app/download/incident_report.xlsx"

        return JSONResponse(status_code=200, content={"file_url": download_link})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "details": str(e)})

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename, media_type="application/vnd.ms-excel")
    return JSONResponse(status_code=404, content={"error": "File not found"})
