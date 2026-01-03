from fastapi import APIRouter


router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"],
)


@router.get("/")
async def get_catalog():
    pass


@router.get("/search")
async def get_catalog_search():
    pass
