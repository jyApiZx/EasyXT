# EasyXT

# 同花顺交易接口

**同花顺交易接口，L1、L2 行情接口。直连券商，无需启动客户端，支持大部分券商。产品介绍见 [thsapi.com](https://thsapi.com/)。技术支持请联系 [Telegram：@Thsapi](https://t.me/Thsapi)**

不点屏幕，不抢鼠标，程序直接连券商。下载后用模拟盘就能测查询、下单和撤单。已经有项目时，打开 [AI 代做提示词](https://thsapi.com/ai.html)，把提示词交给正在改项目的 AI。行情有 L1，也有十档、买卖队列和逐笔。

账户安全说明：接口不上传交易密码、持仓、委托或成交；本地授权不连接授权服务器。价格和开通方式见 [官网授权方式](https://thsapi.com/#license)。完整的联网范围、安全测试和自行核验方法见 [账户安全与授权](https://thsapi.com/security.html)。

按原来的 `init_trade`、`buy`、`sell` 写策略。`init_trade` 仍然连接 QMT。

客户端和下单通道慢，也容易漏单、错单。要用同花顺交易接口直接连券商，用 `init_trade_thsapi`，加载 `thsapi.dll`。不用开着同花顺或通达信客户端。下单、撤单和查询走 DLL。

交易包：[64 位](https://github.com/jyApiZx/stockapi/releases/download/v1.0.6.1/thsapi_1.0.6.1_x64.zip)、[32 位](https://github.com/jyApiZx/stockapi/releases/download/v1.0.6.1/thsapi_1.0.6.1_x32.zip)。调用说明见 [stockapi](https://github.com/jyApiZx/stockapi)。

## 同花顺交易接口

```python
from easy_xt import EasyXT

api = EasyXT()
api.init_trade_thsapi("trade.10jqka.com.cn", 8002, account="YOUR_ACCOUNT", password="YOUR_PASSWORD")
```

模拟账户先把查询、下单和撤单跑通。程序位数要和 `thsapi.dll` 一致。
