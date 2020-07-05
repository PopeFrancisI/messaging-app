from psycopg2 import connect
from datetime import datetime

class Message:

    def __init__(self, from_id="", to_id="", text=""):
        self._id = -1
        self._from_id = from_id
        self._to_id = to_id
        self._text = text
        self._creation_date = None

    @property
    def id(self):
        return self._id

    @property
    def from_id(self):
        return self._from_id

    @property
    def to_id(self):
        return self._to_id

    @property
    def text(self):
        return self._text

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO Messages(from_id, to_id, text, creation_date)
                            VALUES(%s, %s, %s, %s) RETURNING id"""
            values = (self.from_id, self.to_id, self.text, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        # else:
        #     sql = """UPDATE Messages SET from_id=%s, to_id=%s, text=%s, creation_date=%s
        #                    WHERE id=%s"""
        #     values = (self.from_id, self.to_id, self.text, datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f"), self.id)
        #     cursor.execute(sql, values)
        #     return True

    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, creation_date, text FROM Messages"
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id_, to_id_, creation_date_, text_ = row
            loaded_message = Message(from_id_, to_id_, text_)
            loaded_message._id = id_
            loaded_message._creation_date = creation_date_
            messages.append(loaded_message)
        return messages
