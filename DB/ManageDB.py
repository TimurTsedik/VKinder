import configparser
from datetime import datetime, timedelta

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from DB.ModelBD import User, BlackList, Favorite, create_tables


class ManageDB:

    def __init__(self, db_name: str, user_name: str, user_password: str, db_protocol: str = "postgresql",
                 host: str = "localhost", port: str = "5432") -> None:
        self.DSN = f"{db_protocol}://{user_name}:{user_password}@{host}:{port}/{db_name}"
        self.engine = sa.create_engine(self.DSN)
        create_tables(self.engine)
        self._session = sessionmaker(bind=self.engine)()

    def add_user_db(self, user_info: dict) -> int:
        """Добавление пользователя в базу\n
        Параметры:\n
        Vk_id - integer\n
        Name - string\n
        Age - integer > 0\n
        Gender is Male = 1, Female = 0\n
        City - INTEGER\n
        Возвращает  0 если юзер уже есть в базе.
        возвращает  1 если юзер меньше 18\n
        Возвращает  2 если юзер добавлен в базу."""
        x_ret = self._session.query(User).where(User.vk_id == user_info['vk_id'])
        # Проверка 18+
        if int(user_info['age']) < 18:
            return 1
        # Проверка на существование в базе
        elif len(x_ret.all()) > 0:
            return 0
        else:
            self._session.add(
                User(vk_id=user_info['vk_id'],
                     name=user_info['name'],
                     surname=user_info['surname'],
                     age=user_info['age'],
                     sex=user_info['sex'],
                     city=user_info['city'],
                     foto_a_1=user_info['foto_a_1'],
                     foto_a_2=user_info['foto_a_2'],
                     foto_a_3=user_info['foto_a_3'],
                     foto_fr_1=user_info['foto_fr_1'],
                     foto_fr_2=user_info['foto_fr_2'],
                     foto_fr_3=user_info['foto_fr_3'],
                     interests=user_info['interests'],
                     books=user_info['books'],
                     music=user_info['music'],
                     movies=user_info['movies']))
            self._session.commit()
            return 2

    def actualize_user(self, user_info: dict) -> bool:
        """Обновление пользователя в базе\n
        Параметры:\n
        Vk_id - short string\n
        Name - string\n
        Age - integer > 0\n
        Gender is Male = 1, Female = 0\n
        City - INTEGER\n
        Возвращает True если юзер обновлен в базе.\n"""
        if self.get_user_by_vk_id(user_info['vk_id']) is not None or datetime.now() - \
                self.get_user_by_vk_id(user_info['vk_id'])['date_create'] > timedelta(days=1):
            x_ret = self._session.query(User).where(User.vk_id == user_info['vk_id'])
            x_ret.update(user_info)
            self._session.commit()
            return True
        else:
            return False

    def add_favorites(self, user_id: str, fav_id: str) -> bool:
        """Добавление пользователя с базу избранных\n
        Parameters:\n
        user_id кто добавляет в базу\n
        fav_id кого добавляют в базу\n
        Возвращает True если добавлено\n"""
        # Проверка на существование в избранных
        if fav_id in self.get_list_favorites(user_id):
            return False
        else:
            # Проверка на существование в черном списке и удаление из него
            if fav_id in self.get_list_blacklist(user_id):
                self.remove_blacklist(user_id, fav_id)
            self._session.add(Favorite(user_id=user_id, user_fav_id=fav_id))
            self._session.commit()
            return True

    def remove_favorites(self, user_id: str, fav_id: str) -> bool:
        """Удаление пользователя из избранных\n
        Parameters:\n
        user_id кто удаляет из базы\n
        fav_id кого удаляют из базы\n
        Возвращает True если удалено\n"""
        self._session.query(Favorite).where(Favorite.user_id == user_id, Favorite.user_fav_id == fav_id).delete()
        self._session.commit()
        return True

    def add_blacklist(self, user_id: str, bl_id: str) -> bool:
        """Добавление пользователя черный список\n
        Parameters:\n
        user_id кто добавляет в базу\n
        bl_id кого добавляют в базу\n
        Возвращает True если добавлено\n"""
        # Проверка на существование в черном списке
        if bl_id in self.get_list_blacklist(user_id):
            return False
        else:
            # Проверка на существование в избранных и удаление из избранных
            if bl_id in self.get_list_favorites(user_id):
                self.remove_favorites(user_id, bl_id)
            self._session.add(BlackList(user_id=user_id, user_black_id=bl_id))
            self._session.commit()
            return True

    def remove_blacklist(self, user_id: str, bl_id: str) -> bool:
        """Удаление пользователя из черного списка\n
        Parameters:\n
        user_id кто удаляет из базы\n
        bl_id кого удаляют из базы\n
        Возвращает True если удалено\n"""
        self._session.query(BlackList).where(BlackList.user_id == str(user_id),
                                             BlackList.user_black_id == str(bl_id)).delete()
        self._session.commit()
        return True

    def get_list_favorites(self, vk_id: str) -> list:
        """Получение списка избранных\n
        Возвращает не пустой LIST, если все хорошо."""
        fav_list = []
        try:
            favorite_ids = self._session.query(Favorite).where(Favorite.user_id == str(vk_id))
            for x in favorite_ids.all():
                fav_list.append(x.user_fav_id)
            return fav_list
        except Exception:
            return fav_list

    def get_list_blacklist(self, vk_id: str) -> list:
        """Получение черного списка\n
        Возвращает не пустой LIST, если все хорошо."""
        bl_list = []
        try:
            blacklist_ids = self._session.query(BlackList).where(BlackList.user_id == str(vk_id))
            for x in blacklist_ids.all():
                bl_list.append(x.user_black_id)
            return bl_list
        except Exception:
            return bl_list

    def if_user_in_blacklist(self, vk_id_asking: str, vk_id_ckecking: str) -> bool:
        """Проверка на вхождение в черный список\n
        Возвращает True если юзер в черном списке\n"""
        if vk_id_ckecking in self.get_list_blacklist(vk_id_asking):
            return True
        else:
            return False

    def get_user_by_vk_id(self, vk_id: str) -> dict:
        """Получение словаря с данными юзера\n
        Возвращает не пустой LIST, если все хорошо."""
        x_ret = self._session.query(User).where(User.vk_id == str(vk_id))
        for x in x_ret.all():
            return {"name": x.name, "surname": x.surname, "age": x.age, "sex": x.sex, "city": x.city, "vk_id": x.vk_id,
                    "date_create": x.date_create,
                    "foto_a_1": x.foto_a_1, "foto_a_2": x.foto_a_2, "foto_a_3": x.foto_a_3, "foto_fr_1": x.foto_fr_1,
                    "foto_fr_2": x.foto_fr_2, "foto_fr_3": x.foto_fr_3}
        return {}

    def if_user_in_db(self, vk_id: str) -> bool:
        """Проверка на существование в базе\n
        Возвращает True если юзер в базе\n"""
        x_ret = self._session.query(User).where(User.vk_id == str(vk_id))
        if len(x_ret.all()) > 0:
            return True
        else:
            return False


