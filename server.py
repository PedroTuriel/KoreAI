from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import pandas as pd
import os
import logging

app = FastAPI()
UPLOAD_FOLDER = "/tmp"

logging.basicConfig(level=logging.INFO)

@app.post("/generate_excel")
async def generate_excel(request: Request):
    try:
        data = await request.json()
        logging.info(f"Received data: {len(data.get('incidents', []))} incidents")  

        incidents = data.get("incidents", [])
        if not incidents:
            return {"error": "No incidents received"}

        file_path = os.path.join(UPLOAD_FOLDER, "incident_report.xlsx")

        # Guardar en chunks para evitar consumo excesivo de memoria
        chunk_size = 500  # Procesar de 500 en 500 registros
        for i in range(0, len(incidents), chunk_size):
            df = pd.DataFrame(incidents[i:i+chunk_size])
            df.to_excel(file_path, index=False, mode='a', header=not os.path.exists(file_path))

        # Generar enlace de descarga
        download_link = f"https://koreai-production.up.railway.app/download/incident_report.xlsx"

        return {"file_url": download_link}

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return {"error": "Internal Server Error", "details": str(e)}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename, media_type="application/vnd.ms-excel")
    return {"error": "File not found"}
