CREATE TABLE rol(
id_Rol SERIAL,
nombre VARCHAR(20) NOT NULL,
descripcion VARCHAR(50),
CONSTRAINT pk_rol PRIMARY KEY (id_Rol)
);

CREATE TABLE usuario(
id_Usuario SERIAL,
usuario VARCHAR(20),
clave VARCHAR(70) NOT NULL,
nombre VARCHAR(50),
apellido VARCHAR(50),
fecha_Registro TIMESTAMP DEFAULT NOW(),
departamento VARCHAR(50),
provincia VARCHAR(50),
distrito VARCHAR(50),
direccion VARCHAR(100),
correo VARCHAR(120),
id_Rol SERIAL,
CONSTRAINT pk_usuario PRIMARY KEY (id_Usuario),
CONSTRAINT uq_usuario_correo UNIQUE (correo),
CONSTRAINT fk_usuario_rol FOREIGN KEY (id_Rol) REFERENCES rol(id_Rol)
	ON DELETE SET NULL
	ON UPDATE CASCADE
);

CREATE TABLE telefono(
id_Telefono SERIAL,
numero VARCHAR(15),
id_Usuario SERIAL,
CONSTRAINT pk_telefono PRIMARY KEY (id_Telefono),
CONSTRAINT fk_telefono_usuario FOREIGN KEY (id_Usuario) 
REFERENCES usuario(id_Usuario)
ON DELETE CASCADE
ON UPDATE CASCADE
);


CREATE TABLE categoria(
id_Categoria SERIAL,
nombre VARCHAR(20) NOT NULL,
CONSTRAINT pk_categoria PRIMARY KEY (id_Categoria)
);

CREATE TABLE modelo(
id_Modelo SERIAL,
nombre VARCHAR(50) NOT NULL,
marca VARCHAR(30),
CONSTRAINT pk_modelo PRIMARY KEY (id_Modelo)
);

CREATE TABLE estado(
id_Estado SERIAL,
valor VARCHAR(30) NOT NULL,
CONSTRAINT pk_estado PRIMARY KEY (id_Estado)
);


CREATE TABLE estado_pedido(
id_Estado_pedido SERIAL,
valor VARCHAR(30) NOT NULL,
CONSTRAINT pk_estado_pedido PRIMARY KEY (id_Estado_pedido)
);


CREATE TABLE pedido(
id_Pedido SERIAL,
estado VARCHAR(30) NOT NULL,
total NUMERIC (8,2) NOT NULL,
fecha_Registro TIMESTAMP DEFAULT NOW(),
id_usuario SERIAL NOT NULL,
id_estado_pedido SERIAL NOT NULL,
CONSTRAINT pk_pedido PRIMARY KEY (id_Pedido),
CONSTRAINT fk_pedido_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id_Usuario)
	ON UPDATE CASCADE,
CONSTRAINT fk_pedido_estado_pedido FOREIGN KEY (id_estado_pedido) REFERENCES pedido (id_Estado_pedido)
	ON DELETE SET NULL
	ON UPDATE CASCADE
);


CREATE TABLE carrito_compra(
id_Carrito SERIAL,
id_usuario SERIAL NOT NULL,
CONSTRAINT pk_carrito PRIMARY KEY (id_Carrito),
CONSTRAINT fk_carrito_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id_Usuario)
    ON UPDATE CASCADE
);


CREATE TABLE producto(
id_Producto SERIAL,
nombre VARCHAR(30) NOT NULL,
descripcion VARCHAR(100),
precio NUMERIC(8,2) NOT NULL,
url_Imagen VARCHAR(200),
id_Modelo SERIAL,
id_Categoria SERIAL,
id_Estado SERIAL,
fecha_Registro TIMESTAMP DEFAULT NOW(),
CONSTRAINT pk_producto PRIMARY KEY (id_Producto),
CONSTRAINT fk_producto_modelo FOREIGN KEY (id_Modelo)
	REFERENCES modelo(id_Modelo)
	ON DELETE SET NULL
	ON UPDATE CASCADE,
CONSTRAINT fk_producto_categoria FOREIGN KEY (id_Categoria)
	REFERENCES categoria(id_Categoria)
	ON DELETE SET NULL
	ON UPDATE CASCADE,
CONSTRAINT fk_producto_estado FOREIGN KEY (id_Estado)
	REFERENCES estado(id_Estado)
	ON DELETE SET NULL
	ON UPDATE CASCADE
);


