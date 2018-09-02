import pandas as pd
import multiprocessing
import json

from flask import Response


def parse_resp(data, success=True):
    return Response(json.dumps({
        'success': success,
        'data': data
    }), mimetype='application/json')


class StockUtils(object):
    _cache_symbols = set()
    _cached_infos = set()

    @staticmethod
    def get_stock_symbols():
        if not StockUtils._cache_symbols:
            csv_data = pd.read_csv('stock_code.csv')
            StockUtils._cache_symbols = list(map(lambda x: x[1], csv_data.values))
        return StockUtils._cache_symbols

    @staticmethod
    def get_stock_infos():
        if not StockUtils._cached_infos:
            csv_data = pd.read_csv('stock_code.csv')
            StockUtils._cached_infos = list(map(lambda x: {
                'symbol': x[1],
                'title': x[2],
                'date': x[-2]
            }, csv_data.values))
        return StockUtils._cached_infos

    @staticmethod
    def clear_cache():
        StockUtils._cache_symbols = set()


class ManagedProcess(object):
    _process_map = {}

    @staticmethod
    def create_process(name, handler, args=(), kwargs={}):
        if name not in ManagedProcess._process_map:
            ManagedProcess._process_map[name] = \
                multiprocessing.Process(target=handler, name=name, args=args, kwargs=kwargs)
        ManagedProcess._process_map[name].daemon = True
        ManagedProcess._process_map[name].start()
        return ManagedProcess._process_map[name]

    @staticmethod
    def remove_process(name):
        if name not in ManagedProcess._process_map:
            raise RuntimeError('%s not in the process map' % name)
        ManagedProcess._process_map[name].terminate()
        del ManagedProcess._process_map[name]

    @staticmethod
    def is_process_existed(name):
        return name in ManagedProcess._process_map


class SyncProcessHelper(object):

    @staticmethod
    def add_sync_record(record):
        pass