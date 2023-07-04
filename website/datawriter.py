from . import data_queue,db
from datetime import datetime
from .models import Options,Underlying,Futures
from .api import app



def convert_date(date_str):

    date_obj = datetime.strptime(date_str, '%d%b%y')
    formatted_date = date_obj.strftime('%d-%m-%Y')

    return formatted_date


def data_update():

    while True:
        if data_queue.qsize() > 0:
            with app.app_context():
                data = data_queue.get()
                try:
                    PacketLength, BankName, ExpDate, StrikePrice, OptionType, SeqNo, Timestamp, LTP, LTQ, Vol, BPrice, BQuantity, AskP, AskQ, OI, PCP, POI = data
                    datime = datetime.fromtimestamp(Timestamp / 1000)
                    formatted_time = datime.strftime('%Y-%m-%d %H:%M:%S')
                    if OptionType != "XX":
                        underlying = Underlying.query.filter_by(symbol=BankName).first()
                        option = Options.query.filter_by(strike=StrikePrice, exp=convert_date(ExpDate)).first()
                        if OptionType == "PE":
                            if option:
                                option.symbol = BankName
                                option.c_timestamp = formatted_time
                                option.c_ltp = LTP
                                option.c_volume = Vol
                                option.c_bprice = BPrice
                                option.c_bquantity = BQuantity
                                option.c_askp = AskP
                                option.c_askq = AskQ
                                option.c_oi = OI
                                option.c_pcp = PCP
                                option.c_poi = POI
                                option.c_latest = 'Yes'
                                db.session.commit()

                            else:
                                db.session.add(Options(symbol=BankName, c_iv=0, strike=StrikePrice, exp=convert_date(ExpDate), c_timestamp=formatted_time, c_ltp=LTP, c_volume=Vol, c_bprice=BPrice, c_bquantity=BQuantity, c_askp=AskP, c_askq=AskQ, c_oi=OI, c_changecp=PCP, c_changeoi=POI, latest='Yes'))
                                db.session.commit()

                        else:
                            if option:
                                option.symbol = BankName
                                option.p_strike = StrikePrice
                                option.p_timestamp = formatted_time
                                option.p_ltp = LTP
                                option.p_volume = Vol
                                option.p_bprice = BPrice
                                option.p_bquantity = BQuantity
                                option.p_askp = AskP
                                option.p_askq = AskQ
                                option.p_oi = OI
                                option.p_pcp = PCP
                                option.p_poi = POI
                                option.p_latest = 'Yes'
                                db.session.commit()

                            else:
                                db.session.add(Options(symbol=BankName, p_iv=0, strike=StrikePrice, exp=convert_date(ExpDate), p_timestamp=formatted_time, p_ltp=LTP, p_volume=Vol, p_bprice=BPrice, p_bquantity=BQuantity, p_askp=AskP, p_askq=AskQ, p_oi=OI, p_changecp=PCP, p_changeoi=POI, latest='Yes'))
                                db.session.commit()

                    else:

                        future = Futures.query.filter_by(symbol=BankName, exp=ExpDate).first()
                        if future:
                            future.symbol = BankName
                            future.exp = convert_date(ExpDate)
                            future.timestamp = formatted_time
                            future.ltp = LTP
                            future.ltq = LTQ
                            future.volume = Vol
                            future.bprice = BPrice
                            future.bquantity = BQuantity
                            future.askp = AskP
                            future.askq = AskQ
                            future.oi = OI
                            future.pcp = PCP
                            future.poi = POI
                            db.session.commit()

                        else:
                            db.session.add(Futures(symbol=BankName,exp=convert_date(ExpDate),timestamp=formatted_time,ltp=LTP,ltq=LTQ,volume=Vol,bprice=BPrice,bquantity=BQuantity,askp=AskP,askq=AskQ,oi=OI,pcp=PCP,poi=POI))
                            db.session.commit()


                except:
                    BankName,Timestamp,LTP,PCP=data
                    underlying = Underlying.query.filter_by(symbol=BankName).first()
                    if underlying:
                        underlying.symbol = BankName
                        underlying.timestamp = Timestamp
                        underlying.ltp = LTP
                        underlying.pcp = PCP
                        db.session.commit()

                    else:
                        db.session.add(Underlying(symbol=BankName,timestamp=Timestamp, ltp=LTP, pcp=PCP))
                        db.session.commit()
        else:
            continue
