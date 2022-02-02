#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## get Nico-Jikkyo-Log xml file ##

from __future__ import annotations      # Python3.9以降では不要
import enum
import os
import datetime

# constants
url_api = 'https://jikkyo.tsukumijima.net/'
ts_offset = 18800000        # 100kパケット（約18MiB）

class NetType(enum.IntEnum):
    Other = 0
    BS = enum.auto()
    CS = enum.auto()
    GR = enum.auto()

channel_ids = {
    # たぶん必要ないけど一応副チャンネルも入れておく

    NetType.GR: {
        # 地上波

        # NHK総合
        0x400: 'jk1', 0x401: 'jk1', 0x402: 'jk1', # 0x403: 'jk1', 0x404: 'jk1', 0x405: 'jk1', 0x406: 'jk1', 0x407: 'jk1',
        # NHK Eテレ
        0x408: 'jk2', 0x409: 'jk2', 0x40a: 'jk2', # 0x40b: 'jk2', 0x40c: 'jk2', 0x40d: 'jk2', 0x40e: 'jk2', 0x40f: 'jk2',
        # 日本テレビ
        0x410: 'jk4', 0x411: 'jk4', 0x412: 'jk4', # 0x413: 'jk4', 0x414: 'jk4', 0x415: 'jk4', 0x416: 'jk4', 0x417: 'jk4',
        # テレビ朝日
        0x428: 'jk5', 0x429: 'jk5', 0x42a: 'jk5', # 0x42b: 'jk5', 0x42c: 'jk5', 0x42d: 'jk5', 0x42e: 'jk5', 0x42f: 'jk5',
        # TBS
        0x418: 'jk6', 0x419: 'jk6', 0x41a: 'jk6', # 0x41b: 'jk6', 0x41c: 'jk6', 0x41d: 'jk6', 0x41e: 'jk6', 0x41f: 'jk6',
        # テレビ東京
        0x430: 'jk7', 0x431: 'jk7', 0x432: 'jk7', # 0x433: 'jk7', 0x434: 'jk7', 0x435: 'jk7', 0x436: 'jk7', 0x437: 'jk7',
        # フジテレビ
        0x420: 'jk8', 0x421: 'jk8', 0x422: 'jk8', # 0x423: 'jk8', 0x424: 'jk8', 0x425: 'jk8', 0x426: 'jk8', 0x427: 'jk8',
        # TOKYO MX
        0x5c38: 'jk9', 0x5c39: 'jk9', 0x5c3a: 'jk9', # 0x5c3b: 'jk9', 0x5c3c: 'jk9', 0x5c3d: 'jk9', 0x5c3e: 'jk9', 0x5c3f: 'jk9',
        # テレ玉
        0x7438: 'jk10', 0x7439: 'jk10', 0x743a: 'jk10', # 0x743b: 'jk10', 0x743c: 'jk10', 0x743d: 'jk10', 0x743e: 'jk10', 0x743f: 'jk10',
        # tvk
        0x6038: 'jk11', 0x6039: 'jk11', 0x603a: 'jk11', # 0x603b: 'jk11', 0x603c: 'jk11', 0x603d: 'jk11', 0x603e: 'jk11', 0x603f: 'jk11',
        # チバテレビ
        0x6c38: 'jk12', 0x6c39: 'jk12', 0x6c3a: 'jk12', # 0x6c3b: 'jk12', 0x6c3c: 'jk12', 0x6c3d: 'jk12', 0x6c3e: 'jk12', 0x6c3f: 'jk12',
    },
    NetType.BS: {
        # BS

        # NHK BS1
        101: 'jk101', 102: 'jk101',
        # NHK BSプレミアム
        103: 'jk103', 104: 'jk103',
        # BS日テレ
        141: 'jk141', 142: 'jk141', 143: 'jk141',
        # BS朝日
        151: 'jk151', 152: 'jk151', 153: 'jk151',
        # BS‐TBS
        161: 'jk161', 162: 'jk161', 163: 'jk161',
        # BSテレ東
        171: 'jk171', 172: 'jk171', 173: 'jk171',
        # BSフジ
        181: 'jk181', 182: 'jk181', 183: 'jk181',
        # WOWOWプライム
        191: 'jk191',
        # WOWOWライブ
        192: 'jk192',
        # WOWOWシネマ
        193: 'jk193',
        # BS11
        211: 'jk211',
        # トゥエルビ
        222: 'jk222',
        # BSアニマックス
        236: 'jk236',
    },
    NetType.CS: {
        # CS

        # AT‐X
        333: 'jk333',
    },
}


