USE fittrack;

DROP TABLE IF EXISTS meal_logs;
DROP TABLE IF EXISTS weight_logs;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100) NOT NULL,
  sexe ENUM('F','M','X') NOT NULL,
  date_naissance DATE NOT NULL,
  taille_m DECIMAL(4,2) NOT NULL
);

CREATE TABLE weight_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  date_log DATE NOT NULL,
  poids_kg DECIMAL(5,2) NOT NULL,
  imc DECIMAL(5,2) NOT NULL,
  categorie_imc VARCHAR(30) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE meal_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  date_log DATE NOT NULL,
  type_repas VARCHAR(30) NOT NULL,
  calories INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);


INSERT INTO users (nom, prenom, sexe, date_naissance, taille_m)
VALUES ('Demo', 'Alice', 'F', '2000-05-12', 1.65);


INSERT INTO weight_logs (user_id, date_log, poids_kg, imc, categorie_imc) VALUES
(1,'2025-03-01',72.0, 26.45,'surpoids'),
(1,'2025-04-01',70.5, 25.90,'surpoids'),
(1,'2025-05-01',69.0, 25.34,'surpoids');


INSERT INTO meal_logs (user_id, date_log, type_repas, calories) VALUES
(1,'2025-03-01','petit_dej',350),
(1,'2025-03-01','dejeuner',650),
(1,'2025-03-01','diner',700),
(1,'2025-04-01','dejeuner',600),
(1,'2025-05-01','diner',750);
