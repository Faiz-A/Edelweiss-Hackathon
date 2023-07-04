from .models import Options,Underlying
from .iv import implied_volatility_call,implied_volatility_put
from . import db
from .api import app
from datetime import datetime

def time_to_maturity(expiration_date, current_date=None):

    if current_date is None:
        current_date = datetime.now()


    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, '%d-%m-%Y')
    if isinstance(expiration_date, str):
        expiration_date = datetime.strptime(expiration_date, '%d-%m-%Y')


    time_to_maturity_days = (expiration_date - current_date).days


    time_to_maturity_years = time_to_maturity_days / 365.0

    return time_to_maturity_years

def iv_writer():
    while True:
        with app.app_context():
            all_options = Options.query.all()
            for option in all_options:

                underlying_price = Underlying.query.filter_by(symbol=option.symbol).first().ltp
                mtime = time_to_maturity(option.exp)
                if underlying_price != 0:
                    if option.c_ltp != 0:
                        civ= implied_volatility_call(option.c_ltp,option.strike,underlying_price,mtime,0.5)
                        option.c_iv = civ

                    if option.p_ltp != 0:
                        piv = implied_volatility_put(option.p_ltp, option.strike, underlying_price, mtime, 0.5)
                        option.p_iv = piv


                    db.session.commit()
                else:
                    continue