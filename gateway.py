import sqlite3 as sqlite
import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
import secrets
import uvicorn
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()
security = HTTPBasic()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

with open('config.json') as json_file:
    config = json.load(json_file)

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, config["main"]["admin-username"])
    correct_password = secrets.compare_digest(credentials.password, config["main"]["admin-password"])
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
async def index(request: Request):
    heights = await getHeights()
    return templates.TemplateResponse("index.html", {"request": request, 
                                                     "chainName": config['main']['name'],
                                                     "assetID": config['tn']['assetId'],
                                                     "tn_gateway_fee":config['tn']['gateway_fee'],
                                                     "tn_network_fee":config['tn']['network_fee'],
                                                     "tn_total_fee":config['tn']['network_fee']+config['tn']['gateway_fee'],
                                                     "waves_gateway_fee":config['waves']['gateway_fee'],
                                                     "waves_network_fee":config['waves']['network_fee'],
                                                     "waves_total_fee":config['waves']['network_fee'] + config['waves']['gateway_fee'],
                                                     "fee": config['tn']['fee'],
                                                     "company": config['main']['company'],
                                                     "email": config['main']['contact-email'],
                                                     "telegram": config['main']['contact-telegram'],
                                                     "recovery_amount":config['main']['recovery_amount'],
                                                     "recovery_fee":config['main']['recovery_fee'],
                                                     "wavesHeight": heights['Waves'],
                                                     "tnHeight": heights['TN'],
                                                     "tnAddress": config['tn']['gatewayAddress'],
                                                     "wavesAddress": config['waves']['gatewayAddress'],
                                                     "disclaimer": config['main']['disclaimer']}})

@app.get('/heights')
async def getHeights():
    dbCon = sqlite.connect('gateway.db')
    result = dbCon.cursor().execute('SELECT chain, height FROM heights WHERE chain = "Waves" or chain = "TN"').fetchall()
    return { result[0][0]: result[0][1], result[1][0]: result[1][1] }

@app.get('/errors')
async def getErrors(request: Request, username: str = Depends(get_current_username)):
    if (config["main"]["admin-username"] == "admin" and config["main"]["admin-password"] == "admin"):
        return {"message": "change the default username and password please!"}
    
    if username == config["main"]["admin-username"]:
        dbCon = sqlite.connect('gateway.db')
        result = dbCon.cursor().execute('SELECT * FROM errors').fetchall()
        return templates.TemplateResponse("errors.html", {"request": request, "errors": result})

@app.get('/executed')
async def getErrors(request: Request, username: str = Depends(get_current_username)):
    if (config["main"]["admin-username"] == "admin" and config["main"]["admin-password"] == "admin"):
        return {"message": "change the default username and password please!"}
    
    if username == config["main"]["admin-username"]:
        dbCon = sqlite.connect('gateway.db')
        result = dbCon.cursor().execute('SELECT * FROM executed').fetchall()
        return templates.TemplateResponse("tx.html", {"request": request, "txs": result})

@app.get("/api/fullinfo")
async def api_fullinfo(request: Request):
    heights = await getHeights()
    return {"chainName": config['main']['name'],
            "assetID": config['tn']['assetId'],
            "tn_gateway_fee":config['tn']['gateway_fee'],
            "tn_network_fee":config['tn']['network_fee'],
            "tn_total_fee":config['tn']['network_fee']+config['tn']['gateway_fee'],
            "waves_gateway_fee":config['waves']['gateway_fee'],
            "waves_network_fee":config['waves']['network_fee'],
            "waves_total_fee":config['waves']['network_fee'] + config['waves']['gateway_fee'],
            "fee": config['tn']['fee'],
            "company": config['main']['company'],
            "email": config['main']['contact-email'],
            "telegram": config['main']['contact-telegram'],
            "recovery_amount":config['main']['recovery_amount'],
            "recovery_fee":config['main']['recovery_fee'],
            "wavesHeight": heights['Waves'],
            "tnHeight": heights['TN'],
            "tnAddress": config['tn']['gatewayAddress'],
            "wavesAddress": config['waves']['gatewayAddress'],
            "disclaimer": config['main']['disclaimer']}
