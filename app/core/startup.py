from app.core.scheduler import start_scheduler, stop_scheduler
from app.core.database import engine, Base

def on_startup():
    Base.metadata.create_all(bind=engine)
    start_scheduler()

def on_shutdown():
    stop_scheduler()
