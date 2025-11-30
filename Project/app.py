from fastapi import HTTPException
import json
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from pydantic import BaseModel,Field, computed_field
from typing import Annotated,List,Dict, Literal, Optional
import pandas as pd 
import pickle

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

with open("model1.pkl", "rb") as file:
    model = pickle.load(file)

app = FastAPI()

class Userinput(BaseModel):
    age:Annotated[int,Field(...,gt=0,lt=120,description="Enter the age of the user")]
    weight:Annotated[float,Field(...,description="Enter the weight of the patient")]
    height:Annotated[float,Field(...,description="Enter the height of the patient")]
    income:Annotated[float,Field(...,description="Enter the age of the user")]
    smoker:Annotated[bool,Field(...,description="Is the user a smoker or not")]
    city:Annotated[str,Field(...,description="The city which user belongs too")]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job','business_owner', 'unemployed', 'private_job'],Field(...,description="Select from the following Occupations")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def citytier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        else:
            return 2
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "High"
        elif self.smoker or self.bmi > 27:
            return "Medium"
        else:
            return "low"
    
    @computed_field
    @property
    def age_group(self)->int:
        if self.age<=18:
            return "young"
        elif self.age<45:
            return "adult"
        elif self.age<60:
            return "middle_aged"
        else:
            return "senior"


@app.post("/predict")
def predict_result(userinput:Userinput):
    input_df= pd.DataFrame([
        {
        'bmi':userinput.bmi,
        'age_group':userinput.age_group,
        'lifestyle_risk':userinput.lifestyle_risk,
        'city':userinput.citytier,
        'income_lpa':userinput.income,
        'occupation':userinput.occupation
        }
    ])

    predict_result = model.predict(input_df)[0]

    return JSONResponse(status_code=200 , content={'Prediction':predict_result})






        

        



