# coding=utf-8
import os
from ctypes import WinDLL, c_int, c_short, c_float, c_char_p, create_string_buffer

import pandas as pd


def gbk(text):
    if text is None:
        text = ""
    if isinstance(text, bytes):
        return text
    return str(text).encode("gbk", errors="replace")


def decode(buf):
    return buf.raw.split(b"\x00", 1)[0].decode("gbk", errors="replace")


def parse_tsv(text):
    text = (text or "").strip()
    if not text or "\t" not in text:
        return []
    lines = [line for line in text.split("\n") if line]
    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        cols = line.split("\t")
        rows.append({header[i] if i < len(header) else str(i): cols[i] if i < len(cols) else "" for i in range(max(len(header), len(cols)))})
    return rows


class DllTrade(object):
    def __init__(self):
        self.dll = WinDLL(os.environ.get("THSAPI_DLL", "thsapi.dll"))
        self.client_id = -1
        self.account = "YOUR_ACCOUNT"
        self._bind()
        self.dll.Init()

    def _bind(self):
        d = self.dll
        self.logon = d.Logon
        self.logon.argtypes = [c_char_p, c_short, c_char_p, c_short, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p]
        self.logon.restype = c_int
        self.logoff = d.Logoff
        self.logoff.argtypes = [c_int]
        self.query = d.QueryData
        self.query.argtypes = [c_int, c_int, c_char_p, c_char_p]
        self.query.restype = c_int
        self.send = d.SendOrder
        self.send.argtypes = [c_int, c_int, c_int, c_char_p, c_char_p, c_float, c_int, c_char_p, c_char_p]
        self.cancel = d.CancelOrder
        self.cancel.argtypes = [c_int, c_char_p, c_char_p, c_char_p, c_char_p]

    def connect(self, ip="YOUR_BROKER_IP", port=0, account="YOUR_ACCOUNT", password="YOUR_PASSWORD"):
        self.account = account
        err = create_string_buffer(256)
        self.client_id = self.logon(gbk(ip), int(port), gbk('{"account_type":0}'), 0, gbk(account), gbk(account), gbk(password), gbk(""), err)
        return self.client_id >= 0

    def add_account(self, account_id, account_type="STOCK"):
        self.account = account_id
        return self.client_id >= 0

    def _query(self, category):
        result = create_string_buffer(1024 * 1024)
        err = create_string_buffer(256)
        code = self.query(self.client_id, int(category), result, err)
        if code != 0:
            return []
        return parse_tsv(decode(result))

    def buy(self, account_id, code, volume, price=0, price_type="limit"):
        return self._order(code, price, volume, 0)

    def sell(self, account_id, code, volume, price=0, price_type="limit"):
        return self._order(code, price, volume, 1)

    def _order(self, code, price, volume, category):
        result = create_string_buffer(1024 * 1024)
        err = create_string_buffer(256)
        self.send(self.client_id, int(category), 0, gbk(""), gbk(str(code).split(".")[0]), float(price), int(volume), result, err)
        text = decode(result).strip()
        if decode(err).strip():
            return None
        digits = "".join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else 0

    def cancel_order(self, account_id, order_id):
        result = create_string_buffer(1024 * 1024)
        err = create_string_buffer(256)
        self.cancel(self.client_id, gbk("1"), gbk(order_id), result, err)
        return not decode(err).strip()

    def get_account_asset(self, account_id):
        rows = self._query(0)
        return rows[0] if rows else {}

    def get_positions(self, account_id, code=""):
        rows = self._query(1)
        if code:
            bare = str(code).split(".")[0]
            rows = [row for row in rows if bare in "".join(row.values())]
        return pd.DataFrame(rows)

    def get_orders(self, account_id, cancelable_only=False):
        return pd.DataFrame(self._query(4 if cancelable_only else 2))

    def get_trades(self, account_id):
        return pd.DataFrame(self._query(3))