CREATE TABLE inventario(
id_Inventario SERIAL,
cantidad INTEGER NOT NULL DEFAULT 0,
id_Producto SERIAL,
CONSTRAINT pk_inventario PRIMARY KEY(id_Inventario),
CONSTRAINT fk_inventario_producto FOREIGN KEY (id_Producto)
	REFERENCES producto (id_Producto)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);


CREATE TABLE comentario(
id_comentario SERIAL,
contenido VARCHAR(300),
valoracion VARCHAR(1),
fecha_Registro TIMESTAMP DEFAULT NOW(),
id_Producto SERIAL,
id_Usuario SERIAL,
CONSTRAINT pk_comentario PRIMARY KEY (id_comentario),
CONSTRAINT fk_comentario_producto FOREIGN KEY (id_Producto)
	REFERENCES producto (id_Producto)
	ON DELETE SET NULL
	ON UPDATE CASCADE
);


CREATE TABLE detalle_pedido(
id_Detalle SERIAL,
cantidad INTEGER NOT NULL,
precio_Venta NUMERIC(8,2) NOT NULL,
subtotal Numeric(8,2) NOT NULL,
id_Producto SERIAL,
id_Pedido SERIAL,
CONSTRAINT pk_detalle PRIMARY KEY (id_Detalle),
CONSTRAINT fk_detalle_producto FOREIGN KEY (id_Producto)
	REFERENCES producto (id_Producto)
	ON DELETE SET NULL
	ON UPDATE CASCADE,
CONSTRAINT fk_detalle_pedido FOREIGN KEY (id_Pedido)
	REFERENCES pedido (id_Pedido)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE detalle_carrito(
id_Detalle_carrito SERIAL,
cantidad INTEGER NOT NULL,
id_Producto SERIAL,
id_Carrito SERIAL,
CONSTRAINT pk_detalle_carrito PRIMARY KEY (id_Detalle_carrito),
CONSTRAINT fk_detalle_carrito_producto FOREIGN KEY (id_Producto)
	REFERENCES producto (id_Producto)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
CONSTRAINT fk_detalle_carrito FOREIGN KEY (id_Carrito)
    REFERENCES carrito_compra (id_Carrito)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE historial_pedido(
	id_historial_pedido SERIAL,
	id_Pedido SERIAL,
	id_estado_actual SERIAL,
	id_estado_anterior SERIAL,
	fecha_cambio TIMESTAMP DEFAULT NOW(),
	CONSTRAINT pk_historial_pedido PRIMARY KEY (id_historial_pedido),
	CONSTRAINT fk_historial_pedido_pedido FOREIGN KEY (id_Pedido)
		REFERENCES pedido (id_Pedido)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CONSTRAINT fk_historial_pedido_estado_actual FOREIGN KEY (id_estado_actual)
		REFERENCES estado_pedido (id_Estado_pedido)
		ON DELETE SET NULL
		ON UPDATE CASCADE,
	CONSTRAINT fk_historial_pedido_estado_anterior FOREIGN KEY (id_estado_anterior)
		REFERENCES estado_pedido (id_Estado_pedido)
		ON DELETE SET NULL
		ON UPDATE CASCADE
	
);

CREATE TABLE metodo_pago(
	id_metodo_pago SERIAL,
	nombre VARCHAR(30) NOT NULL,
	descripcion VARCHAR(100),
	CONSTRAINT pk_metodo_pago PRIMARY KEY (id_metodo_pago)
);

CREATE TABLE estado_pago(
	id_estado_pago SERIAL,
	valor VARCHAR(30) NOT NULL,
	CONSTRAINT pk_estado_pago PRIMARY KEY (id_estado_pago)
);

CREATE TABLE pago(
	id_pago SERIAL,
	monto NUMERIC(8,2) NOT NULL,
	fecha_registro TIMESTAMP DEFAULT NOW(),
	id_pedido SERIAL,
	id_metodo_pago SERIAL,
	id_estado_pago SERIAL,
	CONSTRAINT pk_pago PRIMARY KEY (id_pago),
	CONSTRAINT fk_pago_pedido FOREIGN KEY (id_pedido)
		REFERENCES pedido (id_Pedido)
		ON DELETE SET NULL
		ON UPDATE CASCADE,
	CONSTRAINT fk_pago_metodo_pago FOREIGN KEY (id_metodo_pago)
		REFERENCES metodo_pago (id_metodo_pago)
		ON DELETE SET NULL
		ON UPDATE CASCADE,
	CONSTRAINT fk_pago_estado_pago FOREIGN KEY (id_estado_pago)
		REFERENCES estado_pago (id_estado_pago)
		ON DELETE SET NULL
		ON UPDATE CASCADE
	
);