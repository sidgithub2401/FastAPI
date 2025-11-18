from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

def load_data():
    with open(r"D:\Fast API\Project\patients.json","r") as f:
        data = json.load(f)
    return data


@app.get("/")
def hello():
    return {"message":"Patient Management System"}

@app.get("/view")
def view_patients():
    result = load_data()
    return result

@app.get("/patient/{patient_id}")
## By using Path Parameter we can add extra information about the path parameters like description,example etc.
def view_patient_id(patient_id: str = Path(...,description="The ID of the patient to retrieve",example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient ID not found")
    

@app.get("/sort")
def sort_patients(sort_by:str = Query(...,description="The attribute to sort patients by",example="age"),
                  order:str=Query("asc",description="Sort order: 'asc' for ascending, 'desc' for descending",example="asc")):
    
    valid_sort_attributes = ["age", "name", "city", "bmi", "weight", "height"]

    if sort_by not in valid_sort_attributes:
        raise HTTPException(status_code=400, detail=f"Invalid sort attribute. Must be one of: {', '.join(valid_sort_attributes)}")
    
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400, detail='invlaid order value.Must be asc or desc')
    
    data = load_data()

    sort_order = True if order =='desc' else False

    sorted_data = sorted(data.values(), key = lambda x: x[sort_by] , reverse = sort_order)

    return sorted_data
    
