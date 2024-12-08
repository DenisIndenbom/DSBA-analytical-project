from datetime import datetime

from pydantic import BaseModel


# Models
class Row(BaseModel):
    index: int
    time: int
    place: str
    status: str
    tsunami: int
    significance: float
    data_type: str
    magnitudo: float
    state: str
    longitude: float
    latitude: float
    depth: float
    date: datetime


class RowCreate(BaseModel):
    time: int
    place: str
    status: str
    tsunami: int
    significance: float
    data_type: str
    magnitudo: float
    state: str
    longitude: float
    latitude: float
    depth: float
    date: datetime


class NewRow(BaseModel):
    index: int
