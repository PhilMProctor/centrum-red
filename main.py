# import Jinja2
import os
import jinja2

# import Tornado
import tornado.ioloop
import tornado.web
import bcrypt
import unicodedata

# Controller Config
sPORT ='/dev/ttyACM0'
import sys
import serial
import time

# Database Connectivity
import models

# Load template
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'views')
static_path = os.path.join(os.path.dirname(__file__), "static")
jinja_environment = \
    jinja2.Environment(autoescape=True, extensions=['jinja2.ext.autoescape'], loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

class BaseHandler(tornado.web.RequestHandler):
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.write(template.render(template_values))

    def get_current_user(self):
        user_id = self.get_secure_cookie("hms")
        if not user_id: return None
        return models.conn.execute("SELECT * FROM users WHERE id = %s", int(user_id))

# Main page Handlers

# Main Page
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)
        self.render_template('index.html', params)

class AuthLoginHandler(BaseHandler):
    def get (self):
        error = ""
        params = {
        'error': error
        }
        self.render_template('login.html', params)

    def post(self):
        admin = models.conn.execute("SELECT * FROM users WHERE username = %s",
            self.get_argument("username"))
        if not admin:
            self.render_template("login.html", error="login error")
        return
        hashed_password = yield executor.submit(
            bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
            tornado.escape.utf8(admin.hashed_password))
        if hashed_password == admin.hashed_password:
            self.set_secure_cookie("hms", str(author.id))
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render_template("login.html", error="incorrect password")
		
		

# Lights Page
class LightsHandler(BaseHandler):
    def get(self):
        cursor = models.conn.execute("SELECT id,\
        name, description, location, switch_on,\
        switch_off, state from switch_settings where cat='Light' and state = 1")
        params = {
        'cursor': cursor,
        }
        self.render_template('lights.html', params)
    def post(self):
        switch_ctl = self.get_argument('switch_action')
        ser = serial.Serial(sPORT, 9600)
        time.sleep(1.5)
        ser.write(switch_ctl)
        ser.close()
        self.redirect('/lights')

# Power Page
class PowerHandler(BaseHandler):
    def get(self):
        cursor = models.conn.execute("SELECT id,\
            name, description, location, switch_on,\
            switch_off, state from switch_settings where cat='Power' and state = 1")
        params = {
        'cursor': cursor,
        }
        self.render_template('power.html', params)

    def post(self):
        switch_ctl = self.get_argument('switch_action')
        ser = serial.Serial(sPORT, 9600)
        time.sleep(1.5)
        ser.write(switch_ctl)
        ser.close()
        self.redirect('/power')

# Monitor Page
class MonitorHandler(BaseHandler):
    def get(self):
        active_home = ""
        active_settings = ""
        params = {
        'active_home': active_home,
        'active_settings': active_settings
        }
        self.render_template('monitor.html', params)

		# Monitor Page
class SwitchSetHandler(BaseHandler):
    def get(self):
		# Extracts the switch values <switch_vals> from the database and loads the page
        switchset = models.conn.execute("SELECT id,\
            name, description, location, cat, switch_on,\
            switch_off, active from switch_settings where cat='Light'")
        params = {
        'switchset': switchset,
        }
        self.render_template('switchset.html', params)

    def post(self):
		# Posts the switch ID to the SwitchEditHandler class via the edit page
        switch_ctl = self.get_argument('switchID')
        self.redirect('/sEdit' + '?switchID=' + switch_ctl)

class SwitchEditHandler(BaseHandler):
    def get(self):
		# Selects the switch details from the database which have the ID of <switch_ctl>
        switch_ctl = self.get_argument('switchID')
        switchVals = models.conn.execute("SELECT * from switch_settings where id = %s" %switch_ctl)
        params = {
        'switchVals': switchVals,
        }
        self.render_template('edit.html', params)

    def post(self):
		# Builds a update statement for sqlite
        switchID = self.get_argument('switchID')
        switchName = self.get_argument('switchName')
        switchDesc = self.get_argument('description')
        switchLoc = self.get_argument('location')
        switchCat = self.get_argument('cat')
        switchSetNum = self.get_argument('switchNum')
        switchSetRnum = self.get_argument('switchRnum')
        switchOn = self.get_argument('switchOn')
        switchOff = self.get_argument('switchOff')
        #switchActive = self.get_argument('active')
		#switchPower = self.get_argument('power')
        cursor = models.conn.execute("UPDATE switch_settings SET name = %s, description = %s, \
            location = %s, cat = %s, setting_num = %s, setting_rnum = %s WHERE id = %s" % \
            ("'" + switchName + "'", "'"+switchDesc+"'", "'"+switchLoc+"'", "'"+switchCat+"'", "'"+switchSetNum+"'", "'"+switchSetRnum+"'", "'"+switchID+"'"))
        models.conn.commit()
        self.redirect(switchCat)

settings = {'debug': True,
'cookie_secret':"fesdkodkokewqkdwqpkd",
'login_url':'/login'}

handlers = [(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
    (r'/', MainHandler),
    (r'/lights', LightsHandler),
    (r'/power', PowerHandler),
    (r'/switchset', SwitchSetHandler),
    (r'/sEdit', SwitchEditHandler),
    (r'/login', AuthLoginHandler),
]

application = tornado.web.Application(handlers, **settings)

PORT=8888
if __name__ == "__main__":
    # Setup the server
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
