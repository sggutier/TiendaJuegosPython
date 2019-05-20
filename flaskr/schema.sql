drop table if exists productos;
CREATE TABLE productos (
  idjuego int(11) NOT NULL AUTO_INCREMENT,
  nombre varchar(50) NOT NULL,
  genero varchar(50) NOT NULL,
  fechalanzamiento date NOT NULL,
  desarrollador varchar(50) NOT NULL,
  clasificacion varchar(30) NOT NULL,
  precio decimal(10,2) NOT NULL,
  stock int(11) NOT NULL,
  descripcion text NOT NULL,
  imagen longblob DEFAULT NULL,
  PRIMARY KEY (idjuego)
);
