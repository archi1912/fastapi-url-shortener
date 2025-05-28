from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import URL, SessionLocal, init_db
import hashlib

init_db()

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "short_url": None})

@app.post("/", response_class=HTMLResponse)
def form_post(request: Request, original: str = Form(...)):
    db = SessionLocal()
    short = hashlib.md5(original.encode()).hexdigest()[:6]
    existing = db.query(URL).filter(URL.original == original).first()
    if not existing:
        new_url = URL(short=short, original=original)
        db.add(new_url)
        db.commit()
    db.close()
    return templates.TemplateResponse("index.html", {
        "request": request, "short_url": f"/{short}"
    })

@app.get("/{short}")
def redirect_to_original(short: str):
    db = SessionLocal()
    url = db.query(URL).filter(URL.short == short).first()
    db.close()
    if url:
        return RedirectResponse(url.original)
    return HTMLResponse("<h1>URL not found</h1>", status_code=404)
