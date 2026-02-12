from pydantic import BaseModel


class DataItem(BaseModel):
    key: str
    value: str
