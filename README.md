# EasyXT

按原来的 `init_trade`、`buy`、`sell` 写策略。`init_trade` 仍然连接 QMT。

客户端和下单通道慢，也容易漏单、错单。要纯协议直接连券商，用 `init_trade_thsapi`，加载 `thsapi.dll`。不用开着同花顺或通达信客户端。下单、撤单和查询走 DLL。

交易包：[64 位](https://github.com/jyApiZx/stockapi/releases/download/v1.0.2/thsapi_1.0.2_x64.zip)、[32 位](https://github.com/jyApiZx/stockapi/releases/download/v1.0.2/thsapi_1.0.2_x32.zip)。调用说明见 [stockapi](https://github.com/jyApiZx/stockapi)。

## 纯协议

```python
from easy_xt import EasyXT

api = EasyXT()
api.init_trade_thsapi("trade.10jqka.com.cn", 8002, account="YOUR_ACCOUNT", password="YOUR_PASSWORD")
```

模拟账户先把查询、下单和撤单跑通。程序位数要和 `thsapi.dll` 一致。
