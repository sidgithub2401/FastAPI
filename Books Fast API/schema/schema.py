from pydantic import BaseModel, Field
from typing import Annotated, List


class Books(BaseModel):
      bookId:Annotated[str,Field(...,description="Enter the Book id", example="BK001")] 
      title: Annotated[str,Field(...,description="Enter the title of the book")]
      author:Annotated[str,Field(...,description="Enter the author of the book")]
      genre: Annotated[str,Field(...,description="Enter the genre")]
      publishedYear:Annotated[int,Field(...,description="In which year was it published")] 
      rating:Annotated[float,Field(...,description="Enter the rating")]
      price: Annotated[int,Field(...,description="Enter the Price in Rupees",gt=500)]
      stock: Annotated[int,Field(...,description="Enter the number of Stockes Purchased")]
      isbn: Annotated[str,Field(...)]
      available: Annotated[bool,Field(...,description="Enter whether the book is available or not")]


class Members(BaseModel):
    memberId:Annotated[str, Field(...,description="Enter the member Id")]
    name: Annotated[str, Field(...,description="Enter the member name")]
    email: Annotated[str, Field(...,description="Enter the email",)]
    phone: Annotated[str, Field(...,description="Enter the member phone number")]
    membershipType: Annotated[str, Field(...,description="Enter the membership type")]
    booksIssued:Annotated[List,Field(...)]
      

