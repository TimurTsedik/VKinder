import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    vk_id = sa.Column(sa.VARCHAR(128), primary_key=True)
    name = sa.Column(sa.VARCHAR(128), nullable=False)
    surname = sa.Column(sa.VARCHAR(128))
    city = sa.Column(sa.VARCHAR(128))
    sex = sa.Column(sa.Integer)
    age = sa.Column(sa.Integer)
    date_create = sa.Column(sa.TIMESTAMP, server_default=sa.func.now())
    foto_a_1 = sa.Column(sa.VARCHAR(256))
    foto_a_2 = sa.Column(sa.VARCHAR(256))
    foto_a_3 = sa.Column(sa.VARCHAR(256))
    foto_fr_1 = sa.Column(sa.VARCHAR(256))
    foto_fr_2 = sa.Column(sa.VARCHAR(256))
    foto_fr_3 = sa.Column(sa.VARCHAR(256))
    interests = sa.Column(sa.VARCHAR(10000))
    books = sa.Column(sa.VARCHAR(10000))
    music = sa.Column(sa.VARCHAR(10000))
    movies = sa.Column(sa.VARCHAR(10000))


class Favorite(Base):
    __tablename__ = "users_favorites"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.VARCHAR(128), sa.ForeignKey("users.vk_id"), nullable=False)
    user_fav_id = sa.Column(sa.VARCHAR(128), sa.ForeignKey("users.vk_id"), nullable=False)
    # favorite = relationship("User", backref="favorite")


class BlackList(Base):
    __tablename__ = "black_list"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.VARCHAR(128), sa.ForeignKey("users.vk_id"), nullable=False)
    user_black_id = sa.Column(sa.VARCHAR(128), sa.ForeignKey("users.vk_id"), nullable=False)
    # black_list = relationship("User", backref="black_list")


def create_tables(engine):
    """
    create_tables function description, including its parameters and return type.
    """
    Base.metadata.create_all(engine)
