import requests
from fastapi import FastAPI, Request, HTTPException

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    title="SFACG WEB LOGIN",
)


@app.middleware("http")
async def add_cors(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers[
        "Access-Control-Allow-Headers"] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    return response


@app.get("/login")
async def login(name, password, al, session, sig, token, scene):
    if not name or not password:
        raise HTTPException(status_code=400, detail="username or password is empty")
    if not al or not session or not sig or not token or not scene:
        raise HTTPException(status_code=400, detail="al, session, sig, token, scene is empty")

    url = "https://passport.sfacg.com/Ajax/QuickLogin.ashx"
    res = requests.get(url, params={
        "name": name,
        "password": password,
        "al": al,
        "session": session,
        "sig": sig,
        "token": token,
        "scene": scene
    })
    if res.status_code == 200:
        return {
            "code": res.status_code,
            "message": "success",
            "SFCommunity": res.cookies[".SFCommunity"],
            "session_PC": res.cookies["session_PC"]
        }
    else:
        return {
            "code": res.status_code,
            "message": "login failed, please check your username and password",
        }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", reload=True)
