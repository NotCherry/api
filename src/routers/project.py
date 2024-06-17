

from fastapi import APIRouter


router = APIRouter()

@router.get("/projects/{org}")
def project(org: str):
    print("org")
    return get_projectsby_org(org)