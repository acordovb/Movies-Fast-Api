''' Only User Schema '''

from pydantic import BaseModel

class User(BaseModel):
    ''' User Model Base '''
    email: str
    password: str

    class Config:
        ''' Config class to login '''
        json_schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "password": "admin"
            }
        }
