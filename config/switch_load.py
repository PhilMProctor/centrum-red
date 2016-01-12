#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('../db/centrum.db')
print "Opened database successfully";

conn.execute("INSERT INTO SWITCH_SETTINGS (id,name,description,location,cat,setting_num,setting_rnum,switch_on,switch_off,active,power)\
	VALUES (1,'Switch One','Lounge Lamp','Lounge','Light',1,1,'A',1,0,0)");

conn.execute("INSERT INTO SWITCH_SETTINGS (id,name,description,location,cat,setting_num,setting_rnum,switch_on,switch_off,active,power)\
	VALUES (2,'Switch Two','Xmas Lights','Lounge','Light',1,2,'B',2,0,0)");

conn.execute("INSERT INTO SWITCH_SETTINGS (id,name,description,location,cat,setting_num,setting_rnum,switch_on,switch_off,active,power)\
	VALUES (3,'Switch Three',' ','Lounge','Light',1,3,'C',3,0,0)");

conn.execute("INSERT INTO SWITCH_SETTINGS (id,name,description,location,cat,setting_num,setting_rnum,switch_on,switch_off,active,power)\
	VALUES (4,'Switch Four',' ','Lounge','Light',1,4,'D',4,0,0)");

conn.execute("INSERT INTO SWITCH_SETTINGS (id,name,description,location,cat,setting_num,setting_rnum,switch_on,switch_off,active,power)\
	VALUES (5,'Switch Five',' ','Lounge','Light',2,1,'E',5,0,0)");

conn.execute("INSERT INTO SWITCH_SETTINGS (id,name,description,location,cat,setting_num,setting_rnum,switch_on,switch_off,active,power)\
	VALUES (6,'Switch Six',' ','Lounge','Light',2,2,'F',6,0,0)");

conn.execute("INSERT INTO SWITCH_SETTINGS (id,name,description,location,cat,setting_num,setting_rnum,switch_on,switch_off,active,power)\
	VALUES (7,'Switch Seven',' ','Lounge','Light',2,3,'G',7,0,0)");

conn.execute("INSERT INTO SWITCH_SETTINGS (id,name,description,location,cat,setting_num,setting_rnum,switch_on,switch_off,active,power)\
	VALUES (8,'Switch Eight',' ','Lounge','Light',2,4,'H',8,0,0)");

conn.commit()
print "Records created successfully";
conn.close()
