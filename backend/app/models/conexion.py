# conexion.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ruta de la base de datos
db_path = '..\\..\\bd\\miProyecto.db'

# Crea la conexión
engine = create_engine(f'sqlite:///{db_path}')

# Crea una sesión para interactuar con la base de datos
LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()
