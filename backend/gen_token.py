from supabase import create_client
from dotenv import load_dotenv
import os
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

res = supabase.auth.sign_in_with_password({
    # "email": "olukosikehinde5@gmail.com",
    # "password": "doors&098"
    # "email": "j.ions.eons@gmail.com",
    # "password": "j.ions.eons_01"
    # "email": "tov.ananim@gmail.com",
    # "password": "tov_ananim",
    "email": "diaken@proton.me",
    "password": "diaken01"
})

print("Access Token:", res.session.access_token)
print("User ID:", res.user.id)