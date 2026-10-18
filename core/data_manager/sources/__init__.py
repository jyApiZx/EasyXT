# -*- coding: utf-8 -*-
"""
数据源模块

提供各个数据源的实现，支持：
- DuckDB本地数据库
- Tushare在线API
- QMT历史数据
- BaoStock免费历史数据
- FTShare云行情及财务数据
"""

from .base_source import BaseDataSource
from .duckdb_source import DuckDBSource
from .tushare_source import TushareSource
from .qmt_source import QMTSource
from .baostock_source import BaoStockSource
from .ftshare_source import FTShareSource

__all__ = ['BaseDataSource', 'DuckDBSource', 'TushareSource', 'QMTSource', 'BaoStockSource', 'FTShareSource']
