from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client
import uuid
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
key_admin = os.environ.get("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)

supabaseAdmin = create_client(url, key_admin)

admin = supabaseAdmin.auth.admin

# response = supabaseAdmin.auth.admin.create_user({
#    "email" : "carlos1234AE@gmail.com",
#    "password" : "carlos123AE4",
#     "user_metadata" : {
#         "Name" : "Carlos"
#                   }s
#  })

# print(response.user)
# supabase.auth.sign_in_with_password(
#      {"email":"vidalae29@example.com",
#       "password":"carlos123"}
#  )
# usuario = supabase.auth.get_session()

# user_id = usuario.user.id
# print(user_id)


# response = (
#     supabase.table("usuario")
#     .update({"usuario": "LLLL"})
#     .eq("id_usuario", 22)
#     .execute()
# )
# print(response)
# uuid = uuid.UUID("32414682-def1-4a8c-a8ad-66fe818e4b12")
# usuario = supabase.table("usuario").select("*").eq("principal",uuid).execute()
# print(f'ID dsadasdsa',usuario.data[0]["id_usuario"])