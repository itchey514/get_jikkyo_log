# get_jikkyo_log.py
tsukumi氏が公開されているニコニコ実況過去ログAPI（[https://jikkyo.tsukumijima.net/](https://jikkyo.tsukumijima.net/)）を利用し、TSファイルの過去ログを取得するスクリプト

## 使い方
```console
$ python3 get_jikkyo_log.py file1.ts [file2.ts ...]
```
入力ファイルと同じ場所に同名で拡張子を「.xml」に変更したファイルが出力される。  
（既に存在する場合は上書き。）

## 動作確認環境
- Windows版Python 3.9.7 [^1]（[Anaconda](https://repo.anaconda.com/)）
- ariblib 0.0.5（[PyPI](https://pypi.org/project/ariblib/)）

[^1]: Python 3.9.7 (default, Sep 16 2021, 16:59:28) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
