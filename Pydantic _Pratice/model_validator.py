from pydantic import BaseModel, model_validator , Field
from typing import Optional, List, Dict, Annotated

class Patient(BaseModel):
    name : Annotated[str, Field(...,description="Name of the patient",max_length=100)]
    age : Annotated[int, Field(...,gt=18,description="Age must be greater than 18")]
    contact_details : Annotated[Dict[str,str], Field(...,description="Contact details of the patient")]
    email : Annotated[str,Field(...,description="Email of the patient belonging to HDFC and ICICI bank")]

# model validators work on the entire model and can be used to validate multiple fields at once

    @model_validator(mode="after")
    def validate_age(cls,model):
        if model.age > 60 and 'emergency_contact' not in model.contact_details:
            raise ValueError("Emergency contact is required for patients above 60 years old")
        else:
            return model
        
    @model_validator(mode="after")
    def uppercase_name(cls,model):
        model.name = model.name.upper()
        return model
    
    @model_validator(mode="after")
    def validate_email_domain(cls,model):
        accpeted_domains = ["hdfcbank.com","icicibank.com"]
        domain = model.email.split("@")[-1]
        if domain not in accpeted_domains:
            raise ValueError(f"Email domain must be one of the following domains :{', '.join(accpeted_domains)}")
        else:
            return model

def print_patient_info(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.contact_details) 
    print(patient.email)

patient_details = {"name": "Siddhant Sharma", "age": 32, "contact_details": {"emergency_contact": "9823444"}, "email": "sidsharma2401@icicibank.com"}
#patient1= Patient(name="Siddhant Sharma",age=32,contact_details={"emergency_contact":"9823444"},email="sidsharma2401@icicibank.com")
patient1 = Patient(**patient_details)
print_patient_info(patient1)