def get_program_info(path: os.PathLike) -> tuple[NetType, int, datetime.datetime, datetime.timedelta]:
    import ariblib, ariblib.sections, ariblib.descriptors

    with ariblib.tsopen(os.fspath(path)) as ts:

        # PATをもとに自ファイルに含まれるサービスIDを取得する
        # （単一ファイル内に複数のサービス（チャンネル）が含まれ得るので、サービスIDは1つとは限らない）
        def get_service_ids() -> list[int]:
            pat = next(ts.sections(ariblib.sections.ProgramAssociationSection))
            return [pid.program_number for pid in pat.pids if pid.program_number]

        # SDTをもとにサービス種別が「デジタルTVサービス」のサービスを取得する
        # TODO: 複数の候補が見つかる場合の対応（現状は最初に見つけたもの）
        def search_tv_service(sids: list[int]) -> tuple[int, int]:
            for sdt in ts.sections(ariblib.sections.ActualStreamServiceDescriptionSection):
                network_id = sdt.original_network_id
                for svc in sdt.services:
                    if svc.service_id in sids:
                        for desc in svc.descriptors[ariblib.descriptors.ServiceDescriptor]:
                            if desc.service_type == 1:      # 1 == デジタルTVサービス
                                return (network_id, svc.service_id)
            return None

        # ネットワークIDから種類を求める
        def get_network_type(nid: int) -> NetType:
            if nid == 4:
                return NetType.BS
            elif nid in (6, 7):
                return NetType.CS
            elif 0x7880 <= nid <= 0x7fe8:
                return NetType.GR
            else:
                return NetType.Other


        # 録画マージンを考慮して少しズラす
        ts.seek(ts_offset)

        sids = get_service_ids()
        if len(sids) == 0:
            raise RuntimeError('サービスIDが見つかりません')
        elif len(sids) > 1:
            import sys
            print('サービスが複数含まれています', file=sys.stderr)

        sid = search_tv_service(sids)

        for eit in (table for table in ts.sections(ariblib.sections.ActualStreamPresentFollowingEventInformationSection) if table.section_number == 0):
            if eit.service_id == sid[1]:
                ev = next(iter(eit.events))
                stime = ev.start_time
                dur = ev.duration
                break

    return (get_network_type(sid[0]), sid[1], stime, dur)

def get_jikkyo_log(channel_id: str, start_time: datetime.datetime, end_time: datetime.datetime) -> str:
    import requests

    params = {
        'starttime': str(int(start_time.timestamp())),
        'endtime': str(int(end_time.timestamp())),
        'format': 'xml'
    }
    xml = requests.get(f'{url_api}/api/kakolog/{channel_id}', params=params)
    return xml.text


### ENTRY POINT ###
if __name__ == '__main__':
    import sys
    import pathlib

    for arg in sys.argv[1:]:
        try:
            ifile = pathlib.Path(arg).resolve(True)

            print(ifile.name)

            ntype, sid, stime, dur = get_program_info(ifile)
            log = get_jikkyo_log(channel_ids[ntype][sid], stime, stime + dur)

            err = None
            try:
                import xml.etree.ElementTree as ET
                xml = ET.fromstring(log)
                if xml.tag == 'error':
                    err = xml.text
            except ET.ParseError:
                # URLに関する問題の時は（formatが不確定なので）jsonで返ってくることがある
                import json
                js = json.loads(log)
                err = js.get('error', None)
            if err:
                raise RuntimeError(err)

            ofile = ifile.with_suffix('.xml')
            #ofile.write_text(log, encoding='utf-8', newline='') # newlineはPython3.10から
            ofile.write_text(log, encoding='utf-8')             # 改行がCRLFに変わる

        except Exception as e:
            print(type(e), e)
