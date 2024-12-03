from fastapi import FastAPI, HTTPException
from pandas import read_csv

from config import DATA_PATH
from units import Row, RowCreate

# Create the FastAPI instance
app = FastAPI(
    title='Earthquakes API',
    description='An API of earthquakes analysis project',
    version='1.0.0'
)

# Load dataset
data = read_csv(DATA_PATH, engine='pyarrow')


@app.get('/get_row/{index}')
def get_row(index: int):
    try:
        row = Row(index=index, **(data.iloc[index].to_dict()))
    except IndexError:
        raise HTTPException(status_code=404, detail='Index out of range')

    return row


@app.post('/create_row')
def get_row(row: RowCreate):
    data.loc[len(data)] = dict(row)

    return {'index': len(data) - 1}
