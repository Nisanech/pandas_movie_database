USE movies;

-- -----------------------------------------------------
-- Cargar datos: Actor
-- -----------------------------------------------------
LOAD DATA INFILE '/var/lib/mysql-files/actor.txt'
INTO TABLE actor 
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\r\n'
IGNORE 0 LINES;

-- -----------------------------------------------------
-- Cargar datos: Director
-- -----------------------------------------------------
LOAD DATA INFILE '/var/lib/mysql-files/director.txt'
INTO TABLE director 
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\r\n'
IGNORE 0 LINES;

-- -----------------------------------------------------
-- Cargar datos: Generos
-- -----------------------------------------------------
LOAD DATA INFILE '/var/lib/mysql-files/genres.txt'
INTO TABLE genres 
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\r\n'
IGNORE 0 LINES;

-- -----------------------------------------------------
-- Cargar datos: Peliculas
-- -----------------------------------------------------
LOAD DATA INFILE '/var/lib/mysql-files/movie.txt'
INTO TABLE movie 
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\r\n'
IGNORE 0 LINES;

-- -----------------------------------------------------
-- Cargar datos: Relacion actor - pelicula
-- -----------------------------------------------------
LOAD DATA INFILE '/var/lib/mysql-files/movie_cast.txt'
INTO TABLE movie_cast 
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\r\n'
(act_id, mov_id, role)
IGNORE 0 LINES;

-- -----------------------------------------------------
-- Cargar datos: Relacion director - pelicula
-- -----------------------------------------------------
LOAD DATA INFILE '/var/lib/mysql-files/movie_direction.txt'
INTO TABLE movie_direction 
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\r\n'
IGNORE 0 LINES;

-- -----------------------------------------------------
-- Cargar datos: Relacion genero - pelicula
-- -----------------------------------------------------
LOAD DATA INFILE '/var/lib/mysql-files/movie_genres.txt'
INTO TABLE movie_genres 
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\r\n'
IGNORE 0 LINES;

-- -----------------------------------------------------
-- Cargar datos: Opiniones
-- -----------------------------------------------------
LOAD DATA INFILE '/var/lib/mysql-files/reviewer.txt'
INTO TABLE reviewer 
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\r\n'
IGNORE 0 LINES;

-- -----------------------------------------------------
-- Cargar datos: Puntaje
-- -----------------------------------------------------
LOAD DATA INFILE '/var/lib/mysql-files/rating.txt'
INTO TABLE rating 
FIELDS TERMINATED BY '|' 
LINES TERMINATED BY '\r\n'
(mov_id, rev_id, rev_stars, num_o_ratings)
IGNORE 0 LINES;