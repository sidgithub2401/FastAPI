from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, List, Dict
import json 

def load_data():
    with open(r"D:\Fast API\Project\patients.json",'r') as f:
        data = json.load(f)
    return data 

def save_data(data):
    with open(r"D:\Fast API\Project\patients.json",'w') as f:
        json.dump(data,f)

class Patient(BaseModel):
    id : Annotated[str, Field(...,description="The unique identifier for the patient",example="P001")]
    name : Annotated[str, Field(...,max_length=100, description="Name of the patient", example="John Doe")]
    city : Annotated[str, Field(..., max_length=100, description="City of residence", example="New York")]
    age : Annotated[int, Field(..., gt=0, lt=120,description="Age of the patient", example=30)]
    gender : Annotated[str, Field(..., description="Gender of the patient", example="male")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in cm", example=180)]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg", example=75)]

    @computed_field
    @property
    def bmi(self)-> float:
        bmi = self.weight / ((self.height / 100) **2)
        return bmi 

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

app= FastAPI()

@app.get("/")
def get_all_patients_details():
    data = load_data()
    return JSONResponse(status_code = 200 , content=data)

@app.get("/patients/{patient_id}")
def get_patient_by_id(patient_id:str):
    data = load_data()
    if patient_id in data:
        result = data[patient_id]
        return JSONResponse(content=result, status_code=200)
    else:
        return JSONResponse(content={"message":"Patient ID not found"}, status_code=404)
    
@app.get("/sort")
def get_sorted_patient_data(sort_by:str=Query(...,description="The attribute to sort patients by",example="age"),
                            order:str=Query("asc",description="Sort order: 'asc' for ascending, 'desc' for descending",example="asc")):
    valid_sort_attributes = ["bmi","weight", "height"]
    valid_order_attributes= ["asc","desc"]

    if sort_by not in valid_sort_attributes:
        return JSONResponse(content={"message":f"Invalid sort attribute. Must be one of: {', '.join(valid_sort_attributes)}"}, status_code=400)
    
    if order not in valid_order_attributes:
        return JSONResponse(content={"message":"Invalid order value. Must be 'asc' or 'desc'"}, status_code=400)
    
    data = load_data()

    sorted_order = True if order =='desc' else False
    sorted_data = sorted(data.values(), key= lambda x: x[sort_by], reverse=sorted_order)

    return JSONResponse(content=sorted_data, status_code=200)

@app.post("/create_patient")
def create_patient(patient:Patient):   #Everything which the user will be entering on the request body will be stored inside this 'patient' variable
    data = load_data()
    if patient.id in data:
        return JSONResponse(content={"message":"Patient ID already exists."}, status_code=400)
    else:
        data[patient.id]= patient.model_dump(exclude=['id'])
        save_data(data)
        return JSONResponse(content={"message":"Patient record created successfully."}, status_code=201)
    
@app.put("/update_patient")
def update_patient_by_id(patient:Patient):
    data = load_data()

    if patient.id in data:
        data[patient.id] = patient.model_dump(exclude=['id']) #This will remove the id from the patient data while updating
        save_data(data)
        return JSONResponse(content={"message":"Patient record updated successfully."}, status_code=200)
    else:
        return JSONResponse(content={"message":"Patient ID not found"}, status_code=404)

