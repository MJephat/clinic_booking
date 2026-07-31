from fastapi import FastAPI

app = FastAPI(
    title="Clinic Booking API",
    version="1.0.0"
)


@app.get("/")
def home():
    return { "message": "Clinic Booking API"}