from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import List, Dict, Annotated
import json

def load_data():
    with open(r"D:\Fast API\Project\patients.json","r") as f:
        data = json.load(f)
    return data 

def save_data(data):
    with open(r"D:\Fast API\Project\patients.json","w") as f:
        json.dump(data,f)

class Patient(BaseModel):
    id : Annotated [str,Field(..., description="Enter the Id of the Patient to be admitted")]
    name : Annotated[str, Field(...,description="Enter the name of the patient", examples=["Siddhant"])]
    age : Annotated[int,Field(...,description="Enter the Age of the Patient")]
    gender: Annotated[str,Field(...,description="Enter the gender Male or Female")]
    height: Annotated[float,Field(..., description="Enter the height of the Patient")]
    weight: Annotated[float,Field(..., description="Enter the weight of the Patient")]
    email : Annotated[str, Field(...,description="Enter the mail of the Patient working In HDFC or ICICI Bank")]

    @computed_field
    @property
    def bmi(self)-> float:
        bmi = self.weight / (self.height*2/100)
        return bmi 
    
    @computed_field
    @property
    def verdict(self)-> str:
        bmi_value = self.bmi
        if bmi_value <= 10:
            return "Underweight"
        elif bmi_value <=20:
            return "Normal"
        elif bmi_value <=30:
            return "OverWeight"
        else:
            return "Obese"

    @field_validator("email")
    @classmethod
    def email_validator(cls,values):
        accepted_domains=["hdfcbank.com","icicibank.com"]
        domain = values.split("@")[-1]
        if domain not in accepted_domains:
            raise ValueError(f"Domain should be in one of the following:{','.join(accepted_domains)}")
        else:
            return values
        
    
app = FastAPI()


@app.get("/")
def get_all_patient():
    data = load_data()
    return JSONResponse(content=data,status_code=200)

@app.get("/patients/{patient_id}")
def get_patient_id(patient_id:str = Path(...,description="Enter the Patient Id")):
    data = load_data()
    if patient_id not in data:
        return JSONResponse(content="Patient Id not Found in the database" , status_code=404)
    else:
        patient_data = data[patient_id]
        return JSONResponse(content=patient_data, status_code=200)

@app.get('/sort') 
def get_sorted_patient_data(sort_by:str=Query(...,description="Enter the on what basis do you want the sorted data",example="Height,Weight,BMI"),
                            order:str=Query("asc",description="In what order do you want to the sorted List in Asc or Desc")):
    accepted_sorted_group = ['height','weight','bmi']
    accepted_order_group = ['asc','desc']

    if sort_by not in accepted_sorted_group:
        raise HTTPException(f"The value entered should be of the following group:{', ',(accepted_sorted_group)}")
    
    if order not in accepted_order_group:
        raise HTTPException(f"The value entered should be of the following group:{', ',(accepted_order_group)}")
    
    data = load_data()

    sorted_order = True if order =='desc' else False
    sorted_data = sorted(data.values(), key = lambda x:x[sort_by], reverse=sorted_order)
    return JSONResponse (content=sorted_data, status_code=200)

@app.post("/create_patients")
def create_new_patient(patient:Patient):
    data = load_data()
    if patient.id in data:
        return JSONResponse(content="Cannot Create Patient as it already exists", status_code=400)
    else:
        data[patient.id] = patient.model_dump(exclude='id')
        save_data(data)
        return JSONResponse(content="Patient Created Succesfully", status_code=200)
    
@app.put("/update_patient")
def update_patient_by_id(patient:Patient):
    data = load_data()
    if patient.id in data:
        data[patient.id] = patient.model_dump(exclude='id')
        save_data(data)
        return JSONResponse(content="Patient Data updated succesfully", status_code=201)
    else:
        return JSONResponse(content="Patient Id not found in Database", status_code=404)
    
@app.delete("/delete_patient")
def delete_patient_by_id(patient_id):
    data = load_data()
    if patient_id in data:
        del data[patient_id]
        save_data(data)
        return JSONResponse(content="Patient Id deleted Succesfully", status_code=200)
    else:
        return JSONResponse(content="Patient Id not found in Database", status_code= 404)
    


