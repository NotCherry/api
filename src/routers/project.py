from fastapi import APIRouter


router = APIRouter()

@router.get("/projects/{org}")
def project_by_org(org: str):
    print("org")
    return get_projects_by_org(org)
