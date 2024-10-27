from sqlalchemy import create_engine, text, Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# Ruta de la base de datos
db_path = 'C:\\Users\\Carlos\\Desktop\\Proyectos\\Web-Neyo-PPP\\backend\\bd\\miProyecto.db'

# Crea la conexión
engine = create_engine(f'sqlite:///{db_path}')

# Crea una sesión para interactuar con la base de datos
LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

# Definición del modelo Usuario
class Usuario(Base):
    __tablename__ = "USUARIO"
    
    IdUsuario = Column(Integer, primary_key=True, index=True)
    Usuario = Column(String(30), unique=True, nullable=False)
    Clave = Column(String(30), unique=True, nullable=False)
    Nombre = Column(String(30), nullable=False)
    Apellido = Column(String(30), nullable=False)
    Fecha_registro = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    Departamento = Column(String(50), nullable=False)
    Provincia = Column(String(50), nullable=False)
    Distrito = Column(String(50), nullable=False)
    Direccion = Column(String(50), nullable=False)
    Correo = Column(String(50), unique=True, nullable=False)

    # Restricciones de unicidad
    __table_args__ = (
        UniqueConstraint("Usuario", "Clave", "Correo", name="uq_usuario_clave_correo"),
        {'extend_existing': True}  # Agregar esta línea
    )

# Prueba la conexión ejecutando una consulta (por ejemplo, seleccionando los nombres de las tablas)
with engine.connect() as connection:
    result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    print("Tablas en la base de datos:", [row[0] for row in result])

# Consultar y mostrar todos los registros de la tabla usuarios
with LocalSession() as session:
    # Crear la tabla si no existe
    Base.metadata.create_all(bind=engine)

    # Consultar todos los registros de la tabla USUARIO
    usuarios = session.query(Usuario).all()  # Recupera todos los registros de la tabla USUARIO
    
    # Muestra los registros
    for usuario in usuarios:
        print(f"ID: {usuario.IdUsuario}, Usuario: {usuario.Usuario}, Nombre: {usuario.Nombre}, Apellido: {usuario.Apellido} ")
