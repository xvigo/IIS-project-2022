DROP EXTENSION pgcrypto;
CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS uživatel CASCADE;
DROP TABLE IF EXISTS správce_města CASCADE;
DROP TABLE IF EXISTS servisní_technik CASCADE;
DROP TABLE IF EXISTS obyvatel CASCADE;
DROP TABLE IF EXISTS servisní_požadavek CASCADE;
DROP TABLE IF EXISTS komentář_požadavku CASCADE;
DROP TABLE IF EXISTS komentář_tiketu CASCADE;
DROP TABLE IF EXISTS tiket CASCADE;
DROP TABLE IF EXISTS obrázek CASCADE;

CREATE TABLE users(
	id_user SERIAL PRIMARY KEY NOT NULL,
	name VARCHAR(50) NOT NULL,
	surname VARCHAR(50) NOT NULL,
	email VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL
);

CREATE TABLE správce_města(
	id_správce INT PRIMARY KEY NOT NULL,
	telefon VARCHAR(20) NOT NULL,
	id_uživatel INT NOT NULL,
	CONSTRAINT uživatel_správce FOREIGN KEY (id_uživatel)
		REFERENCES uživatel(id_uživatel) ON DELETE CASCADE
);

CREATE TABLE servisní_technik(
	id_technik INT PRIMARY KEY NOT NULL,
	telefon VARCHAR(50) NOT NULL,
	id_uživatel INT NOT NULL,
	CONSTRAINT uživatel_technik FOREIGN KEY (id_uživatel)
		REFERENCES uživatel(id_uživatel) ON DELETE CASCADE
);

CREATE TABLE obyvatel(
	id_obyvatel INT PRIMARY KEY NOT NULL,
	id_uživatel INT NOT NULL,
	CONSTRAINT uživatel_obyvatel FOREIGN KEY (id_uživatel)
		REFERENCES uživatel(id_uživatel) ON DELETE CASCADE
);

CREATE TABLE tiket(
	id_tiket INT PRIMARY KEY NOT NULL,
	název VARCHAR(50) NOT NULL,
	popis TEXT NOT NULL,
	ulice TEXT NOT NULL,
	číslo_popisné INT NOT NULL,
	stav TEXT NOT NULL,
	id_obyvatel INT NOT NULL,
	CONSTRAINT tiket_obyvatel FOREIGN KEY (id_obyvatel)
		REFERENCES obyvatel(id_obyvatel) ON DELETE CASCADE
);

CREATE TABLE servisní_požadavek(
	id_požadavek INT PRIMARY KEY NOT NULL,
	popis TEXT NOT NULL,
	stav_řešení BOOLEAN DEFAULT FALSE,
	předpokládaný_čas TIME NOT NULL,
	cena INT NOT NULL,
	vykázaný_čas TIME NOT NULL,
	id_správce INT NOT NULL,
	id_technik INT NOT NULL,
	id_tiket INT NOT NULL,
	CONSTRAINT požadavek_správce FOREIGN KEY (id_správce)
		REFERENCES správce_města(id_správce) ON DELETE CASCADE,
	CONSTRAINT požadavek_technik FOREIGN KEY (id_technik)
		REFERENCES servisní_technik(id_technik) ON DELETE CASCADE,
	CONSTRAINT požadavek_tiket FOREIGN KEY (id_tiket)
		REFERENCES tiket(id_tiket) ON DELETE CASCADE
);

CREATE TABLE komentář_požadavku(
	id_komentář_požadavek SERIAL PRIMARY KEY NOT NULL,
	datum DATE NOT NULL,
	k_text TEXT NOT NULL,
	id_požadavek INT NOT NULL,
	id_technik INT NOT NULL,
	CONSTRAINT komentář_požadavek FOREIGN KEY (id_požadavek)
		REFERENCES servisní_požadavek(id_požadavek) ON DELETE CASCADE,
	CONSTRAINT komentář_technik FOREIGN KEY (id_technik)
		REFERENCES servisní_technik(id_technik) ON DELETE CASCADE
);

CREATE TABLE komentář_tiketu(
	id_komentář_tiket INT PRIMARY KEY NOT NULL,
	datum DATE NOT NULL,
	k_text TEXT NOT NULL,
	id_správce INT NOT NULL,
	id_tiket INT NOT NULL,
	CONSTRAINT komentář_správce FOREIGN KEY (id_správce)
		REFERENCES správce_města(id_správce) ON DELETE CASCADE,
	CONSTRAINT komentář_tiket FOREIGN KEY (id_tiket)
		REFERENCES tiket(id_tiket) ON DELETE CASCADE
);

