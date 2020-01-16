from flask import Flask, make_response, jsonify
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Record, AlchemyEncoder


app = Flask(__name__)
engine = create_engine(
    "postgresql+psycopg2://postgres:320683@localhost:5432/test", encoding='utf-8')
DBSession = sessionmaker(bind=engine)


@app.route('/')
def hello():
    return 'Hello World'


@app.route('/search/<string:key>', methods=['GET'])
def get_data(key):
    session = DBSession()
    data = session.query(Record).filter(Record.title.contains(key)).all()
    if len(data) > 12:
        data = data[0:12]
    res = {"status": True, "data": []}
    for i in data:
        temp = json.dumps(i, cls=AlchemyEncoder)
        temp = json.loads(temp)
        res['data'].append(temp)
    return make_response(jsonify(res))


if __name__ == '__main__':
    app.run()
