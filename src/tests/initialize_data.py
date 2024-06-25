from sqlmodel import Session
from src.models import ProjectStatusCode


def init_status_code(db: Session):
    print("init_status_code")
    status_code = ProjectStatusCode(status="In Progress")
    db.add(status_code)
    db.commit()
    db.refresh(status_code)
    status_code = ProjectStatusCode(status="Done")
    db.add(status_code)
    db.commit()
    db.refresh(status_code)
    status_code = ProjectStatusCode(status="Canceled")
    db.add(status_code)
    db.commit()
    db.refresh(status_code)
    return status_code
    