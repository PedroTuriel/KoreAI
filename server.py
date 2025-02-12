from fastapi import FastAPI, Request
import pandas as pd
import os

app = FastAPI()

# Carpeta donde se guardarán los archivos
UPLOAD_FOLDER = "files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/generate_excel")
async def generate_excel(request: Request):
    data = await request.json()
    incidents = data.get("incidents", [])

    if not incidents:
        return {"error": "No incidents received"}

    # Convert incidents to DataFrame
    df = pd.DataFrame(incidents)
    file_path = os.path.join(UPLOAD_FOLDER, "incident_report.xlsx")
    df.to_excel(file_path, index=False)

    # Generar enlace de descarga desde Railway
    download_link = f"https://your-railway-app.up.railway.app/download/incident_report.xlsx"

    return {"file_url": download_link}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return {"message": "File available", "download_url": f"https://your-railway-app.up.railway.app/files/{filename}"}
    return {"error": "File not found"}
