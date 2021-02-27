
from flask import Blueprint, request, jsonify, Response
from app.models import db, get_rates, add_prices_for_daterange
from functools import wraps

main = Blueprint('main', __name__)

def input_validation(required_params):
    def decorator(f):
        @wraps(f)
        def decorated_function():
            params = request.args if request.method == "GET" else request.get_json()
            for param_key in required_params:
                param_value = params.get(param_key)
                if param_value == None:
                    message = f'Missing required parameter "{param_key}"'
                    return Response(response=message, status=400)
                if param_key != 'price' and not isinstance(param_value, str):
                    message = f'Invalid parameter "{param_key} = {param_value}" needs to be a string'
                    return Response(response=message, status=400)
                elif param_key == 'price' and not str(param_value).isnumeric():
                    message = f'Invalid parameter "{param_key} = {param_value}" needs to be a number'
                    return Response(response=message, status=400)
            return f(params)
        return decorated_function
    return decorator

@main.route('/')
def health_check():
    return 'The server is running!'

@main.route('/rates', methods=['GET'])
@input_validation(['date_from', 'date_to', 'origin', 'destination'])
def rates(params):
    result = get_rates(params)
    
    return jsonify(result)

@main.route('/rates_null', methods=['GET'])
@input_validation(['date_from', 'date_to', 'origin', 'destination'])
def rates_null(params):
    result = get_rates(params, 3)
    
    return jsonify(result)

@main.route('/price', methods=['POST'])
@input_validation(['date_from', 'date_to', 'origin', 'destination', 'price'])
def add_price(params):
    currency = request.form.get("currency")
    
    return add_prices_for_daterange(params, currency)