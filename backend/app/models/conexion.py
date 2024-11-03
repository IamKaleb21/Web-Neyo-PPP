# librerias necesario
from supabase import create_client, Client
from decouple import config
#Parametros url, key de un nuevo proyecto 
url = config("SUPERBASE_URL")
key = config ("SUPERBASE_KEY")

# Inicializar un nuevo cliente Supabase 
supabase: Client = create_client(url, key)