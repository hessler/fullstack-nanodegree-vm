"""
This module provides views for the Item Catalog App project.
"""

#pylint: disable=import-error,no-member,unused-variable

from flask import Markup #, Flask
from flask import flash, jsonify, make_response
from flask import redirect, render_template, request, url_for

from flask import session as login_session

from catalog import app
from catalog.models import Category, CategoryItem, User
from catalog.database import db_session #, get_or_create
from catalog.database import db_get_all_objects_of_type, db_get_last_x_items_of_type, db_get_all_items

from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials
from oauth2client.client import FlowExchangeError

from sqlalchemy.orm.exc import NoResultFound

import httplib2, json, random, requests, string, urllib

FACEBOOK_JSON = 'catalog/client_secrets_facebook.json'
GOOGLE_JSON = 'catalog/client_secrets_google.json'
CLIENT_ID_GOOGLE = json.loads(open(GOOGLE_JSON, 'r').read())['web']['client_id']
APP_ID_FACEBOOK = json.loads(open(FACEBOOK_JSON, 'r').read())['web']['app_id']
APP_SECRET_FACEBOOK = json.loads(open(FACEBOOK_JSON, 'r').read())['web']['app_secret']
APPLICATION_NAME = 'Catalog App'


#-----------------------------------------------------------------------
# Views
#-----------------------------------------------------------------------

# Main page
@app.route('/')
@app.route('/catalog/')
def index():
    """
    Function to return a page listing all categories and most recent items.
    """

    categories = db_get_all_objects_of_type(Category)
    latest_items = db_get_last_x_items_of_type(5, CategoryItem)
    user = get_user()
    items = db_get_all_items()

    return render_template('home.html',
                           categories=categories,
                           items=items,
                           latest_items=latest_items,
                           user=user)

# Category Information
@app.route('/catalog/category/<int:category_id>/')
def category_info(category_id):
    """
    Function to return a page to view items for specified category.

    Args:
        category_id: ID value of the category to view.
    """

    # Retrieve Category object for template rendering.
    # If not found, render error template.
    category = db_session.query(Category)\
        .filter_by(id=category_id)\
        .first()
    if not category:
        return render_template('error.html',
                               headline_text='Category Not Found',
                               error_text='The specified category was not found.')

    login_session['last_category_id'] = category.id
    category_items = db_session.query(CategoryItem).filter_by(category_id=category.id).all()
    creator = category.user
    user = get_user()

    return render_template('category_info.html',
                           categories=db_get_all_objects_of_type(Category),
                           category=category,
                           category_items=category_items,
                           creator=creator,
                           items=db_get_all_items(),
                           user=user)

# Category Item
@app.route('/catalog/item/<int:item_id>/')
def category_item_info(item_id):
    """
    Function to return a page to view a category item.

    Args:
        item_id: ID value of the category item to view.
    """

    # Retrieve CategoryItem object for template rendering.
    # If nott found, render error template.
    category_item = db_session.query(CategoryItem)\
        .filter_by(id=item_id)\
        .first()
    if not category_item:
        return render_template('error.html',
                               headline_text='Item Not Found',
                               error_text='The specified item was not found.')

    creator = category_item.category.user
    user = get_user()

    return render_template('category_item_info.html',
                           categories=db_get_all_objects_of_type(Category),
                           item=category_item,
                           items=db_get_all_items(),
                           creator=creator,
                           user=user)

# New Category
@app.route('/catalog/category/new/', methods=['GET', 'POST'])
def new_category():
    """
    Function to create a new category.
    """

    user = get_user()
    if not user:
        return redirect(url_for('login_with_redirect',
                                redirect_url=urllib.quote_plus('/catalog/category/new/')))
    if request.method == 'POST':
        category = Category(name=request.form['name'],
                            user_id=login_session['user_id'])
        db_session.add(category)
        db_session.commit()
        flash('New Category {} Successfully Created!'.format(category.name))
        return redirect(url_for('index'))
    else:
        return render_template('new_category.html',
                               user=user)

