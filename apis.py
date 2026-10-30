from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from database import FETDatabase
from fastapi.responses import FileResponse

app = FastAPI(title="FET (Family Evaluation Tool) API", version="1.0")

# Enable CORS for frontend integration (GitHub Pages / local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = FETDatabase()

# --- ROOT / INDEX SERVING ---

@app.get("/")
def read_index():
    return FileResponse("index.html")

# --- PYDANTIC MODELS FOR REQUEST BODIES ---

class UserCreateRequest(BaseModel):
    user_id: str

class PointAddRequest(BaseModel):
    user_id: str
    points: int
    reason: str

class UserConditionsRequest(BaseModel):
    user_id: Optional[str] = None
    min_balance: Optional[int] = None
    max_balance: Optional[int] = None
    order_by: str = "user_id"
    direction: str = "ASC"

class LedgerConditionsRequest(BaseModel):
    user_id: Optional[str] = None
    min_points: Optional[int] = None
    max_points: Optional[int] = None
    keywords: Optional[List[str]] = None
    order_by: str = "x_id"
    direction: str = "ASC"

# --- TABLE LISTING ENDPOINT ---

@app.get("/api/tables/{table_name}")
def get_table(table_name: str, order_by: str = "user_id", direction: str = "ASC"):
    if table_name not in ("users", "ledger"):
        raise HTTPException(status_code=400, detail="Invalid table name. Use 'users' or 'ledger'.")
    data = db.get_table_data(table_name, order_by=order_by, direction=direction)
    return {"table": table_name, "data": data}

# --- USER & POINT MANAGEMENT ENDPOINTS ---

@app.get("/api/users/check/{user_id}")
def check_user_exists(user_id: str):
    user = db.check_user(user_id)
    exists = user is not None
    return {"user_id": user_id, "exists": exists, "user_data": user}

@app.post("/api/users")
def create_user(req: UserCreateRequest):
    existing = db.check_user(req.user_id)
    if existing:
        raise HTTPException(status_code=400, detail=f"User '{req.user_id}' already exists.")
    db.add_user(req.user_id)
    return {"status": "success", "message": f"User '{req.user_id}' created successfully."}

@app.post("/api/points")
def add_points(req: PointAddRequest):
    existing = db.check_user(req.user_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"User '{req.user_id}' does not exist. Create user first.")
    db.add_points(req.user_id, req.points, req.reason)
    return {"status": "success", "message": f"Successfully added {req.points} points to '{req.user_id}'."}

# --- USERS SEARCH ENDPOINTS ---

@app.get("/api/search/users/id")
def search_users_id(user_id: str, order_by: str = "user_id", direction: str = "ASC"):
    results = db.search_users_by_id(user_id, order_by=order_by, direction=direction)
    return {"results": results}

@app.get("/api/search/users/balance")
def search_users_balance(balance: int, order_by: str = "user_id", direction: str = "ASC"):
    results = db.search_users_by_balance(balance, order_by=order_by, direction=direction)
    return {"results": results}

@app.post("/api/search/users/conditions")
def search_users_conditions(req: UserConditionsRequest):
    results = db.search_users_with_conditions(
        user_id=req.user_id,
        min_balance=req.min_balance,
        max_balance=req.max_balance,
        order_by=req.order_by,
        direction=req.direction
    )
    return {"results": results}

# --- LEDGER SEARCH ENDPOINTS ---

@app.get("/index.html")
def read_index_explicit():
    return FileResponse("index.html")

@app.get("/api/search/ledger/id")
def search_ledger_id(user_id: str, order_by: str = "x_id", direction: str = "ASC"):
    results = db.search_ledger_by_user_id(user_id, order_by=order_by, direction=direction)
    return {"results": results}

@app.get("/api/search/ledger/point")
def search_ledger_point(point: int, order_by: str = "x_id", direction: str = "ASC"):
    results = db.search_ledger_by_point(point, order_by=order_by, direction=direction)
    return {"results": results}

@app.post("/api/search/ledger/keywords")
def search_ledger_keywords(keywords: List[str], order_by: str = "x_id", direction: str = "ASC"):
    results = db.search_ledger_by_keywords(keywords, order_by=order_by, direction=direction)
    return {"results": results}

@app.post("/api/search/ledger/conditions")
def search_ledger_conditions(req: LedgerConditionsRequest):
    results = db.search_ledger_with_conditions(
        user_id=req.user_id,
        min_points=req.min_points,
        max_points=req.max_points,
        keywords=req.keywords,
        order_by=req.order_by,
        direction=req.direction
    )
    return {"results": results}