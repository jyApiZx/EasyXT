from datetime import datetime
import logging

import pandas as pd
import pytest

from easy_xt.data_api import DataAPI, minute_download_range
from easy_xt.data_types import DataError


def test_explicit_range_is_not_truncated():
    assert minute_download_range('20260901', '20260914', '1m', None) == (
        '20260901', '20260914'
    )


def test_count_window_uses_query_end_and_grows_with_count():
    short_start, short_end = minute_download_range(None, '20260914', '1m', 100)
    long_start, long_end = minute_download_range(None, '20260914', '1m', 3000)
    assert short_end == long_end == '20260914'
    assert short_start < '20260911'  # Never silently use just three days.
    assert long_start < short_start


def test_default_window_is_not_a_multiyear_download():
    start, end = minute_download_range(None, None, '5m', None,
                                       now=datetime(2026, 9, 14))
    assert (start, end) == ('20260904', '20260914')


@pytest.mark.parametrize('count', [0, -1, True])
def test_invalid_count_is_rejected(count):
    with pytest.raises(ValueError, match='count'):
        minute_download_range(None, '20260914', '1m', count)


def test_qmt_count_download_logs_range_and_does_not_claim_data_success(caplog):
    api = DataAPI.__new__(DataAPI)
    api.xt = object()
    api._connected = True
    calls = []

    def fake_call(method, **kwargs):
        calls.append((method, kwargs))
        if method == 'get_market_data_ex':
            return {'002714.SZ': pd.DataFrame()}
        return None

    api._call_qmt = fake_call
    caplog.set_level(logging.INFO, logger='easy_xt.data_api')
    with pytest.raises(DataError, match='请求区间'):
        api._get_price_qmt(['002714.SZ'], None, '20260914', '1m', 100, None, 'none')

    download = next(kwargs for method, kwargs in calls
                    if method == 'download_history_data2')
    assert download['end_time'] == '20260914'
    assert download['start_time'] < '20260911'
    assert len([method for method, _ in calls if method == 'get_market_data_ex']) == 2
    assert '下载请求已返回' in caplog.text
    assert '历史数据下载完成' not in caplog.text


def test_qmt_explicit_minute_query_downloads_full_requested_range():
    api = DataAPI.__new__(DataAPI)
    api.xt = object()
    api._connected = True
    calls = []

    def fake_call(method, **kwargs):
        calls.append((method, kwargs))
        return {'002714.SZ': pd.DataFrame()} if method == 'get_market_data_ex' else None

    api._call_qmt = fake_call
    with pytest.raises(DataError, match='20260901 至 20260914'):
        api._get_price_qmt(['002714.SZ'], '20260901', '20260914',
                           '5m', None, None, 'none')

    download = next(kwargs for method, kwargs in calls
                    if method == 'download_history_data2')
    assert (download['start_time'], download['end_time']) == (
        '20260901', '20260914'
    )


def test_fallback_error_preserves_qmt_failure_reason():
    api = DataAPI.__new__(DataAPI)
    api._active_source = 'qmt'
    api._tdx_provider = None
    api._eastmoney_provider = object()
    api._get_price_qmt = lambda *args: (_ for _ in ()).throw(
        DataError('QMT请求区间 20260901 至 20260914 后仍无K线')
    )
    api._get_price_eastmoney = lambda *args: (_ for _ in ()).throw(
        DataError('代理连接失败')
    )
    with pytest.raises(DataError) as error:
        api.get_price(['002714.SZ'], period='1m', count=100)
    assert 'QMT请求区间 20260901 至 20260914' in str(error.value)
    assert '代理连接失败' in str(error.value)