# New Category Item
@app.route('/catalog/item/new/', methods=['GET', 'POST'])
def new_category_item():
    """
    Function to return a page to create a new category item.
    """

    user = get_user()
    categories = db_get_all_objects_of_type(Category)
    if not user:
        return redirect(url_for('login_with_redirect',
                                redirect_url=urllib.quote_plus('/catalog/item/new/')))
    if request.method == 'POST':
        if request.form.get('name', '') == '' and request.form.get('category', '') != '':
            return render_template('new_category_item.html',
                                   user=user,
                                   categories=categories,
                                   request=request)
        new_item = CategoryItem(name=request.form['name'],
                                user_id=login_session['user_id'],
                                description=request.form['description'],
                                category_id=request.form['category'])
        db_session.add(new_item)
        db_session.commit()
        flash('New Item {} Successfully Created!'.format(new_item.name))
        return redirect(url_for('index'))
    else:
        return render_template('new_category_item.html',
                               user=user,
                               categories=categories)

# Edit Category Item
@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def edit_category(category_id):
    """
    Function to return a page to edit a category.

    Args:
        category_id: ID value of the category to edit.
    """

    user = get_user()
    categories = db_get_all_objects_of_type(Category)
    edited_item = db_session.query(Category)\
        .filter_by(id=category_id)\
        .first()
    if not edited_item:
        return render_template('error.html',
                               headline_text='Category Not Found',
                               error_text='The specified category was not found.')


    if request.method == 'POST':
        edited_item.name = request.form['name']
        db_session.add(edited_item)
        db_session.commit()
        flash('Category Successfully Updated!')
        return redirect(url_for('category_info',
                                category_id=edited_item.id))
    else:
        return render_template('edit_category.html',
                               category=edited_item,
                               user=user,
                               categories=categories)

