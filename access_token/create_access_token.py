from fyers_apiv3 import fyersModel
import json

client_id = "ALT6RUE1IF-100"
secret_key = "0UT0LW5PE4"
redirect_uri = "https://luvratan.tech/"

def get_auth_url():
    """Generate auth URL for FYERS login"""
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        state="sample_state"
    )
    return session.generate_authcode()

def generate_token_from_auth_code(auth_code: str):
    """Exchange auth_code for access_token"""
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code"
    )
    
    session.set_token(auth_code)
    token_response = session.generate_token()
    
    # Save to JSON file
    with open("../assets/fyers_token.json", "w") as f:
        json.dump(token_response, f, indent=2)
    
    return token_response

def get_token_from_file():
    """Read token from JSON file"""
    try:
        with open("../assets/fyers_token.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None