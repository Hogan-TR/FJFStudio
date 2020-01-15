import json
from models import Record
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:320683@localhost:5432/test',
                       encoding='utf-8')
DBSession = sessionmaker(bind=engine)
session = DBSession()


def insert(data):
    if type(data) == type([]):
        session.add_all(data)
    else:
        session.add(data)

    session.commit()


def read_json():
    path = r"C:\Users\TR152\Desktop\dn120-xitongcheng.json"
    file = open(path, 'r', encoding='utf-8')
    json_file = json.load(file)

    que = list()
    for i in json_file[:5]:
        data = Record(title=i['title'], link=i['link'], tags=i['tags'],
                      introduction=i['content']['introduction'], solve=i['content']['solve'], img=i['img_url'])
        # que.append(data)
        insert(data)
    # insert(que)
    file.close()


if __name__ == '__main__':
    read_json()
    session.close()
