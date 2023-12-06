from sqlmodel import SQLModel, Session, create_engine
from models.events import Event

filename = "planner.db"
dialect = "sqlite"
db_conn_url = f"{dialect}:///{filename}"
c_args = {"check_same_thread": False}

engine = create_engine(db_conn_url, echo=True, connect_args=c_args)

# Database Table Creation
def conn():
    SQLModel.metadata.create_all(engine)

# Database Session Creation
def get_session():
    with Session(engine) as session:
        yield session  # For Dependency Injection into CRUD Functions
