from pydantic import BaseModel, Field , computed_field
from typing import List, Dict , Annotated

class Patient(BaseModel):
    name : Annotated[str, Field(...,description="Name of the patient",max_length=100)]
    age : Annotated[int, Field(...,gt=18,description="Age must be greater than 18")]
    contact_details : Annotated[Dict[str,str], Field(...,description="Contact details of the patient")]
    email : Annotated[str,Field(...,description="Email of the patient belonging to HDFC and ICICI bank")]
    weight: Annotated[float, Field(...,gt=20,description="Weight of the patient in kgs")]
    height: Annotated[float, Field(...,gt=0.5,description="Height of the patient in meters")]

# computed fields are used to define fields that are derived from other fields in the model
#The name of the property will be used as the field name in the model like in this case bmi will be the field name
    @computed_field
    @property
    def bmi(self)-> float:
        bmi = self.weight / (self.height ** 2)
        return bmi
    
def print_patient_info(patient:Patient):
    print("Name:", patient.name)
    print("Age:", patient.age)
    print("Contact Details:", patient.contact_details)
    print("Email:", patient.email)
    print("Weight:", patient.weight)
    print("Height:", patient.height)
    print("BMI:", patient.bmi)


patient_details = {"name": "Siddhant Sharma", "age": 32, "contact_details": {"emergency_contact": "9823444"}, "email": "sidsharma2401@gmail.com", "weight": 75, "height": 1.8}
patient1 = Patient(**patient_details)

print_patient_info(patient1)

