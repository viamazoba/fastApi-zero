from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return '¡Hola mundo!'


@app.get('/home')
async def home():
    return {'home': 'Este es el home'}
