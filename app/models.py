from flask_sqlalchemy import SQLAlchemy
from flask import Response
import requests
from configparser import ConfigParser
from datetime import datetime, timedelta

db = SQLAlchemy()
api_config = ConfigParser()
api_config.read('api.ini')


class Port(db.Model):
    __tablename__ = 'ports'
    code = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    parent_slug = db.Column(db.String(), db.ForeignKey('regions.slug'), nullable=False)


class Region(db.Model):
    __tablename__ = 'regions'
    slug = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    parent_slug = db.Column(db.String(), db.ForeignKey('regions.slug'), nullable=True)


class Price(db.Model):
    __tablename__ = 'prices'
    orig_code = db.Column(db.String(), db.ForeignKey('ports.code'), primary_key=True)
    dest_code = db.Column(db.String(), db.ForeignKey('ports.code'), primary_key=True)
    day = db.Column(db.DateTime(), primary_key=True)
    price = db.Column(db.Integer(), primary_key=True, autoincrement=False)


def get_rates(params, min_price_count=0):
    val_map = dict(params)
    val_map["min_price_count"] = min_price_count
    result = db.session.execute('''
    select day, 
    case when count(price)>=:min_price_count then avg(price)
		 else null
	end as price
    from prices
    where day between :date_from and :date_to
    and orig_code IN(
        select code
        from ports
        where code = :origin or parent_slug = :origin
        )
    and dest_code IN(
        select code
        from ports
        where code = :destination or parent_slug = :destination
        )
    group by day
    order by day asc
    ''', val_map)

    return [{"day":str(row[0]), "average_price": round(row[1]) if row[1]  else None} for row in result]

# Add caching function, because the currencies only update once every hour
api_cache = dict()
def get_api_resp(api):
    prev_resp = api_cache.get(api)
    if prev_resp:
        last_update = datetime.fromtimestamp(prev_resp.get('timestamp'))
        if last_update + timedelta(hours=1) > datetime.now():
            return api_cache[api]

    resp = requests.get(api_config.get('currency', 'openexchangerates'))
    api_cache[api] = resp.json()
    return api_cache[api]

def add_prices_for_daterange(price_data, currency=None):
    price_value = float(price_data.get('price'))
    if currency != None:
        api = api_config.get('currency', 'openexchangerates')
        currency_map = get_api_resp(api)
        if currency not in currency_map.get('rates'):
            return Response(response=f'Invalid currency: "{currency}"', status=400)
        price_value = price_value / currency_map.get('rates').get(currency)

    try:
        date_from = datetime.strptime(price_data.get('date_from') ,'%Y-%m-%d')
        date_to = datetime.strptime(price_data.get('date_to') ,'%Y-%m-%d')
    except ValueError as e:
        return Response(response=str(e), status=400)

    for i in range(int((date_to - date_from).days)+1):
        day = date_from + timedelta(i)
        price = Price(
            orig_code=price_data.get('origin'),
            dest_code=price_data.get('destination'),
            day=day,
            price=int(round(price_value))
            )
        db.session.add(price)
    db.session.commit()

    return {'result': 'success'}
