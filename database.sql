DROP TABLE IF EXISTS user_t CASCADE;
DROP TABLE IF EXISTS manager CASCADE;
DROP TABLE IF EXISTS technician CASCADE;
DROP TABLE IF EXISTS resident CASCADE;
DROP TABLE IF EXISTS service_requirement CASCADE;
DROP TABLE IF EXISTS requirement_comment CASCADE;
DROP TABLE IF EXISTS ticket_comment CASCADE;
DROP TABLE IF EXISTS ticket CASCADE;
DROP TABLE IF EXISTS attached_image CASCADE;
DROP TYPE U_ROLE_ENUM;

CREATE TYPE U_ROLE_ENUM AS ENUM ('admin', 'resident', 'manager', 'technician');
CREATE TABLE user_t(
	id_user SERIAL PRIMARY KEY,

	firstname VARCHAR(50) NOT NULL,
	surname VARCHAR(50) NOT NULL,
	email VARCHAR(254) NOT NULL UNIQUE,
	password_hash VARCHAR(60) NOT NULL,
    u_role U_ROLE_ENUM NOT NULL
);

CREATE TABLE manager(
	id_manager SERIAL PRIMARY KEY,

	phone_number VARCHAR(50),

	id_user INT NOT NULL REFERENCES user_t(id_user) ON DELETE CASCADE
);

CREATE TABLE technician(
	id_technician SERIAL PRIMARY KEY,

	phone_number VARCHAR(50),
	
	id_user INT NOT NULL REFERENCES user_t(id_user) ON DELETE CASCADE,
    id_manager INT NOT NULL REFERENCES manager(id_manager) ON DELETE CASCADE

);

CREATE TABLE resident(
	id_resident SERIAL PRIMARY KEY,

	id_user INT NOT NULL REFERENCES user_t(id_user) ON DELETE CASCADE
);

CREATE TABLE ticket(
	id_ticket SERIAL PRIMARY KEY,

	title VARCHAR(500) NOT NULL,
	content TEXT NOT NULL,
	street VARCHAR(200) NOT NULL,
	house_number INT,
	current_state VARCHAR(200) NOT NULL,
	created_at TIMESTAMP NOT NULL,

	id_resident INT REFERENCES resident(id_resident) ON DELETE SET NULL
);

CREATE TABLE service_requirement(
	id_service_requirement SERIAL PRIMARY KEY,

	content TEXT NOT NULL,
	is_finished BOOLEAN,
	estimated_time INTERVAL,
	real_time INTERVAL,
	price INT,
   	created_at TIMESTAMP NOT NULL,

	id_manager INT NOT NULL,
	id_technician INT,
	id_ticket INT NOT NULL,

	CONSTRAINT fk_manager FOREIGN KEY (id_manager)
		REFERENCES manager(id_manager) ON DELETE CASCADE,
	CONSTRAINT fk_technician FOREIGN KEY (id_technician)
		REFERENCES technician(id_technician) ON DELETE SET NULL,
	CONSTRAINT fk_ticket FOREIGN KEY (id_ticket)
		REFERENCES ticket(id_ticket) ON DELETE CASCADE
);

CREATE TABLE requirement_comment(
	id_requirement_comment SERIAL PRIMARY KEY,

	content TEXT NOT NULL,
	created_at TIMESTAMP NOT NULL,

	id_service_requirement INT NOT NULL,
	id_technician INT NOT NULL,

	CONSTRAINT fk_requirement FOREIGN KEY (id_service_requirement)
		REFERENCES service_requirement(id_service_requirement) ON DELETE CASCADE,
	CONSTRAINT fk_technician FOREIGN KEY (id_technician)
		REFERENCES technician(id_technician) ON DELETE CASCADE
);

CREATE TABLE ticket_comment(
	id_ticket_comment SERIAL PRIMARY KEY,

	content TEXT NOT NULL,
	created_at TIMESTAMP NOT NULL,

	id_manager INT NOT NULL,
	id_ticket INT NOT NULL,

	CONSTRAINT fk_manager FOREIGN KEY (id_manager)
		REFERENCES manager(id_manager) ON DELETE CASCADE,
	CONSTRAINT fk_ticket FOREIGN KEY (id_ticket)
		REFERENCES ticket(id_ticket) ON DELETE CASCADE
);

CREATE TABLE attached_image(
	id_image SERIAL PRIMARY KEY,
	url_path TEXT NOT NULL,

	id_ticket INT NOT NULL REFERENCES ticket(id_ticket) ON DELETE CASCADE
);


/************************** USER **************************/
INSERT INTO
	user_t(firstname, surname, email, u_role, password_hash)
