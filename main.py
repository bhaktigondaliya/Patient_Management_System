import json

from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str,Field(...,description='ID of the patient', examples=['P001'])]
    name: Annotated[str,Field(...,description='Name of the patient')]
    city: Annotated[str,Field(...,description='City of the patient')]
    age: Annotated[int,Field(...,gt = 0, lt = 120, description='Age of the patient')]
    gender: Annotated[Literal['male','female','others'],Field(...,description='Gender of the patient')]
    height: Annotated[float,Field(...,description='Height of the patient in mtrs')]
    weight: Annotated[float,Field(...,description='Weight of the patient in kgs')]


    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)
    return data


def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {'msg' : 'Patient Management System API'}


@app.get("/about")
def about():
    return{'msg' : 'A fully functional API to manage patient records'}

@app.get('/view')
def view():
    data =load_data()

    return data

@app.get("/patient/{patient_ids}")
def view_patient(patient_ids : str =Path(..., description = 'ID of patient in the DB', example= 'POO1') ):
    data = load_data()
    ids = patient_ids.split(',')
    result = {}
    for patient_id in ids:
        if patient_id in data:
            result[patient_id] = data[patient_id]
        else:
            raise HTTPException(status_code=404, detail='Patient not found')

    return result

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description = 'Sort on the basis of height, weight or bmi'),order: str = Query('asc', description = 'Sort on asc or desc order')):

    valid_fields = ['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='Sort by must be one of {}'.format(valid_fields))

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Select between asc or desc {}'.format(valid_fields))

    data = load_data()

    sort_order = True if order =='desc' else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = sort_order)
    return sorted_data

@app.post('/create')
def create_patient(patient : Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')


    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)
    return JSONResponse(status_code=201, content={'msg':'patient created successfully'})

