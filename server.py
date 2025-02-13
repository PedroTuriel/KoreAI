from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import os

app = FastAPI()

# Directorio seguro en Railway para guardar archivos temporalmente
UPLOAD_FOLDER = "/tmp"

# Mapeo de estados numéricos a nombres
STATE_MAPPING = {
    "1": "New",
    "-5": "Assigned",
    "2": "In Progress",
    "3": "On Hold",
    "6": "Resolved",
    "8": "Canceled",
    "7": "Closed"
}

@app.post("/generate_excel")
async def generate_excel(request: Request):
    try:
        data = await request.json()

        # Determinar si la raíz de la solicitud es directamente una lista
        if isinstance(data, list):  
            incidents = data  # Es una lista, usarla directamente
        else:
            incidents = data.get("incidents", [])  # Si no, buscar dentro de "incidents"

        if not incidents:
            return JSONResponse(status_code=400, content={"error": "No incidents received"})

        # Normalizar los datos
        processed_incidents = []
        for incident in incidents:
            processed_incidents.append({
                "sys_id": incident.get("sysid") or incident.get("sys_id", ""),  # Asegurar sys_id
                "number": incident.get("number", ""),
                "short_description": incident.get("short_description") or incident.get("shortdescription") or incident.get("short description", ""),  # Normaliza descripción
                "state": STATE_MAPPING.get(str(incident.get("state", "")), "Unknown")  # Mapear estados
            })

        # Convertir a DataFrame
        df = pd.DataFrame(processed_incidents)

        # Ruta del archivo
        file_path = os.path.join(UPLOAD_FOLDER, "incident_report.xlsx")

        # Guardar en formato Excel
        df.to_excel(file_path, index=False, engine='openpyxl')

        # Generar enlace de descarga
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
