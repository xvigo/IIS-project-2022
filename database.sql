DROP TABLE IF EXISTS user_t CASCADE;
DROP TABLE IF EXISTS manager CASCADE;
DROP TABLE IF EXISTS technician CASCADE;
DROP TABLE IF EXISTS resident CASCADE;
DROP TABLE IF EXISTS service_request CASCADE;
DROP TABLE IF EXISTS request_comment CASCADE;
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
    
    id_user INT NOT NULL REFERENCES user_t(id_user) ON DELETE CASCADE
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
    created_at TIMESTAMP DEFAULT NOW(),

    id_resident INT REFERENCES resident(id_resident) ON DELETE SET NULL
);

CREATE TABLE service_request(
    id_service_request SERIAL PRIMARY KEY,

    content TEXT NOT NULL,
    is_finished BOOLEAN,
    estimated_time DATE,
    real_time DATE,
    price INT,
    created_at TIMESTAMP DEFAULT NOW(),

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

CREATE TABLE request_comment(
    id_request_comment SERIAL PRIMARY KEY,

    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

    id_service_request INT NOT NULL,
    id_technician INT NOT NULL,

    CONSTRAINT fk_request FOREIGN KEY (id_service_request)
        REFERENCES service_request(id_service_request) ON DELETE CASCADE,
    CONSTRAINT fk_technician FOREIGN KEY (id_technician)
        REFERENCES technician(id_technician) ON DELETE CASCADE
);

CREATE TABLE ticket_comment(
    id_ticket_comment SERIAL PRIMARY KEY,

    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

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
    ('Admin',  'Admin',      'admin@auto.cz',       'admin',      '$2b$12$zwLjku1vkbTi46JnGLbsb.tTHALok7blJZA3g4g8Q8fgIC7UHZ5Oe'),
    ('First',  'Manager',    'manager1@auto.cz',    'manager',    '$2b$12$zwLjku1vkbTi46JnGLbsb.tTHALok7blJZA3g4g8Q8fgIC7UHZ5Oe'),
    ('Second', 'Manager',    'manager2@auto.cz',    'manager',    '$2b$12$aV9aJFHZb8VLPi7DRjp2H.Nk62o1/g0BlhpwBsz6aTLh3rZkRWD7K'),
    ('First',  'Technician', 'technician1@auto.cz', 'technician', '$2b$12$vmxa7fyyI9G4SH8j7mupVe3axqWfD99IIHKs6ycOVAypLF01JEO6K'),
    ('Second', 'Technician', 'technician2@auto.cz', 'technician', '$2b$12$vmxa7fyyI9G4SH8j7mupVe3axqWfD99IIHKs6ycOVAypLF01JEO6K'),
    ('First',  'Resident',   'resident1@auto.cz',   'resident',   '$2b$12$VPAXc4QCzdpDb1UufEC6qenNML2e6/4j1bTNQuo0eOPChUmpyyyCO'),
    ('Second', 'Resident',   'resident2@auto.cz',   'resident',   '$2b$12$3fpZ1xUp0npph3nhRWjmE.uFC8wKmA2pQ7npr9Mtaut8E5cuKJuCu');
    
/************************** CITY MANAGER **************************/
INSERT INTO
    manager(phone_number, id_user)
VALUES
    ('123456789', 2),
    ('987654321', 3);
    
/************************** SERVICE TECHNICIAN **************************/
INSERT INTO
    technician(phone_number, id_user)
VALUES
    ('333444555', 4),
    ('666777888', 5);

    
/************************** RESIDENT **************************/
INSERT INTO
    resident(id_user)
VALUES
    (6),
    (7);

/************************** TICKET **************************/
INSERT INTO
    ticket(title, content, street, house_number, current_state,	created_at,	id_resident)
VALUES
    ('Broken lamp', 'The lamp on in front of the Semilasso bus stop is not lightning. It is really scary to be here at night. Please fix it as soon as posible.', 'Kosmova', 3016, 'Finished', '2004-11-19 10:23:54', 1),
    ('Lamp issue', 'The lamp is too bright, we can not sleep at night.', 'Zilkova', 113, 'In process', '2005-11-19 10:23:54', 2),
    ('Road is in bad condition', 'There is a dangerous hole in the middle of the road. Someone could get seriously injured.', 'Bozetechova', 1, 'Denied','2006-11-19 10:23:54', 1),
    ('Missing road sign', 'The road sign marking priority road was stolen.', 'Tumova', 2256, 'Accepted', '2007-11-19 10:23:54', 2);
    
/************************** IMAGE **************************/
INSERT INTO
    attached_image(url_path, id_ticket)
VALUES
    ('/static/ticket_pics/8cd4255ddb3184a5.png', 1),
    ('/static/ticket_pics/52dc7258209a56b4.jpg', 2),
    ('/static/ticket_pics/1ef64478b0d1cf65.png', 3);

/************************** TICKET COMMENT **************************/
INSERT INTO
    ticket_comment(created_at, content, id_manager, id_ticket)
VALUES
    ('2004-11-19 19:23:54', 'The issue was reported to a technician, it should be repaired by the end of the next week.', 1, 1),
    ('2004-11-25 19:23:54', 'Technician replaced the light bulb and the lamp is now working.', 1, 1),
    ('2004-11-25 19:23:54', 'The issue was forwarded to an expert, which will check the brightness level of the lamp.', 1, 2),
    ('2006-11-19 19:23:54', 'This road is still in a good shape, there is no need to repair it yet.', 2, 3);

/************************** SERVICE REQUEST **************************/
INSERT INTO
    service_request(content, is_finished, estimated_time, price, real_time, created_at, id_manager, id_technician, id_ticket)
VALUES
    ('Repair the lamp.', TRUE,  '2004-10-15', 5000, '2004-10-15', '2004-12-19 19:23:54', 1, 1, 1),
    ('Please look at the brightness level of the lamp and reduce it if necessary.', FALSE, '2020-12-19 19:23:54', NULL, NULL, '2005-12-19 19:23:54', 2, 2, 2);

/************************** REQUEST COMMENT **************************/
INSERT INTO
    request_comment(created_at, content, id_service_request, id_technician)
VALUES
    ('2004-12-25 19:23:54', 'I am now full, i will look at it next week.', 1, 1),
    ('2004-12-25 19:23:54', 'Lamp repaired, I just had to replace the light bulb.', 1, 1);
