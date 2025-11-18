from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Optional, List, Dict, Annotated
import json

app= FastAPI()

def load_data():
    with open(r"D:\Fast API\Project\patients.json","r") as f:
        data = json.load(f)
    return data 

def save_data(data):
    with open(r"D:\Fast API\Project\patients.json","w") as f:
        json.dump(data,f)

class Patient(BaseModel):
    id : Annotated[str, Field(...,description="Patient ID in format PXXX", example="P001")]
    name : Annotated[str, Field(...,max_length=100, description="Name of the patient", example="John Doe")]
    city : Annotated[str, Field(..., max_length=100, description="City of residence", example="New York")]
    age : Annotated[int, Field(..., gt=0, lt=120,description="Age of the patient", example=30)]
    gender : Annotated[str, Field(..., description="Gender of the patient", example="male")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in cm", example=180)]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg", example=75)]

    @computed_field
    @property
    def bmi(self) -> float:
        height_in_meters = self.height / 100
        bmi_value = self.weight / (height_in_meters ** 2)
        return bmi_value
    
    @computed_field
    @property
    def verdict(self) -> str:
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            return "Normal"
        elif 25 <= bmi_value < 29.9:
            return "Overweight"
        else:
            return "Obese"


@app.post("/create_patient")
def create_patient(patient: Patient):
    # load the data
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists.")
    else:
        #add the new patient record into the dictionary 
        data[patient.id] = patient.model_dump(exclude=['id'])
        #save the data inside the json file 
        save_data(data)

        return JSONResponse(content={"message": "Patient record created successfully."}, status_code=201)

@app.get("/patient/{patient_id}")
def get_patient_id(patient_id:str):
    data = load_data()

    if patient_id in data:
        return JSONResponse(content = data[patient_id], status_code=200)
    else:
        return JSONResponse(content={"message":"Patient ID not found"}, status_code=404)
    
@app.get("/")
def get_all_patient():
    data = load_data()
    return JSONResponse(content=data, status_code=200)

@app.get("/sort")
def sorted_patients(sort_by:str = Query(...,description="The attribute to sort patients by",example="age"),
                  order:str=Query("asc",description="Sort order: 'asc' for ascending, 'desc' for descending",example="asc")):
    
    valid_sort_attributes=["bmi","weight","height"]

    valid_order_attributes=["asc","desc"]

    if sort_by not in valid_sort_attributes:
        raise HTTPException(status_code=400, detail=f"Invalid sort attribute. Must be one of: {', '.join(valid_sort_attributes)}")
    
    if order not in valid_order_attributes:
        raise HTTPException(status_code=400, detail='invlaid order value.Must be asc or desc')
    
    data = load_data()

    sorted_order = True if order =='desc' else False
    sorted_data = sorted(data.values(), key = lambda x : x[sort_by], reverse=sorted_order)
    return JSONResponse(content=sorted_data, status_code=200)


