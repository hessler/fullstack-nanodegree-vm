"""
This module provides pre-fab data for User, Category, and
CategoryItem objects for the database.
"""

#pylint: disable=global-statement,unused-variable,line-too-long,too-many-locals

from catalog.models import Category, CategoryItem, User
from catalog.database import get_or_create


def populate_database(session):
    """Function to create User, Category, and CategoryItem objects."""

    print "Populating database with users, categories, and items..."

    # Create users first so we can attribute categories and items
    user_1 = get_or_create(session, User,
                           name="Neal Caffrey",
                           email="neal.caffrey@whitecollar.com",
                           picture="https://pbs.twimg.com/profile_images/1214625748/003b.jpg")

    user_2 = get_or_create(session, User,
                           name="Mozzie",
                           email="mozzie@whitecollar.com",
                           picture="https://pbs.twimg.com/profile_images/2250024994/DanteHaversham.jpg")

    user_3 = get_or_create(session, User,
                           name="Richard Castle",
                           email="richard.castle@castle.com",
                           picture="https://pbs.twimg.com/profile_images/2623279287/image.jpg")

    user_4 = get_or_create(session, User,
                           name="Jerry Seinfeld",
                           email="jerry@seinfeld.com",
                           picture="https://pbs.twimg.com/profile_images/433319671430123521/LAm8cB1b.jpeg")

    user_5 = get_or_create(session, User,
                           name="Harvey Specter",
                           email="harvey.specter@suits.com",
                           picture="https://pbs.twimg.com/profile_images/450189672967204864/dOrXNMrc.jpeg")

    # Create categories
    category_1 = get_or_create(session, Category,
                               name="Art",
                               user_id=1)

    category_2 = get_or_create(session, Category,
                               name="Wine",
                               user_id=2)

    category_3 = get_or_create(session, Category,
                               name="Books",
                               user_id=3)

    category_4 = get_or_create(session, Category,
                               name="Television",
                               user_id=4)

    category_5 = get_or_create(session, Category,
                               name="Men's Fashion",
                               user_id=5)

    # Create category items
    item_1 = get_or_create(session, CategoryItem,
                           name="Mona Lisa",
                           description="The Mona Lisa is a half-length "\
                                "portrait of a woman by the Italian artist "\
                                "Leonardo da Vinci, which has been acclaimed "\
                                "as 'the best known, the most visited, the "\
                                "most written about, the most sung about, the "\
                                "most parodied work of art in the world'.",
                           category_id=1,
                           user_id=1)

    item_2 = get_or_create(session, CategoryItem,
                           name="Riesling",
                           description="Riesling is a white grape variety "\
                                "which originated in the Rhine region of Germany. "\
                                "Riesling is an aromatic grape variety displaying "\
                                "flowery, almost perfumed, aromas as well as high "\
                                "acidity.",
                           category_id=2,
                           user_id=2)

    item_3 = get_or_create(session, CategoryItem,
                           name="The Phantom Tollbooth",
                           description="The Phantom Tollbooth is a children's "\
                                "adventure novel and modern fairy tale by Norton "\
                                "Juster. It was published in 1961 with "\
                                "illustrations by Jules Feiffer.",
                           category_id=3,
                           user_id=3)

    item_4 = get_or_create(session, CategoryItem,
                           name="White Collar",
                           description="The third time turns out to be the "\
                                "charm for criminal Neal Caffrey. He has been "\
                                "eluding FBI agent Peter Burke for years, a "\
                                "run that finally comes to an end with his "\
                                "capture. But after the resourceful prisoner "\
                                "escapes from a maximum-security facility, "\
                                "then is nabbed once again by Burke, Caffrey "\
                                "suggests a different end-game: In return for "\
                                "freedom, he'll help the Feds catch long-sought "\
                                "criminals. Though skeptical, Burke soon realizes "\
                                "that Caffrey's instincts and insight are a rare "\
                                "commodity. Caffrey's trusted friend and "\
                                "co-conspirator with ties to the criminal "\
                                "underworld, Mozzie, also becomes a useful "\
                                "source for Burke and the FBI.",
                           category_id=4,
                           user_id=4)

    item_5 = get_or_create(session, CategoryItem,
                           name="Power Suit",
                           description="By pairing together a custom tailored "\
                                "3-piece suit with a spread-collar dress shirt "\
                                "with french cuffs and a bold tie with a windsor "\
                                "knot, you can easily pull off a look of "\
                                "corporate power and confidence that can help "\
                                "you elevate your game in the office, the board "\
                                "room, and beyond.",
                           category_id=5,
                           user_id=5)

    item_6 = get_or_create(session, CategoryItem,
                           name="Starry Night",
                           description="The Starry Night is an oil on canvas "\
                                "by the Dutch post-impressionist painter Vincent "\
                                "van Gogh. Painted in June, 1889, it depicts the "\
                                "view from the east-facing window of his asylum "\
                                "room at Saint-Remy-de-Provence, just before "\
                                "sunrise, with the addition of an idealized "\
                                "village. It has been in the permanent collection "\
                                "of the Museum of Modern Art in New York City "\
                                "since 1941, acquired through the Lillie P. "\
                                "Bliss Bequest. It is regarded as among Van "\
                                "Gogh's finest works, and is one of the most "\
                                "recognized paintings in the history of Western "\
                                "culture.",
                           category_id=1,
                           user_id=1)

    item_7 = get_or_create(session, CategoryItem,
                           name="Malbec",
                           description="Malbec is a purple grape variety used "\
                                "in making red wine. The grapes tend to have an "\
                                "inky dark color and robust tannins, and are "\
                                "known as one of the six grapes allowed in the "\
                                "blend of red Bordeaux wine.",
                           category_id=2,
                           user_id=2)

    item_8 = get_or_create(session, CategoryItem,
                           name="Digital Fortress",
                           description="Digital Fortress is a techno-thriller "\
                                "novel written by American author Dan Brown and "\
                                "published in 1998 by St. Martin's Press. The "\
                                "book explores the theme of government "\
                                "surveillance of electronically stored "\
                                "information on the private lives of citizens, "\
                                "and the possible civil liberties and ethical "\
                                "implications using such technology.",
                           category_id=3,
                           user_id=3)

    item_9 = get_or_create(session, CategoryItem,
                           name="Suits",
                           description="In need of an associate, big-time "\
                                "Manhattan corporate lawyer Harvey Specter hires "\
                                "the only guy who impresses him -- college "\
                                "dropout Mike Ross. The fact that Ross isn't "\
                                "actually a lawyer isn't lost on Specter, who "\
                                "believes his new right-hand man is a legal "\
                                "prodigy with the book smarts of a Harvard law "\
                                "grad and the street smarts of a hustler. "\
                                "However, in order to keep their jobs, the "\
                                "charade must remain strictly between these two "\
                                "unconventional thinkers.",
                           category_id=4,
                           user_id=4)

    item_10 = get_or_create(session, CategoryItem,
                            name="Duffle Coat",
                            description="A recent fashion trend among winter "\
                                "outerwear, the duffle coat is between the "\
                                "classic winter coat and the parka, usually "\
                                "with a hood, wooden buttons, square pockets, "\
                                "and sporting a well-defined cut and shape.",
                            category_id=5,
                            user_id=5)

    print "Database successfully populated with pre-fab data."
