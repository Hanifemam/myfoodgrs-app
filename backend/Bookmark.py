import json
import random

import BookmarkModel


class Bookmark(object):
    def __init__(self, connection):
        self.mysql_conn = connection

    def create_bookmark_table(self):
        my_cursor = self.mysql_conn.cursor()
        my_cursor.execute('DROP TABLE IF EXISTS bookmarks;')
        query = 'CREATE TABLE bookmarks ' \
                '(id int PRIMARY KEY UNIQUE auto_increment, ' \
                'restaurant_id int, ' \
                'group_id int)'
        # 'FOREIGN KEY (group_id) REFERENCES mygroups(id)' \
        # 'FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)' \
        my_cursor.execute(query)

    def insert_bookmark(self, bookmark: BookmarkModel):
        my_cursor = self.mysql_conn.cursor()
        new_bookmark = bookmark
        query = "INSERT INTO bookmarks (restaurant_id, group_id) " \
                "VALUES (%(restaurant_id)s, %(group_id)s)"
        my_cursor.execute(query, new_bookmark)
        self.mysql_conn.commit()
        query = "SELECT last_insert_id();"
        my_cursor.execute(query)
        last_id = my_cursor.fetchone()
        self.mysql_conn.commit()
        return json.dumps({'bookmar_id': int(last_id[0])})

    def remove_bookmark(self, bookmark: BookmarkModel):
        my_cursor_select = self.mysql_conn.cursor()
        new_bookmark = bookmark
        query = f"DELETE FROM bookmarks WHERE restaurant_id = {new_bookmark['restaurant_id']} AND " \
                f"group_id = {new_bookmark['group_id']}; "
        my_cursor_select.execute(query)
        self.mysql_conn.commit()
        return "DELETED"

    def get_bookmark(self, group_id: int):
        bookmarked_restaurants = []
        my_cursor_select = self.mysql_conn.cursor()
        query = f"SELECT restaurant_id FROM bookmarks WHERE group_id = {group_id};"
        my_cursor_select.execute(query)
        for restaurant in my_cursor_select:
            bookmarked_restaurants.append(int(restaurant[0]))
        return bookmarked_restaurants

    def create_fake_data_bookmark(self):
        restaurant_id_list = []
        query = "SELECT id FROM restaurants"
        cursor = self.mysql_conn.cursor()
        cursor.execute(query)
        for restaurant in cursor:
            restaurant_id_list.append(int(restaurant[0]))
        for i in range(3100):
            sampled = random.choices(restaurant_id_list)
            self.insert_bookmark(
                BookmarkModel.BookmarkModel(
                    restaurant_id=sampled[0],
                    group_id=random.randint(1, 100)
                )
            )

