use ventas;

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

select * from productos;

drop table if exists auditoria;
create table auditoria (
    idaudi int not null auto_increment primary key,
    accion varchar(10),
    usr varchar(70),
    timestamp datetime,
    idjuegoViejo int(11) DEFAULT NULL,
    nombreViejo varchar(50) DEFAULT NULL,
    generoViejo varchar(50) DEFAULT NULL,
    fechalanzamientoViejo date DEFAULT NULL,
    desarrolladorViejo varchar(50) DEFAULT NULL,
    clasificacionViejo varchar(30) DEFAULT NULL,
    precioViejo decimal(10,2) DEFAULT NULL,
    stockViejo int(11) DEFAULT NULL,
    descripcionViejo text DEFAULT NULL,
    imagenViejo longblob DEFAULT NULL,
    idjuegoNuevo int(11) DEFAULT NULL,
    nombreNuevo varchar(50) DEFAULT NULL,
    generoNuevo varchar(50) DEFAULT NULL,
    fechalanzamientoNuevo date DEFAULT NULL,
    desarrolladorNuevo varchar(50) DEFAULT NULL,
    clasificacionNuevo varchar(30) DEFAULT NULL,
    precioNuevo decimal(10,2) DEFAULT NULL,
    stockNuevo int(11) DEFAULT NULL,
    descripcionNuevo text DEFAULT NULL,
    imagenNuevo longblob DEFAULT NULL
);
select  * from auditoria;

drop trigger if exists trigInsertar;

delimiter  $$
CREATE TRIGGER trigInsertar AFTER INSERT ON productos
	FOR EACH ROW
	BEGIN
	  INSERT INTO auditoria (accion, usr, timestamp,
	                            idjuegoNuevo,
                                nombreNuevo,
                                generoNuevo,
                                fechalanzamientoNuevo,
                                desarrolladorNuevo,
                                clasificacionNuevo,
                                precioNuevo,
                                stockNuevo,
                                descripcionNuevo,
                                imagenNuevo)
	  VALUES('insert', USER(), NOW(),
	        NEW.idjuego,
            NEW.nombre,
            NEW.genero,
            NEW.fechalanzamiento,
            NEW.desarrollador,
            NEW.clasificacion,
            NEW.precio,
            NEW.stock,
            NEW.descripcion,
            NEW.imagen);
	END;
$$

drop trigger if exists trigBorrar;

delimiter  $$
CREATE TRIGGER trigBorrar AFTER delete ON productos
	FOR EACH ROW
	BEGIN
	  INSERT INTO auditoria (accion, usr, timestamp,
	                            idjuegoViejo,
                                nombreViejo,
                                generoViejo,
                                fechalanzamientoViejo,
                                desarrolladorViejo,
                                clasificacionViejo,
                                precioViejo,
                                stockViejo,
                                descripcionViejo,
                                imagenViejo)
	  VALUES('delete', USER(), NOW(),
	        OLD.idjuego,
            OLD.nombre,
            OLD.genero,
            OLD.fechalanzamiento,
            OLD.desarrollador,
            OLD.clasificacion,
            OLD.precio,
            OLD.stock,
            OLD.descripcion,
            OLD.imagen);
	END;
$$

drop trigger if exists trigActualizar;

delimiter  $$
CREATE TRIGGER trigActualizar AFTER update ON productos
	FOR EACH ROW
	BEGIN
	  INSERT INTO auditoria (accion, usr, timestamp,
	                            idjuegoViejo,
                                nombreViejo,
                                generoViejo,
                                fechalanzamientoViejo,
                                desarrolladorViejo,
                                clasificacionViejo,
                                precioViejo,
                                stockViejo,
                                descripcionViejo,
                                imagenViejo,
	                            idjuegoNuevo,
                                nombreNuevo,
                                generoNuevo,
                                fechalanzamientoNuevo,
                                desarrolladorNuevo,
                                clasificacionNuevo,
                                precioNuevo,
                                stockNuevo,
                                descripcionNuevo,
                                imagenNuevo)
	  VALUES('update', USER(), NOW(),
	        if(NEW.idjuego = OLD.idjuego, NULL, OLD.idjuego),
            if(NEW.nombre = OLD.nombre, NULL, OLD.nombre),
            if(NEW.genero = OLD.genero, NULL, OLD.genero),
            if(NEW.fechalanzamiento = OLD.fechalanzamiento, NULL, OLD.fechalanzamiento),
            if(NEW.desarrollador = OLD.desarrollador, NULL, OLD.desarrollador),
            if(NEW.clasificacion = OLD.clasificacion, NULL, OLD.clasificacion),
            if(NEW.precio = OLD.precio, NULL, OLD.precio),
            if(NEW.stock = OLD.stock, NULL, OLD.stock),
            if(NEW.descripcion = OLD.descripcion, NULL, OLD.descripcion),
            if(NEW.imagen = OLD.imagen, NULL, OLD.imagen),

            if(NEW.idjuego = OLD.idjuego, NULL, NEW.idjuego),
            if(NEW.nombre = OLD.nombre, NULL, NEW.nombre),
            if(NEW.genero = OLD.genero, NULL, NEW.genero),
            if(NEW.fechalanzamiento = OLD.fechalanzamiento, NULL, NEW.fechalanzamiento),
            if(NEW.desarrollador = OLD.desarrollador, NULL, NEW.desarrollador),
            if(NEW.clasificacion = OLD.clasificacion, NULL, NEW.clasificacion),
            if(NEW.precio = OLD.precio, NULL, NEW.precio),
            if(NEW.stock = OLD.stock, NULL, NEW.stock),
            if(NEW.descripcion = OLD.descripcion, NULL, NEW.descripcion),
            if(NEW.imagen = OLD.imagen, NULL, NEW.imagen));
	END;
$$
