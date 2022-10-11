DROP TABLE IF EXISTS u_user CASCADE;
DROP TABLE IF EXISTS city_manager CASCADE;
DROP TABLE IF EXISTS service_technician CASCADE;
DROP TABLE IF EXISTS resident CASCADE;
DROP TABLE IF EXISTS service_requirement CASCADE;
DROP TABLE IF EXISTS requirement_comment CASCADE;
DROP TABLE IF EXISTS ticket_comment CASCADE;
DROP TABLE IF EXISTS ticket CASCADE;
DROP TABLE IF EXISTS image CASCADE;

CREATE TABLE u_user(
	id_user SERIAL PRIMARY KEY NOT NULL,
	u_name VARCHAR(50) NOT NULL,
	u_surname VARCHAR(50) NOT NULL,
	u_email VARCHAR(254) NOT NULL,
	u_password VARCHAR(60) NOT NULL
);

CREATE TABLE city_manager(
	id_city_manager SERIAL PRIMARY KEY NOT NULL,
	phone_number VARCHAR(50) NOT NULL,
	id_user INT NOT NULL,
	CONSTRAINT user_city_manager FOREIGN KEY (id_user)
		REFERENCES u_user(id_user) ON DELETE CASCADE
);

CREATE TABLE service_technician(
	id_service_technician SERIAL PRIMARY KEY NOT NULL,
	phone_number VARCHAR(50) NOT NULL,
	id_user INT NOT NULL,
	CONSTRAINT user_technician FOREIGN KEY (id_user)
		REFERENCES u_user(id_user) ON DELETE CASCADE
);

CREATE TABLE resident(
	id_resident SERIAL PRIMARY KEY NOT NULL,
	id_user INT NOT NULL,
	CONSTRAINT user_resident FOREIGN KEY (id_user)
		REFERENCES u_user(id_user) ON DELETE CASCADE
);

CREATE TABLE ticket(
	id_ticket SERIAL PRIMARY KEY NOT NULL,
	title VARCHAR(50) NOT NULL,
	t_description TEXT NOT NULL,
	street TEXT NOT NULL,
	house_number INT NOT NULL,
	t_state TEXT NOT NULL,
	id_user INT NOT NULL,
	datetime_created TIMESTAMP NOT NULL,
	CONSTRAINT ticket_resident FOREIGN KEY (id_user)
		REFERENCES u_user(id_user) ON DELETE CASCADE
);

CREATE TABLE service_requirement(
	id_service_requirement SERIAL PRIMARY KEY NOT NULL,
	r_description TEXT NOT NULL,
	r_state BOOLEAN DEFAULT FALSE,
	estimated_time TIME NOT NULL,
	price INT NOT NULL,
	real_time TIME NOT NULL,
	id_city_manager INT NOT NULL,
	id_service_technician INT NOT NULL,
	id_ticket INT NOT NULL,
	CONSTRAINT requirement_city_manager FOREIGN KEY (id_city_manager)
		REFERENCES city_manager(id_city_manager) ON DELETE CASCADE,
	CONSTRAINT requirement_technician FOREIGN KEY (id_service_technician)
		REFERENCES service_technician(id_service_technician) ON DELETE CASCADE,
	CONSTRAINT requirement_ticket FOREIGN KEY (id_ticket)
		REFERENCES ticket(id_ticket) ON DELETE CASCADE
);

CREATE TABLE requirement_comment(
	id_requirement_comment SERIAL PRIMARY KEY NOT NULL,
	rc_date DATE NOT NULL,
	rc_text TEXT NOT NULL,
	id_service_requirement INT NOT NULL,
	id_service_technician INT NOT NULL,
	CONSTRAINT requirement_comment_requirement FOREIGN KEY (id_service_requirement)
		REFERENCES service_requirement(id_service_requirement) ON DELETE CASCADE,
	CONSTRAINT requirement_comment_technik FOREIGN KEY (id_service_technician)
		REFERENCES service_technician(id_service_technician) ON DELETE CASCADE
);

CREATE TABLE ticket_comment(
	id_ticket_comment SERIAL PRIMARY KEY NOT NULL,
	tc_date DATE NOT NULL,
	tc_text TEXT NOT NULL,
	id_city_manager INT NOT NULL,
	id_ticket INT NOT NULL,
	CONSTRAINT comment_city_manager FOREIGN KEY (id_city_manager)
		REFERENCES city_manager(id_city_manager) ON DELETE CASCADE,
	CONSTRAINT comment_ticket FOREIGN KEY (id_ticket)
		REFERENCES ticket(id_ticket) ON DELETE CASCADE
);

