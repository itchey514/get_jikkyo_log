# Windowsでファイルをドラッグ&ドロップで実行する方法メモ

- 公式インストーラーでPythonを入れた場合は「Pythonランチャー」（`py.exe`）を使えばよいので特に問題なし

- Anaconda経由で入れた場合は↑が使えないので、ショートカットを作るとよい
	|項目|値|
	|:---|:---|
	|リンク先|`%windir%\System32\cmd.exe /S /C (Anacondaのインストール先)\Scripts\activate.bat %USERPROFILE%\.conda\envs\(環境名) && python get_jikkyo_log.py`|
	|作業フォルダー|`(get_jikkyo_log.pyのあるフォルダ)`|
	|実行時の大きさ|最小化|

- いっそexe化する
	- [PyInstaller](http://www.pyinstaller.org/)
	- [Nuitka](https://nuitka.net/)
		- tsukumi氏による紹介記事⇒[PyInstallerより圧倒的に優れているNuitkaの使い方とハマったポイント](https://blog.tsukumijima.net/article/python-nuitka-usage/ "つくみ島だより")
