from flask.views import View
from flask import render_template

class Home_View(View):
    def dispatch_request(self):
        return render_template('index.html')