CREATE TABLE image(
	id_image SERIAL PRIMARY KEY NOT NULL,
	i_name VARCHAR(50) NOT NULL,
	i_data TEXT NOT NULL,
	id_ticket INT NOT NULL,
	CONSTRAINT ticket_image FOREIGN KEY (id_ticket)
		REFERENCES ticket(id_ticket) ON DELETE CASCADE
);

/************************** USER (hashed passwords: heslo)**************************/
INSERT INTO
	u_user(u_name, u_surname, u_email, u_password)
VALUES
	('Karel', 'Havlíček', 'karel.hav@seznam.cz', '$2b$12$zwLjku1vkbTi46JnGLbsb.tTHALok7blJZA3g4g8Q8fgIC7UHZ5Oe'),
	('Adam', 'Novák', 'adam.novak@seznam.cz', '$2b$12$aV9aJFHZb8VLPi7DRjp2H.Nk62o1/g0BlhpwBsz6aTLh3rZkRWD7K'),
	('Test1', 'Test1', 'test1@test1.cz', '$2b$12$vmxa7fyyI9G4SH8j7mupVe3axqWfD99IIHKs6ycOVAypLF01JEO6K'),
	('Test2', 'Test2', 'test2@test2.cz', '$2b$12$VPAXc4QCzdpDb1UufEC6qenNML2e6/4j1bTNQuo0eOPChUmpyyyCO'),
	('Test3', 'Test3', 'test3@test3.cz', '$2b$12$3fpZ1xUp0npph3nhRWjmE.uFC8wKmA2pQ7npr9Mtaut8E5cuKJuCu');
	
/************************** CITY MANAGER **************************/
INSERT INTO
	city_manager(phone_number, id_user)
VALUES
	('111222333', 1);
	
/************************** SERVICE TECHNICIAN **************************/
INSERT INTO
	service_technician(phone_number, id_user)
VALUES
	('444555666', 2);
	
/************************** RESIDENT **************************/
INSERT INTO
	resident(id_resident, id_user)
VALUES
	(1, 3),
	(2, 4),
	(3, 5);

/************************** TICKET **************************/
INSERT INTO
	ticket(title, t_description, street, house_number, t_state, datetime_created, id_user)
VALUES
	('Lampa', 'Lampa nesvítí', 'U Bobra', 12, 'Servisák se na to podívá', '2004-11-19 10:23:54', 3),
	('Lampa', 'Lampa až moc svítí', 'U Řeky', 14, 'Servisák se na to nepodívá', '2005-11-19 10:23:54', 3),
	('Silnice', 'Špatné značení', 'U Borovičky', 12, 'Servisák na tom pracuje', '2006-11-19 10:23:54', 4),
	('Značka', 'Značka byla ukradena', 'U Konvice', 12, 'Servisák na tom pracuje', '2007-11-19 10:23:54', 5);
	
/************************** IMAGE **************************/
INSERT INTO
	image(i_name, i_data, id_ticket)
VALUES
	('Lampa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 1),
	('Lampa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 2),
	('Silnice', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 3),
	('Značka', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 4);

/************************** TICKET COMMENT **************************/
INSERT INTO
	ticket_comment(tc_date, tc_text, id_city_manager, id_ticket)
VALUES
	('1996-12-02', 'Dělá se na tom', 1, 1),
	('1996-1-02', 'Dělá se na tom', 1, 2),
	('1996-2-22', 'Dělá se na tom', 1, 3),
	('1996-3-12', 'Dělá se na tom', 1, 4);

/************************** SERVICE REQUIREMENT **************************/
INSERT INTO
	service_requirement(r_description, r_state, estimated_time, price, real_time, id_city_manager, id_service_technician, id_ticket)
VALUES
	('Chce to víc lepidla pro příště', TRUE, '02:00:00', 5000, '02:00:00', 1, 1, 1),
	('Snad hotovo', TRUE, '02:00:00', 500, '02:00:00', 1, 1, 2),
	('Konečně hotovo', TRUE, '20:00:00', 2000, '20:00:00', 1, 1, 3),
	('Dávám tomu týden', FALSE, '24:00:00', 50000, '00:00:00', 1, 1, 4);

/************************** REQUIREMENT COMMENT **************************/
INSERT INTO
	requirement_comment(rc_date, rc_text, id_service_requirement, id_service_technician)
VALUES
	('1996-12-02', 'Dělá se na tom', 1, 1),
	('1996-1-02', 'Dělá se na tom', 2, 1),
	('1996-2-22', 'Dělá se na tom', 3, 1),
	('1996-3-12', 'Dělá se na tom', 4, 1);
