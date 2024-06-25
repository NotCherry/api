from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.models import Project, User
from src.crud import create_user_project, get_current_user, get_projects_by_org, get_org_by_user, get_projects_by_user
from src.models import Project
from src.util import get_db


router = APIRouter()

@router.post("/projects")
def db_create_user_project(project: Project, db: Session = Depends(get_db)):
    return create_user_project(db, project)
@router.get("/projects")
def projects(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_projects_by_user(db, user.id)

@router.post("/org/projects")
def db_create_org_project(project: Project, db: Session = Depends(get_db)):
    return create_user_project(db, project)


@router.get("/org/projects/{org_id}")
def project_by_org(org_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_org_id = get_org_by_user(db, user.id).organization_id
    if user_org_id != org_id :
        return "Unauthorized"
    
    return get_projects_by_org(db, org_id)
