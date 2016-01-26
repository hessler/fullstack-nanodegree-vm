from flask import Flask
app = Flask(__name__)

import catalog.views
from catalog.database import db_session

# To use SQLAlchemy in a declarative way with an application, have to
# put this code into application module. Flask will automatically remove
# database sessions at the end of the request or when the app shuts down.
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
