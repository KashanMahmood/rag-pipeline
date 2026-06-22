from fastapi import FastAPI
from pydantic import BaseModel
from search import search as do_search

class SearchRequest(BaseModel):
    query: str

app = FastAPI()

@app.get("/")
def root():
    return {"status" : "ok"}

@app.post("/search")
def search(request: SearchRequest):
    search_results = do_search(request.query)
    return {"results": search_results}