BEGIN TRANSACTION;
CREATE TABLE switch_settings (id INTEGER PRIMARY KEY, name TEXT, description TEXT, location TEXT, cat TEXT, setting_num NUMERIC, setting_rnum NUMERIC, switch_on NUMERIC, switch_off TEXT, active NUMERIC, power NUMERIC);
COMMIT;
