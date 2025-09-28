-- init.sql
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE
);

INSERT INTO tasks (description, completed) VALUES 
('Learn Docker', false),
('Build a Flask app', true)
ON CONFLICT DO NOTHING;
