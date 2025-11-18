from pydantic import BaseModel,Field,field_validator
from typing import Optional,List,Dict,Annotated

# By default everything is default in pydantic model but we can change that behavior by using Optional from typing module

class Patient(BaseModel):
    name:str = Field(max_length=100)
    age:Optional[int] = Field(gt=18,description="Age must be greater than 18")
    city:str = "Pune"
    allergies:List[str]
    contact_details:Dict[str,str]
    salary : Annotated[int, Field(description="default salary is 70000",default=70000,gt=60000)]
    email : Annotated[str, Field(...,description="Email is required field")]

#field validators are used to validate the fields in pydantic models and it works on only one field at a time

    @field_validator('email')
    @classmethod 
    #in value the value of the field will be passed and cls is the class itself
    def validate_email(cls,value):
        accepted_emails = ['hdfc.com','axis.com']
        domain = value.split('@')[-1]
        if domain not in accepted_emails:
            raise ValueError(f"Email domain must be one of the following: {', '.join(accepted_emails)}")
        else:
            return value

    @field_validator("name")
    @classmethod
    def uppercase_name(cls,value):
        return value.upper() 

def print_patient_details(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.city)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.salary)
    print(patient.email)


patient_details = {"name":"Siddhant Sharma","age":24,"city":"Delhi","allergies":["pollen","dust"],"contact_details":{"email":"sidsharma2401@gmail.com","phone":"9823444"},"salary":80000,"email":"sidsharma2401@axis.com"}

patient1 = Patient(**patient_details)

print_patient_details(patient1)

