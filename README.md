# EasyXT

# 通达信/同花顺纯协议接口

**提供通达信/同花顺纯协议接口，支持大部分券商。接入请联系 Telegram：`JyApi888`。**

完整函数表和各语言示例见 [stockapi](https://github.com/jyApiZx/stockapi)。

按 EasyXT 的 `init_trade`、`buy`、`sell` 写策略。交易连接到 `Api.dll`，不再连接 QMT 或 miniQMT。

已有 EasyXT 策略保留原来的函数名即可。券商覆盖、L2 行情和逐笔数据都由这一份 DLL 提供。

## Api.dll

面向 A 股的交易和行情库，支持大部分券商。

| 能力 | 说明 |
| --- | --- |
| 券商交易 | 登录、资金、持仓、当日委托、当日成交、买入、卖出、撤单 |
| A 股行情 | K 线、分时、实时报价 |
| L2 | 十档、逐笔成交、逐笔委托 |
| 扩展行情 | 期货、期权等 |

DLL 与函数说明见 [stockapi](https://github.com/jyApiZx/stockapi)。

进程位数须与 `Api.dll` 一致。查询结果为 GBK 文本。

## 交易

```python
from easy_xt import EasyXT

api = EasyXT()
api.init_trade(
    "YOUR_BROKER_IP",
    account="YOUR_ACCOUNT",
    password="YOUR_PASSWORD",
    port=0,
)

api.buy("YOUR_ACCOUNT", "000001.SZ", 100, 10.0, "limit")
api.sell("YOUR_ACCOUNT", "000001.SZ", 100, 10.5, "limit")
api.cancel_order("YOUR_ACCOUNT", 委托编号)

api.get_account_asset("YOUR_ACCOUNT")
api.get_positions("YOUR_ACCOUNT")
api.get_orders("YOUR_ACCOUNT")
api.get_trades("YOUR_ACCOUNT")
```

`init_trade` 的第一个参数是券商交易地址。买入、卖出返回委托编号。

## 仓库里保留的其它部分

回测、图形界面和 Tushare 数据文件仍在仓库中，方便对照原来的策略结构。实盘下单、撤单和账户查询走 `Api.dll`。

## 说明

调用风格来自 EasyXT。交易由 `Api.dll` 完成。许可证见 [LICENSE](LICENSE)。
