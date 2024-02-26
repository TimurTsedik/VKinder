import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    vk_id = sa.Column(sa.VARCHAR(128), primary_key=True)
    name = sa.Column(sa.VARCHAR(256), nullable=False)
    surname = sa.Column(sa.VARCHAR(256))
    city = sa.Column(sa.Integer)
    sex = sa.Column(sa.Integer)
    age = sa.Column(sa.Integer)


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
    # Не забыть удалить перед сдачей проекта!!!!!!!!!
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
