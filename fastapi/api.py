from fastapi import FastAPI, HTTPException
from pandas import read_csv

from config import DATA_PATH, NUMBER_OF_ROWS
from units import Row, RowCreate

# Create the FastAPI instance
app = FastAPI(
    title='Earthquakes API',
    description='An API of earthquakes analysis project',
    version='1.0.0',
    root_path='/api',
    docs_url='/docs',
    root_path_in_servers=False
)

# Load dataset
data = read_csv(DATA_PATH, engine='pyarrow') if NUMBER_OF_ROWS == -1 else read_csv(DATA_PATH, nrows=NUMBER_OF_ROWS)


@app.get('/get_row/{index}')
def get_row(index: int) -> Row:
    try:
        row = Row(index=index, **(data.iloc[index].to_dict()))
    except IndexError:
        raise HTTPException(status_code=404, detail='Index out of range')

    return row


@app.post('/create_row')
def get_row(row: RowCreate) -> Row:
    data.loc[len(data)] = dict(row)

    return {'index':len(data) - 1}


@app.get("/health")
async def health_check():
    return 'ok'


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
