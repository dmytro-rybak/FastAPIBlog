import re
from pydantic import BaseModel, EmailStr, validator, validate_email


class UserSchema(BaseModel):
    username: str
    email: EmailStr



class UserWithPass(UserSchema):
    password: str


class UserValidate(UserWithPass):
    @validator('email')
    def check_email(cls, value):
        if not validate_email(value):
            raise ValueError('Invalid email')
        return value

    @validator('username')
    def check_username(cls, value):
        pattern = r'^(?=.{3,30}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'
        if not re.match(pattern, value):
            raise ValueError('Invalid username')
        return value

    @validator('password')
    def check_password(cls, value):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(pattern, value):
            raise ValueError('Password must contains minimum eight characters, at least one uppercase letter, '
                             'one lowercase letter, one number and one special character:')
        return value


class UserShow(UserSchema):
    class Config:
        orm_mode = True
