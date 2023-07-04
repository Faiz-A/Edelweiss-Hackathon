#from main import app
from website import create_app
from flask import request, jsonify
from website.models import Options, Underlying

app = create_app()

@app.route('/api/options', methods=['GET'])
def get_options_data():
    symbol = request.args.get('symbol')
    expiry = request.args.get('expiry')


    if symbol:
        if expiry:
            options_data = Options.query.filter_by(symbol=symbol,exp=expiry).order_by(Options.strike).all()
        else:
            options_data = Options.query.filter_by(symbol=symbol).order_by(Options.strike).all()
    else:
        options_data = Options.query.all()
    data = [
        {
            'symbol': option.symbol,
            'c_iv': option.c_iv,
            'strike': option.strike,
            'exp': option.exp,
            'c_ltp': option.c_ltp,
            'c_volume': option.c_volume,
            'c_bprice': option.c_bprice,
            'c_bquantity': option.c_bquantity,
            'c_askp': option.c_askp,
            'c_askq': option.c_askq,
            'c_oi': option.c_oi,
            'c_changecp': option.c_changecp,
            'c_changeoi': option.c_changeoi,
            'p_iv': option.p_iv,
            'p_ltp': option.p_ltp,
            'p_volume': option.p_volume,
            'p_bprice': option.p_bprice,
            'p_bquantity': option.p_bquantity,
            'p_askp': option.p_askp,
            'p_askq': option.p_askq,
            'p_oi': option.p_oi,
            'p_changecp': option.p_changecp,
            'p_changeoi': option.p_changeoi,
        }
        for option in options_data
    ]
    return jsonify(data)

@app.route('/api/symbols', methods=['GET'])
def get_symbols():
    symbols = [underlying.symbol for underlying in Underlying.query.distinct(Underlying.symbol)]
    return jsonify(symbols)


@app.route('/api/expiry', methods=['GET'])
def get_expiry_dates():
    symbol = request.args.get('symbol')

    if symbol is None:
        expiryDates = [option.exp for option in Options.query.distinct(Options.exp)]
        return jsonify(expiryDates)

    expiry_dates = [option.exp for option in Options.query.filter(Options.symbol == symbol).distinct(Options.exp)]
    return jsonify(expiry_dates)

@app.route('/api/underlying', methods=['GET'])
def get_underlying():
    symbol = request.args.get('symbol')

    if symbol is None:
        underlying = 0
        return jsonify(underlying)

    underlying = [Underlying.query.filter(symbol=symbol).ltp]
    return jsonify(underlying)
