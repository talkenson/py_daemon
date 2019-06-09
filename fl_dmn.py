from flask import Flask, request, Response
from multiprocessing import Process, Queue, Manager
import os
import sys
from time import sleep
import time
from json import dumps, loads
import json
import requests as req
import traceback
from flask_cors import CORS
from lxml import html
import re
import math


app = Flask(__name__)
CORS(app)
plugins = {}

workers_number = 2
workers = []
queue = Queue()

methods_name = []


@app.route('/bwd.decode/<string:phrase>') # BWD - Binary Word Decoder
def bwd_decode(phrase):
    _a_code = ord('a')
    mess_d = ''
    mess = [int(i) for i in re.split('-| ',phrase)]
    for chunk in mess:
        for dem in range(0,26):
            if chunk & 2**dem == 2**dem:
                mess_d += chr(_a_code + dem)
                #print('Worked with ', dem)

    return Response(mess_d, mimetype='text/plain')

@app.route('/bwd.encode/<string:phrase>') # BWD - Binary Word Decoder
def bwd_encode(phrase):
    _a_code = ord('a')
    mess_e = ''
    mess = [str(i) for i in re.split('-| |, |,',phrase)]
    l_code=0
    for chunk in mess:
        for sym in chunk.lower():
            if 2**(ord(sym)-_a_code) > l_code:
                l_code += 2**(ord(sym)-_a_code)
                #print(sym, 'added to ', l_code)
            else:
                mess_e += str(l_code)+'-'
                l_code=0
                l_code += 2**(ord(sym)-_a_code)
                #print(sym, 'added to ', l_code)
    mess_e += str(l_code)

    return Response(mess_e, mimetype='text/plain')






if __name__ == '__main__':

    app.run('0.0.0.0', port=9797, debug=False)
