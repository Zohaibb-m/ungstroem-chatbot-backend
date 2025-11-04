import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timedelta

load_dotenv()

class DatabaseHandler():
    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        self.supabase: Client = create_client(url, key)
        self.users = self.supabase.table("users")

    def register_user(self, name, email: str, password: str, phone: str = ""):
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            if not response.user:
                raise Exception("Registration failed")
            
            user_id = response.user.id

            # Insert user into 'users' table
            self.users.insert({
                "uid": user_id,
                "name": name,
                "email": email,
                "role": "user",
                "phone": phone
            }).execute()
            return {"message": "User registered successfully", "data": response, "status_code": 200}
        except Exception as e:
            return {"error": f"An error occurred during user registration: {e}", "status_code": 404}

    def login_user(self, email: str, password: str):
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            print(response)
            return {
                "message": "User logged in successfully", 
                "user": {
                    "id":response.user.id, 
                    "email": response.user.user_metadata["email"]
                },
                "token": response.session.access_token,
                "status_code": 200
                }
        except Exception as e:
            return {"error": f"An error occured during login: {e}", "status_code": 404}
    
    def get_all_users(self):
        try:
            users = self.users.select("*").execute()
            return {"message": "Users retrieved successfully", "data": users.data, "status_code": 200}
        except Exception as e:
            return {"error": f"An error occurred while fetching users: {e}", "status_code": 404}