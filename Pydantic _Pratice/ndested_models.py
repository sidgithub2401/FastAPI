from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Annotated

class Address(BaseModel):
    street: str = Field(..., max_length=100)
    city: str = Field(..., max_length=50)
    state: str = Field(..., max_length=50)
    zip_code: str = Field(..., max_length=10)

address_details = {"street": "123 Main St", "city": "Pune", "state": "Maharashtra", "zip_code": "411001"}

address1 = Address(**address_details)

class Patient(BaseModel):
    name : Annotated[str, Field(..., description="Name of the patient", max_length=100)]
    address : Annotated[Address, Field(..., description="Address details of the patient")]

patient_details = {"name": "John Doe", "address": address1}
patient1 = Patient(**patient_details)
print(patient1.name)
print(patient1.address)  # Accessing nested model attribute
print(patient1.address.state)  # Accessing nested model attribute
print(patient1.address.city)   # Accessing nested model attribute

