from fastapi import FastAPI
from access_token.create_access_token import get_auth_url, generate_token_from_auth_code, get_token_from_file

app = FastAPI()

@app.get("/")
def home():
    return "Welcome to the Ultimate trading Bot"

@app.get("/auth-url")
def auth_url():
    """Get FYERS auth URL"""
    url = get_auth_url()
    return url

@app.post("/update-token")
def update_token(redirected_url: str):
    """Update token using redirected URL"""
    # Extract auth_code
    try:
        auth_code = redirected_url.split("auth_code=")[1].split("&")[0]
    except IndexError:
        return {"error": "Invalid redirect URL"}
    
    token_response = generate_token_from_auth_code(auth_code)
    return {"success": True, "token": token_response}

@app.get("/get-token")
def get_token():
    """Get current token"""
    token = get_token_from_file()
    if token:
        return token
    return {"error": "No token found"}