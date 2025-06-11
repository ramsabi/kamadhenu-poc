from fastapi import FastAPI, Request
import uvicorn
import os
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/on_search")
async def on_search(request: Request):
    body = await request.json()
    print("Received on_search callback:")
    print(body)
    return {"message": "Kamadhenu received the rice list 🐄🍚"}

@app.get("/ondc-site-verification.html")
async def serve_verification():
    return FileResponse("ondc-site-verification.html", media_type="text/plain")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("kamadhenu_on_search:app", host="0.0.0.0", port=port)