# Edit Category Item
@app.route('/catalog/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def edit_category_item(item_id):
    """
    Function to return a page to edit a category item.

    Args:
        item_id: ID value of the category item to edit.
    """

    user = get_user()
    categories = db_get_all_objects_of_type(Category)
    edited_item = db_session.query(CategoryItem)\
        .filter_by(id=item_id)\
        .first()
    if not edited_item:
        return render_template('error.html',
                               headline_text='Item Not Found',
                               error_text='The specified item was not found.')


    if request.method == 'POST':
        edited_item.name = request.form['name']
        edited_item.description = request.form['description']
        edited_item.category_id = request.form['category']
        db_session.add(edited_item)
        db_session.commit()
        flash('Item Successfully Updated!')
        category = db_session.query(Category)\
            .filter_by(id=edited_item.category_id)\
            .first()
        return redirect(url_for('category_item_info',
                                item_id=edited_item.id))
    else:
        return render_template('edit_category_item.html',
                               item=edited_item,
                               user=user,
                               categories=categories)

# Delete Category
@app.route('/catalog/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def delete_category(category_id):
    """
    Function to return a page to delete a category.

    Args:
        category_id: ID of the category to delete.
    """

    category = db_session.query(Category)\
        .filter_by(id=category_id).first()
    if not category:
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Get and delete all items associated with this category.
        items = db_session.query(CategoryItem)\
            .filter_by(category_id=category.id)\
            .all()
        for item in items:
            db_session.delete(item)

        # Delete the category itself and commit everything.
        db_session.delete(category)
        db_session.commit()
        flash("Category {} deleted.".format(category.name))
        return redirect(url_for('index'))
    else:
        return render_template('delete_category.html',
                               category=category)

# Delete Category Item
@app.route('/catalog/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def delete_category_item(item_id):
    """
    Function to return a page to delete a category item.

    Args:
        item_id: ID of the category item to delete.
    """

    item = db_session.query(CategoryItem)\
        .filter_by(id=item_id)\
        .first()
    category_id = ''
    if not item:
        if login_session.get('last_category_id', '') == '':
            return redirect(url_for('index'))
        else:
            category_id = login_session.get('last_category_id')
    else:
        category_id = item.category.id

    #item_category = item.category
    if request.method == 'POST':
        db_session.delete(item)
        db_session.commit()
        flash("Item {} deleted.".format(item.name))
        return redirect(url_for('category_info',
                                category_id=category_id))
    else:
        return render_template('delete_category_item.html',
                               item=item)



#-----------------------------------------------------------------------
# Login/Social Connect Functionality
#-----------------------------------------------------------------------

# Log In
@app.route('/login/')
def login():
    """
    Function to return a page for user login.
    """

    # Create random number to store in session
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/login/?redirect_url=<redirect_url>')
def login_with_redirect(redirect_url):
    """
    Function to return a page for user login with redirect.
    """

    # Create random number to store in session
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    login_session['redirect_url'] = redirect_url
    return render_template('login.html', STATE=state)

# Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Function to connect to Google for social login.
    """

    # If state doesn't match login session state, we know it's an invalid
    # request and should redirect accordingly.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Set code to the request data for use in retrieving credentials
    code = request.data
    credentials = None

    # Upgrade the authorization code into credentials object,
    # specify this is the one-time code server sending off, and
    # initiate exchange, passing in one-time code as input.
    # This exchanges authorization code for a credentials object
    try:
        oauth_flow = flow_from_clientsecrets(GOOGLE_JSON, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that access token is valid.
    # Use UAuth2Credentials.from_json() method, which accepts a data str
    # argument of a JSON string from its own to_json() method.
    access_token = OAuth2Credentials.from_json(credentials.to_json()).access_token
    api_url = 'https://www.googleapis.com/oauth2/v1'
    url = '{}/tokeninfo?access_token={}'.format(api_url, access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])

    # If there was an error, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps('Token of user ID does not match given user ID.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify the access token is valid for this app
    if result['issued_to'] != CLIENT_ID_GOOGLE:
        response = make_response(json.dumps('Token of client ID does not match app ID.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store access token and ID in session for later use
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info and store in login session
    userinfo_url = '{}/userinfo'.format(api_url)
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists. If not, make a new one.
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user()

    # Store user_id in login session
    login_session['user_id'] = user_id

    # Create flash message with user-specific info included
    flash(get_user_logged_in_markup())
    return ''

# Facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """
    Function to connect to Facebook for social login.
    """

    # If state doesn't match login session state, we know it's an invalid
    # request and should redirect accordingly.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data

    # Exchange client token for long-lived server-side token
    url = """https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token
        &client_id={}&client_secret={}&fb_exchange_token={}"""\
        .format(APP_ID_FACEBOOK, APP_SECRET_FACEBOOK, access_token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]

    # Use token to get user info from API, stripping expire tag from token.
    userinfo_url = 'https://graph.facebook.com/v2.5/me'
    token = result.split('&')[0]
    url = '{}?{}&fields=name,id,email'.format(userinfo_url, token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    # Store data in login_session
    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']
    login_session['access_token'] = token

    # Get user picture and store in login session
    url = '{}/picture?{}&redirect=0&height=200&width=200'.format(userinfo_url, token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data['data']['url']

    # See if user exists. If not, make a new one.
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user()
    login_session['user_id'] = user_id

    # Create flash message with user-specific info included
    flash(get_user_logged_in_markup())
    return ''


#-----------------------------------------------------------------------
# Logout/Disconnect Functionality
#-----------------------------------------------------------------------

# Log Out
#@app.route('/logout/')
#def logout():
#    """
#    Function to return a page for user logout.
#    """
#
#    return render_template('logout.html')

# Google
@app.route('/gdisconnect')
def gdisconnect():
    """
    Function to disconnect from Google.
    """

    # Only disconnect a connected user
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute request to revoke current user
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(access_token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]

    if result['status'] != '200':
        # For some reason, given token was invalid
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

# Facebook
@app.route('/fbdisconnect')
def fbdisconnect():
    """
    Function to disconnect from Facebook.
    """

    # Note: Access token must be included to successfully log out
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = """https://graph.facebook.com/{}/permissions?access_token={}"""\
        .format(facebook_id, access_token)
    http = httplib2.Http()
    result = http.request(url, 'DELETE')[1]

# General
@app.route('/disconnect')
def disconnect():
    """
    Function to disconnect from social provider and clear session.
    """

    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        if login_session.get('last_category_id', '') != '':
            del login_session['last_category_id']
        if login_session.get('redirect_url', '') != '':
            del login_session['redirect_url']
        flash('You have successfully logged out.')
        return redirect(url_for('index'))
    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('index'))


#-----------------------------------------------------------------------
# Convenience functions
#-----------------------------------------------------------------------

def user_logged_in():
    """
    Function to return whether or not user is logged in.
    """

    return 'username' in login_session

def get_user():
    """
    Function to retrieve user from email stored in login session.
    """

    return get_user_info(get_user_id(login_session.get('email', '')))


def get_user_id(email):
    """
    Function to return user ID for user with specified email address.

    Args:
        email: Email address for user whose ID will be returned.
    """

    try:
        user = db_session.query(User).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None

def get_user_info(user_id):
    """
    Function to return User object for user with specified user ID.

    Args:
        user_id: User ID for user object to return.
    """

    try:
        user = db_session.query(User).filter_by(id=user_id).one()
        return user
    except NoResultFound:
        return None

def create_user():
    """
    Function to create a new user with the info from login session.
    """

    new_user = User(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    db_session.add(new_user)
    db_session.commit()
    user = db_session.query(User)\
        .filter_by(email=login_session['email'])\
        .one()
    return user.id

def get_user_logged_in_markup():
    """
    Function to return Markup for user login.
    """

    return Markup("""<table class="flash-table">
        <tr><td><span class="profile-pic">
        <img src="{0}" alt="{1}"/></span>
        </td><td>Logged in as {1}</td></tr></table>"""\
        .format(login_session['picture'], login_session['username']))


#-----------------------------------------------------------------------
# JSON Endpoints
#-----------------------------------------------------------------------

@app.route('/catalog/json/')
def catalog_json():
    """
    Function to return JSON of all categories and items.
    """

    categories = db_get_all_objects_of_type(Category)
    categories_list = []
    for cat in categories:
        categories_list.append(cat.serialize)
        items = db_session.query(CategoryItem).filter_by(category_id=cat.id).all()
        categories_list[-1]['items'] = [item.serialize for item in items]
    return jsonify(categories=categories_list)


@app.route('/catalog/categories/json/')
def categories_json():
    """
    Function to return JSON of all categories.
    """

    categories = db_get_all_objects_of_type(Category)
    return jsonify(categories=[cat.serialize for cat in categories])

@app.route('/catalog/category/<int:category_id>/json/')
def category_info_json(category_id):
    """
    Function to return JSON of specified category.

    Args:
        category_id: ID value of the category for the item.
    """

    category = db_session.query(Category).filter_by(id=category_id).first()
    if not category:
        return jsonify({'error': 'The specified category was not found.'})
    return jsonify(category.serialize)

@app.route('/catalog/category/<int:category_id>/items/json/')
def category_items_info_json(category_id):
    """
    Function to return JSON of category items for specified category.

    Args:
        category_id: ID value of the category for the item.
    """

    category = db_session.query(Category).filter_by(id=category_id).first()
    if not category:
        return jsonify({'error': 'The specified category was not found.'})
    items = db_session.query(CategoryItem).filter_by(category_id=category_id).all()
    return jsonify(items=[item.serialize for item in items])

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/json/')
def category_item_info_json(category_id, item_id):
    """
    Function to return JSON of specified category item.

    Args:
        category_id: ID value of the category for the item.
        item_id: ID value of the category item to view.
    """

    category = db_session.query(Category).filter_by(id=category_id).first()
    if not category:
        return jsonify({'error': 'The specified category was not found.'})
    item = db_session.query(CategoryItem).filter_by(id=item_id).first()
    if not item:
        return jsonify({'error': 'The specified category item was not found.'})
    return jsonify(item.serialize)
