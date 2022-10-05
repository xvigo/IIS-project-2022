DROP EXTENSION pgcrypto;
CREATE EXTENSION pgcrypto;

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
	id_user INT PRIMARY KEY NOT NULL,
	u_name VARCHAR(50) NOT NULL,
	u_surname VARCHAR(50) NOT NULL,
	u_email TEXT NOT NULL,
	u_password TEXT NOT NULL
);

CREATE TABLE city_manager(
	id_city_manager INT PRIMARY KEY NOT NULL,
	phone_number VARCHAR(50) NOT NULL,
	id_user INT NOT NULL,
	CONSTRAINT user_city_manager FOREIGN KEY (id_user)
		REFERENCES u_user(id_user) ON DELETE CASCADE
);

CREATE TABLE service_technician(
	id_service_technician INT PRIMARY KEY NOT NULL,
	phone_number VARCHAR(50) NOT NULL,
	id_user INT NOT NULL,
	CONSTRAINT user_technician FOREIGN KEY (id_user)
		REFERENCES u_user(id_user) ON DELETE CASCADE
);

CREATE TABLE resident(
	id_resident INT PRIMARY KEY NOT NULL,
	id_user INT NOT NULL,
	CONSTRAINT user_resident FOREIGN KEY (id_user)
		REFERENCES u_user(id_user) ON DELETE CASCADE
);

CREATE TABLE ticket(
	id_ticket INT PRIMARY KEY NOT NULL,
	t_name VARCHAR(50) NOT NULL,
	description TEXT NOT NULL,
	street TEXT NOT NULL,
	house_number INT NOT NULL,
	t_state TEXT NOT NULL,
	id_resident INT NOT NULL,
	CONSTRAINT ticket_resident FOREIGN KEY (id_resident)
		REFERENCES resident(id_resident) ON DELETE CASCADE
);

CREATE TABLE service_requirement(
	id_service_requirement INT PRIMARY KEY NOT NULL,
	description TEXT NOT NULL,
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
	id_ticket_comment INT PRIMARY KEY NOT NULL,
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
	id_image INT PRIMARY KEY NOT NULL,
	i_name VARCHAR(50) NOT NULL,
	i_data TEXT NOT NULL,
	id_ticket INT NOT NULL,
	CONSTRAINT ticket_image FOREIGN KEY (id_ticket)
		REFERENCES ticket(id_ticket) ON DELETE CASCADE
);

/************************** USER **************************/
INSERT INTO
	u_user(id_user, u_name, u_surname, u_email, u_password)
VALUES
	(1, 'Karel', 'Havlíček', 'karel.hav@seznam.cz', crypt('karlovoheslo', gen_salt('bf'))),
	(2, 'Adam', 'Novák', 'adam.novak@seznam.cz', crypt('adamovoheslo', gen_salt('bf'))),
	(3, 'Test1', 'Test1', 'test1@test1.cz', crypt('test1', gen_salt('bf'))),
	(4, 'Test2', 'Test2', 'test2@test2.cz', crypt('test2', gen_salt('bf'))),
	(5, 'Test3', 'Test3', 'test3@test3.cz', crypt('test3', gen_salt('bf')));
	
/************************** CITY MANAGER **************************/
INSERT INTO
	city_manager(id_city_manager, phone_number, id_user)
VALUES
	(1, '111222333', 1);
	
/************************** SERVICE TECHNICIAN **************************/
INSERT INTO
	service_technician(id_service_technician, phone_number, id_user)
VALUES
	(1, '444555666', 2);
	
/************************** RESIDENT **************************/
INSERT INTO
	resident(id_resident, id_user)
VALUES
	(1, 3),
	(2, 4),
	(3, 5);

/************************** TICKET **************************/
INSERT INTO
	ticket(id_ticket, t_name, description, street, house_number, t_state, id_resident)
VALUES
	(1, 'Lampa', 'Lampa nesvítí', 'U Bobra', 12, 'Servisák se na to podívá', 1),
	(2, 'Lampa', 'Lampa až moc svítí', 'U Řeky', 14, 'Servisák se na to nepodívá', 1),
	(3, 'Silnice', 'Špatné značení', 'U Borovičky', 12, 'Servisák na tom pracuje', 2),
	(4, 'Značka', 'Značka byla ukradena', 'U Konvice', 12, 'Servisák na tom pracuje', 3);
	
/************************** IMAGE **************************/
INSERT INTO
	image(id_image, i_name, i_data, id_ticket)
VALUES
	(1, 'Lampa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 1),
	(2, 'Lampa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 2),
	(3, 'Silnice', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 3),
	(4, 'Značka', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png', 4);

/************************** TICKET COMMENT **************************/
INSERT INTO
	ticket_comment(id_ticket_comment, tc_date, tc_text, id_city_manager, id_ticket)
VALUES
	(1, '1996-12-02', 'Dělá se na tom', 1, 1),
	(2, '1996-1-02', 'Dělá se na tom', 1, 2),
	(3, '1996-2-22', 'Dělá se na tom', 1, 3),
	(4, '1996-3-12', 'Dělá se na tom', 1, 4);

/************************** SERVICE REQUIREMENT **************************/
INSERT INTO
	service_requirement(id_service_requirement, description, r_state, estimated_time, price, real_time, id_city_manager, id_service_technician, id_ticket)
VALUES
	(1, 'Chce to víc lepidla pro příště', TRUE, '02:00:00', 5000, '02:00:00', 1, 1, 1),
	(2, 'Snad hotovo', TRUE, '02:00:00', 500, '02:00:00', 1, 1, 2),
	(3, 'Konečně hotovo', TRUE, '20:00:00', 2000, '20:00:00', 1, 1, 3),
	(4, 'Dávám tomu týden', FALSE, '24:00:00', 50000, '00:00:00', 1, 1, 4);

/************************** REQUIREMENT COMMENT **************************/
INSERT INTO
	requirement_comment(id_requirement_comment, rc_date, rc_text, id_service_requirement, id_service_technician)
VALUES
	(1, '1996-12-02', 'Dělá se na tom', 1, 1),
	(2, '1996-1-02', 'Dělá se na tom', 2, 1),
	(3, '1996-2-22', 'Dělá se na tom', 3, 1),
	(4, '1996-3-12', 'Dělá se na tom', 4, 1);

SELECT * FROM u_user WHERE u_password = crypt('karlovoheslo', u_password);
