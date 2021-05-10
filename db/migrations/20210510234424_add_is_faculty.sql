-- migrate:up
ALTER TABLE users ADD COLUMN is_faculty BOOLEAN DEFAULT false;

-- migrate:down

ALTER TABLE users DROP COLUMN is_faculty;