VALUES
	('Admin', 'Administrator', 'admin@test.cz', 'admin', '$2b$12$zwLjku1vkbTi46JnGLbsb.tTHALok7blJZA3g4g8Q8fgIC7UHZ5Oe'),
	('Manager', 'Havlíček',      'manager@test.cz', 'manager','$2b$12$zwLjku1vkbTi46JnGLbsb.tTHALok7blJZA3g4g8Q8fgIC7UHZ5Oe'),
	('Adam',  'Novák',         'adam@mesto.cz',  'manager','$2b$12$aV9aJFHZb8VLPi7DRjp2H.Nk62o1/g0BlhpwBsz6aTLh3rZkRWD7K'),
	('Technik',  'Novotny',       'technician@test.cz', 'technician','$2b$12$vmxa7fyyI9G4SH8j7mupVe3axqWfD99IIHKs6ycOVAypLF01JEO6K'),
	('Resident', 'Test',         'resident@test.cz', 'resident','$2b$12$VPAXc4QCzdpDb1UufEC6qenNML2e6/4j1bTNQuo0eOPChUmpyyyCO'),
	('Ivan',  'Mladek',        'test3@test3.cz', 'resident','$2b$12$3fpZ1xUp0npph3nhRWjmE.uFC8wKmA2pQ7npr9Mtaut8E5cuKJuCu');
	
/************************** CITY MANAGER **************************/
INSERT INTO
	manager(phone_number, id_user)
VALUES
	('559876048', 2),
	('985486652', 3);
	
/************************** SERVICE TECHNICIAN **************************/
INSERT INTO
	technician(phone_number, id_manager, id_user)
VALUES
	('964358721', 1, 4);
	
/************************** RESIDENT **************************/
INSERT INTO
	resident(id_user)
VALUES
	(5),
	(6);

/************************** TICKET **************************/
INSERT INTO
	ticket(title, content, street, house_number, current_state,	created_at,	id_resident)
VALUES
	('Lampa', 	'Lampa nesvítí', 		'U Bobra', 		12,   'Vyreseno',    '2004-11-19 10:23:54', 1),
	('Lampa', 	'Lampa až moc svítí', 	'U Řeky', 		NULL, 'V reseni',    '2005-11-19 10:23:54', 1),
	('Silnice', 'Špatné značení', 		'U Borovičky', 	12,   'Zamitnuto',   '2006-11-19 10:23:54', 2),
	('Značka', 	'Značka byla ukradena', 'U Konvice', 	152,  'Zaevidovano', '2007-11-19 10:23:54', 2);
	
/************************** IMAGE **************************/
INSERT INTO
	attached_image(url_path, id_ticket)
VALUES
	('https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 1),
	('https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 2),
	('https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 3),
	('https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 4);

/************************** TICKET COMMENT **************************/
INSERT INTO
	ticket_comment(created_at, content, id_manager, id_ticket)
VALUES
	('2004-11-19 19:23:54', 'Dělá se na tom', 1, 1),
	('2005-11-19 19:23:54', 'Dělá se na tom', 1, 2),
	('2006-11-19 19:23:54', 'Dělá se na tom', 2, 3),
	('2007-11-19 19:23:54', 'Dělá se na tom', 2, 4);

/************************** SERVICE REQUIREMENT **************************/
INSERT INTO
	service_requirement(content, is_finished, estimated_time, price, real_time, created_at, id_manager, id_technician, id_ticket)
VALUES
	('Opravit lampu',        TRUE,  '02:00:00', 5000, '02:00:00', '2004-12-19 19:23:54', 1, 1, 1),
	('Snizit svit lampy',    TRUE,  '02:00:00', 500,  '02:00:00', '2005-12-19 19:23:54', 1, 1, 2),
	('Vymenit znaceni ',     TRUE,  '20:00:00', 2000, '20:00:00', '2006-12-19 19:23:54', 2, 1, 3),
	('Osadit  novou znacku', FALSE, '24:00:00', NULL, '00:00:00', '2007-12-19 19:23:54', 2, 1, 4);

/************************** REQUIREMENT COMMENT **************************/
INSERT INTO
	requirement_comment(created_at, content, id_service_requirement, id_technician)
VALUES
	('2004-12-25 19:23:54', 'Dělá se na tom', 1, 1),
	('2005-12-25 19:23:54', 'Dělá se na tom', 2, 1),
	('2006-12-25 19:23:54', 'Dělá se na tom', 3, 1),
	('2007-12-25 19:23:54', 'Dělá se na tom', 4, 1);

