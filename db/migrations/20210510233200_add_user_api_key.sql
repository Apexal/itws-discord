-- migrate:up
ALTER TABLE users ADD COLUMN api_key VARCHAR;

-- migrate:down

ALTER TABLE users DROP COLUMN api_key;