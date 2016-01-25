"""
This module provides database-related items, including setup of
the DB engine and session, DB initialization, and convenience
functions.
"""

#pylint: disable=invalid-name,no-member,relative-import

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///catalog/item_catalog.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """
    Function to initialize the application database.
    """

    # Import all modules here that might define models so that they will
    # be registered properly on the metadata. Otherwise will need to import
    # them first before calling init_db()
    from catalog.models import Category, CategoryItem, User
    Base.metadata.create_all(bind=engine)

    # Query all items. If none exist, we know we need to populate the DB.
    if len(get_all_objects_of_type(Category)) < 1:
        from database_setup import populate_database
        populate_database(db_session)

    all_users = get_all_objects_of_type(User)
    all_categories = get_all_objects_of_type(Category)
    all_items = get_all_objects_of_type(CategoryItem)
    print "Database Info:"
    print "  - {} Users".format(len(all_users))
    print "  - {} Categories".format(len(all_categories))
    print "  - {} Category Items".format(len(all_items))


def get_last_x_items_of_type(num_items, Class):
    """
    Convenience function to return the last X number
    of items for specified object type.
    """
    return db_session.query(Class).order_by(Class.id.desc()).limit(num_items)


def get_all_objects_of_type(Class):
    """
    Convenience function to return result of query for specified object type.
    """
    return db_session.query(Class).all()


def get_all_items_for_category_id(category_id):
    """
    Convenience function to return CategoryItem objects of specified category.
    """
    from catalog.models import CategoryItem
    return db_session.query(CategoryItem).filter_by(category_id=category_id).all()


def get_all_items():
    """
    Convenience function to return a list of lists for all items.
    """
    from catalog.models import Category
    categories = get_all_objects_of_type(Category)
    items = []
    for category in categories:
        items.append(get_all_items_for_category_id(category.id))
    return items



def get_or_create(session, model, **kwargs):
    """
    Function to get or create the given object.

    Args:
        session: An instance of Session
        model: The object to create and add (if not already present)
        **kwargs: Keyword arguments for the specified model object

    Returns:
        Instance of the specified object.

    Source:
        http://stackoverflow.com/a/6078058/1914233
    """

    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        # To persist new item into DB, need to add and commit!
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


if __name__ == '__main__':
    pass
