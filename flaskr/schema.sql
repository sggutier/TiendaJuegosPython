DROP TABLE IF EXISTS juegos;

CREATE TABLE juegos (
  idjuego int(11) NOT NULL AUTO_INCREMENT,
  nombre varchar(50) NOT NULL,
  genero varchar(50) NOT NULL,
  fechalanzamiento date NOT NULL,
  desarrollador varchar(50) NOT NULL,
  clasificacion varchar(30) NOT NULL,
  precio decimal(10,2) NOT NULL,
  rating decimal(3,2) NOT NULL,
  publicador varchar(50) NOT NULL,
  imagen blob,
  PRIMARY KEY (idjuego)
) ;

