from fastapi import FastAPI, BackgroundTasks
from app.detector import sniff_pmf, results

app = FastAPI()

# Baca interface yang dipilih dari file
with open("interface.txt", "r") as f:
    SELECTED_INTERFACE = f.read().strip()

@app.get("/")
def root():
    return {"message": "PMF Detector API is running", "interface": SELECTED_INTERFACE}

@app.get("/scan")
def scan(background_tasks: BackgroundTasks):
    background_tasks.add_task(sniff_pmf, SELECTED_INTERFACE)
    return {"status": f"Scanning started on {SELECTED_INTERFACE}"}

@app.get("/results")
def get_results():
    return {"pmf_results": results}
