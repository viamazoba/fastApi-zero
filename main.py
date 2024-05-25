from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles
app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static/images/"), name="static")


@app.get('/')
async def root():
    return '¡Hola mundo!'


@app.get('/home')
async def home():
    return {'home': 'Este es el home'}
