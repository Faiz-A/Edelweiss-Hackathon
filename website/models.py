from . import db

class Options(db.Model):
    primary = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50))
    c_iv = db.Column(db.DECIMAL(precision=5,scale=2),default=0)
    strike = db.Column(db.Integer)
    exp = db.Column(db.String(50))
    c_timestamp = db.Column(db.String(50),default=0)
    c_ltp = db.Column(db.Integer,default=0)
    c_volume = db.Column(db.Integer,default=0)
    c_bprice = db.Column(db.Integer,default=0)
    c_bquantity = db.Column(db.Integer,default=0)
    c_askp = db.Column(db.Integer,default=0)
    c_askq = db.Column(db.Integer,default=0)
    c_oi = db.Column(db.Integer,default=0)
    c_changecp = db.Column(db.Integer,default=0)
    c_changeoi = db.Column(db.Integer,default=0)
    p_iv = db.Column(db.DECIMAL(precision=5, scale=2), default=0)
    p_timestamp = db.Column(db.String(50),default=0)
    p_ltp = db.Column(db.Integer,default=0)
    p_volume = db.Column(db.Integer,default=0)
    p_bprice = db.Column(db.Integer,default=0)
    p_bquantity = db.Column(db.Integer,default=0)
    p_askp = db.Column(db.Integer,default=0)
    p_askq = db.Column(db.Integer,default=0)
    p_oi = db.Column(db.Integer,default=0)
    p_changecp = db.Column(db.Integer,default=0)
    p_changeoi = db.Column(db.Integer,default=0)
    latest = db.Column(db.String(5),default=0)

class Underlying(db.Model):
    primary = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50))
    timestamp = db.Column(db.Integer)
    ltp = db.Column(db.Integer)
    pcp = db.Column(db.Integer)

class Futures(db.Model):
    primary = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50))
    exp = db.Column(db.String(20))
    timestamp = db.Column(db.Integer)
    ltp = db.Column(db.Integer)
    ltq = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    bprice = db.Column(db.Integer)
    bquantity = db.Column(db.Integer)
    askp = db.Column(db.Integer)
    askq = db.Column(db.Integer)
    oi = db.Column(db.Integer)
    pcp = db.Column(db.Integer)
    poi = db.Column(db.Integer)

