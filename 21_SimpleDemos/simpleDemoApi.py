from dbConnection import get_session
from fastapi import FastAPI, Depends
from pydantic import BaseModel

async def get_db_session():
    # this wraps getting the session in a way that works with the Depends injection
    yield get_session()

prepared_employee_insert = None
def get_prepared_employee_insert(session):
    global prepared_employee_insert
    if prepared_employee_insert is None:
        prepared_employee_insert = session.prepare("INSERT INTO emp (empid, first_name, last_name) VALUES (?, ?, ?)")

    return prepared_employee_insert

prepared_employee_select = None
def get_prepared_employee_select(session):
    global prepared_employee_select
    if prepared_employee_select is None:
        prepared_employee_select = session.prepare("SELECT empid, first_name, last_name FROM emp WHERE empid = ?")

    return prepared_employee_select

class Employee(BaseModel):
    empid: int
    first_name: str
    last_name: str

### API code proper
app = FastAPI()

@app.get('/cluster_info')
async def get_info(session=Depends(get_db_session)):
    return [
        {
            'name': cluster.cluster_name,
            'version': cluster.release_version,
        }
        for cluster in session.execute("SELECT cluster_name, release_version FROM system.local")
    ]

@app.post('/employee/create')
async def post_employee(params: Employee, session=Depends(get_db_session)):
    prepared = get_prepared_employee_insert(session)
    id = params.empid
    first = params.first_name
    last = params.last_name

    session.execute(prepared, (id, first, last))

    return [
        {
            'empid': id,
        }
    ]

@app.get('/employee/{id}')
async def get_employee(id: int, session=Depends(get_db_session)):
    prepared = get_prepared_employee_select(session)

    return [
        {
            'empid': employee.empid,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
        }
        for employee in session.execute(prepared, (int(id),))
    ]

@app.get('/employees/{limit}')
async def get_employees(limit: int, session=Depends(get_db_session)):

    strCQL = "SELECT empid, first_name, last_name FROM emp LIMIT " + str(limit)
    return [
        {
            'empid': employee.empid,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
        }
        for employee in session.execute(strCQL)
    ]
