"""
This module provides logic for initializing the database and
running the Item Catalog App project.
"""

from catalog import app
from catalog.database import init_db

if __name__ == '__main__':
    app.secret_key = '$up3r$3cr3tK3y'
    app.debug = True
    init_db()
    # Run the local server
    app.run(host='0.0.0.0', port=5000)
