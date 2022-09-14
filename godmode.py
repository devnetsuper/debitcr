#godmode.py
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from openpyxl import load_workbook
from datetime import datetime
import requests
import APIS as api

class Token:
    def __init__(self, symbol, multiplier, api_link='', api_key=''):
        self.symbol = symbol
        self.multiplier = multiplier
        self.api_link = api_link
        self.api_key = api_key

SCAN_ASSETS = {
    'ETH',
    'AVAX',
    'BNB',
    'MATIC',
    'FTM',
    'USDT',
}            

SCAN_APIS = [
    Token('ETH', 1e18, 'etherscan.io', 'XQBQNA7X7Z8BU41N9DZ5WUGT5E7YSFF15M'),
    Token('MATIC', 1e18, 'polygonscan.com', 'FD9PJJDSJ6JX3K2ZKWJIWRJMEWXEBG31QU'),
    Token('BNB', 1e8, 'bscscan.com', 'IG49A7A5VG6SEA2ZBSDEH2NXRHTNDN93B2'),
    Token('AVAX', 1e18, 'snowtrace.io', 'RS48JWVWEP5UYSE79S3XRJACW9DYJCTEDU'),
    Token('FTM', 1e18, 'ftmscan.com', 'ZPCF593WU8S5J7E3VRMKRGBK44NEAEETAU')
]

CHAIR_APIS = {
    'BCH': Token('BCH', 1e8, 'bitcoin-cash'),
    'DOGE': Token('DOGE', 1e8, 'dogecoin'),
    'BTC': Token('BTC', 1e8, 'bitcoin'),
    'BSV': Token('BSV', 1e8, 'bitcoin-sv'),
    'ZEC': Token('ZEC', 1e8, 'zcash'),
    'LTC': Token('LTC', 1e8, 'litecoin'),
    'DASH': Token('DASH', 1e8, 'dash'),
}

def set_output_dir():
    output_dir.set(filedialog.askdirectory())
   
def generate_excel():
    progress_message.set("Attempting to retrieve transactions")
    asset = asset_entry.get().upper()
    address = address_entry.get()
   
    success = False
    if asset in SCAN_ASSETS:
        for token in SCAN_APIS:
            if api.scan_call(token, address, output_dir=dir_entry.get()):
                success = True
                break
    elif asset in CHAIR_APIS:
        success = api.chair_call(CHAIR_APIS[asset.upper()], address, output_dir=dir_entry.get())
       
    elif asset == 'ALGO':
        success = api.algo_call(Token('ALGO', 1e6), address, output_dir=dir_entry.get())
       
    if success:
        progress_message.set(f'Transactions retrieved successfully as of {datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")}')
    else:
        progress_message.set("Transactions Retrieval Failed")

window = tk.Tk()
window.title("Asset Analyzer")

tk.Label(window, text="Asset", borderwidth=1).grid(row=0, column=0)
tk.Label(window, text="Address", borderwidth=1).grid(row=0, column=1)

asset_entry = tk.Entry(width=10)
address_entry = tk.Entry(width=100)

asset_entry.grid(row=1, column=0)
address_entry.grid(row=1, column=1)

output_dir = tk.StringVar()
dir_entry = tk.Entry(width=75, state=DISABLED, textvariable=output_dir)
dir_entry.grid(row=2, column=0)

progress_message = tk.StringVar()
progress_entry = tk.Entry(width=100, state=DISABLED, textvariable=progress_message)
progress_entry.grid(row=2, column=1)


setdir_button = tk.Button(text="Set Output Directory", command=set_output_dir)
setdir_button.grid(row=3, column=0)

genxl_button = tk.Button(text="Generate Excel", command=generate_excel)
genxl_button.grid(row=3, column=1)

window.mainloop()