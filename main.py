from website import data_queue
from website.datawriter import data_update
from website.iv_manager import iv_writer
import socket
import struct
from datetime import datetime
import re
import time
import threading
from website.api import app








def receive_data(client_socket):
    data = b''
    while True:
        chunk = client_socket.recv(130)
        if not chunk:
            break
        PacketLength,TradingSymbol,SeqNo,Timestamp,LTP,LTQ,Vol,BPrice,BQuantity,AskP,AskQ,OI,PCP,POI = struct.unpack('<i30sqqqqqqqqqqqq', chunk)
        datime=datetime.fromtimestamp(Timestamp/1000)
        formatted_time = datime.strftime('%Y-%m-%d %H:%M:%S')


        try:
            stringTraining = TradingSymbol.decode('utf-8', 'ignore').split('\x00')[0]
            try:
                match = re.match(r'^([A-Z]+)(\d{2}[A-Z]+\d{2})(\d+)([A-Z]+)$', stringTraining)
                BankName = match.group(1)
                ExpDate = match.group(2)
                StrikePrice = match.group(3)
                OptionType = match.group(4)
                data_queue.put((PacketLength, BankName, ExpDate, StrikePrice, OptionType, SeqNo, Timestamp, LTP, LTQ, Vol,
                                BPrice, BQuantity, AskP, AskQ, OI, PCP, POI))
            except:
                match = re.match(r'^([A-Z]+)(\d{2}[A-Z]+\d{2})([A-Z]+)$', stringTraining)
                BankName = match.group(1)
                ExpDate = match.group(2)
                StrikePrice = 0
                OptionType = match.group(3)
                data_queue.put(
                    (PacketLength, BankName, ExpDate, StrikePrice, OptionType, SeqNo, Timestamp, LTP, LTQ, Vol,
                     BPrice, BQuantity, AskP, AskQ, OI, PCP, POI))


        except:
            stringTraining = TradingSymbol.decode('utf-8', 'ignore').split('\x00')[0]
            match = re.match(r'^([A-Z]+)$', stringTraining)
            BankName = match.group(0)
            data_queue.put((BankName,Timestamp,LTP,PCP))



def start_socket():
    server_ip = 'localhost'
    server_port = 8080

    try:
        time.sleep(1)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 3600)
        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3600)
        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)



        market_data_bytes = b'h'
        client_socket.send(market_data_bytes)

        while True:
            receive_data(client_socket)

    except ConnectionRefusedError:
        print('Connection refused. Make sure the server is running.')
    except Exception as e:
        print(f'Error occurred: {e}')




if __name__ == '__main__':
    socket_thread = threading.Thread(target=start_socket)
    socket_thread.start()
    process_thread = threading.Thread(target=data_update)
    process_thread.start()
    iv_thread = threading.Thread(target=iv_writer)
    iv_thread.start()
    app.run()

