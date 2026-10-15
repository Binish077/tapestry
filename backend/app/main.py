from fastapi import FastAPI

from app.api.tree import router as tree_router

app = FastAPI(title="Tapestry API")
app.include_router(tree_router, prefix="/api", tags=["tree"])