CREATE TABLE obrázek(
	id_obrázek INT PRIMARY KEY NOT NULL,
	název VARCHAR(50) NOT NULL,
	o_data TEXT NOT NULL,
	id_tiket INT NOT NULL,
	CONSTRAINT tiket_obrázek FOREIGN KEY (id_tiket)
		REFERENCES tiket(id_tiket) ON DELETE CASCADE
);

/************************** UŽIVATEL **************************/
INSERT INTO
	uživatel(id_uživatel, jméno, příjmení, email, heslo)
VALUES
	(1, 'Karel', 'Havlíček', 'karel.hav@seznam.cz', crypt('karlovoheslo', gen_salt('bf'))),
	(2, 'Adam', 'Novák', 'adam.novak@seznam.cz', crypt('adamovoheslo', gen_salt('bf'))),
	(3, 'Test1', 'Test1', 'test1@test1.cz', crypt('test1', gen_salt('bf'))),
	(4, 'Test2', 'Test2', 'test2@test2.cz', crypt('test2', gen_salt('bf'))),
	(5, 'Test3', 'Test3', 'test3@test3.cz', crypt('test3', gen_salt('bf')));
	
/************************** SPRÁVCE **************************/
INSERT INTO
	správce_města(id_správce, telefon, id_uživatel)
VALUES
	(1, '111222333', 1);
	
/************************** TECHNIK **************************/
INSERT INTO
	servisní_technik(id_technik, telefon, id_uživatel)
VALUES
	(1, '444555666', 2);
	
/************************** OBYVATEL **************************/
INSERT INTO
	obyvatel(id_obyvatel, id_uživatel)
VALUES
	(1, 3),
	(2, 4),
	(3, 5);

/************************** TIKET **************************/
INSERT INTO
	tiket(id_tiket, název, popis, ulice, číslo_popisné, stav, id_obyvatel)
VALUES
	(1, 'Lampa', 'Lampa nesvítí', 'U Bobra', 12, 'Servisák se na to podívá', 1),
	(2, 'Lampa', 'Lampa až moc svítí', 'U Řeky', 14, 'Servisák se na to nepodívá', 1),
	(3, 'Silnice', 'Špatné značení', 'U Borovičky', 12, 'Servisák na tom pracuje', 2),
	(4, 'Značka', 'Značka byla ukradena', 'U Konvice', 12, 'Servisák na tom pracuje', 3);
	
/************************** OBRÁZEK **************************/
INSERT INTO
	obrázek(id_obrázek, název, o_data, id_tiket)
VALUES
	(1, 'Lampa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 1),
	(2, 'Lampa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 2),
	(3, 'Silnice', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 3),
	(4, 'Značka', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 4);

/************************** KOMENTÁŘ TIKETU **************************/
INSERT INTO
	komentář_tiketu(id_komentář_tiket, datum, k_text, id_správce, id_tiket)
VALUES
	(1, '1996-12-02', 'Dělá se na tom', 1, 1),
	(2, '1996-1-02', 'Dělá se na tom', 1, 2),
	(3, '1996-2-22', 'Dělá se na tom', 1, 3),
	(4, '1996-3-12', 'Dělá se na tom', 1, 4);

/************************** SERVISNÍ POŽADAVEK **************************/
INSERT INTO
	servisní_požadavek(id_požadavek, popis, stav_řešení, předpokládaný_čas, cena, vykázaný_čas, id_správce, id_technik, id_tiket)
VALUES
	(1, 'Chce to víc lepidla pro příště', TRUE, '02:00:00', 5000, '02:00:00', 1, 1, 1),
	(2, 'Snad hotovo', TRUE, '02:00:00', 500, '02:00:00', 1, 1, 2),
	(3, 'Konečně hotovo', TRUE, '20:00:00', 2000, '20:00:00', 1, 1, 3),
	(4, 'Dávám tomu týden', FALSE, '24:00:00', 50000, '00:00:00', 1, 1, 4);

/************************** KOMENTÁŘ POŽADAVKU **************************/
INSERT INTO
	komentář_požadavku(id_komentář_požadavek, datum, k_text, id_požadavek, id_technik)
VALUES
	(1, '1996-12-02', 'Dělá se na tom', 1, 1),
	(2, '1996-1-02', 'Dělá se na tom', 2, 1),
	(3, '1996-2-22', 'Dělá se na tom', 3, 1),
	(4, '1996-3-12', 'Dělá se na tom', 4, 1);

SELECT * FROM uživatel WHERE heslo = crypt('karlovoheslo', heslo);
