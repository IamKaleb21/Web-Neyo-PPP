from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Ruta de la base de datos
db_path = 'C:\\Users\\Carlos\\Desktop\\Proyectos\\Web-Neyo-PPP\\backend\\bd\\miProyecto.db'

# Crea la conexión
engine = create_engine(f'sqlite:///{db_path}')

# Crea una sesión para interactuar con la base de datos
Session = sessionmaker(autoflush=False, autocommit =False, bind=engine)
session = Session()

# Prueba la conexión ejecutando una consulta (por ejemplo, seleccionando los nombres de las tablas)
with engine.connect() as connection:
    result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    print("Tablas en la base de datos:", [row[0] for row in result])

session.close()