# Тест базы
# if __name__ == '__main__':
#     config = configparser.ConfigParser()
#     config.read('../config.ini')
#     DB = ManageDB(db_name=config['DB']['DB_name'], user_name=config['DB']['DB_user'],
#                   user_password=config['DB']['DB_password'])
#
#     DB.add_user_db(
#         {"name": "Vasya", "surname": "Pupkin", "age": 18, "sex": 1, "city": 1, "vk_id": "431302925", "foto_a_1": "1",
#          "foto_a_2": "2", "foto_a_3": "3", "foto_fr_1": "4", "foto_fr_2": "5", "foto_fr_3": "6"})
#     DB.add_user_db({"name": "Petya", "surname": "Ivanov", "age": 55, "sex": 1, "city": 1, "vk_id": "2", "foto_a_1": "1",
#                     "foto_a_2": "2", "foto_a_3": "3", "foto_fr_1": "4", "foto_fr_2": "5", "foto_fr_3": "6"})
#     DB.add_user_db(
#         {"name": "V", "surname": "P", "age": 20, "sex": 1, "city": 1, "vk_id": "3", "foto_a_1": "1", "foto_a_2": "2",
#          "foto_a_3": "3", "foto_fr_1": "4", "foto_fr_2": "5", "foto_fr_3": "6"})
#     DB.actualize_user({"name": "Vasya", "surname": "Pupkin", "age": 38, "sex": 1, "city": 1, "vk_id": "431302925"})
#     DB.add_favorites("431302925", "2")
#     DB.add_blacklist("431302925", "3")
#     print(DB.get_list_favorites("431302925"))
#     print(DB.get_list_blacklist("431302925"))
#     print(DB.get_user_by_vk_id("431302925"))
