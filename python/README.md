# Python3環境の構築

この章では、はじめに、前章で扱ったubuntu:18.04のイメージからpython3が動作する環境を構築する。ubuntu:18.04のイメージにはpython3はインストールされていないため、python3をインストールすることから始める。その後に、Docker Hubで公開されているpythonイメージを利用する方法を紹介する。また、pythonイメージを用いたjupyter環境の構築も行う。

## python3のインストール
pythonとそのライブラリのインストールにはいくつか方法がある。本資料では、Anacondaを利用する方法と、pipのみを利用する方法を紹介する。
### Anacondaを利用する方法
Anacondaはpythonでよく利用するライブラリをまとめてインストールしてくれる。その分容量が大きくなるため、目的に応じて後述するpipを用いた方法と使い分けるのがいいだろう。

はじめに、コンテナを作成する。ターミナルで次のコマンドを実行する。
```shell
$ docker run -it --name anaconda ubuntu:18.04
```
Anacondaは[anaconda.com](https://www.anaconda.com/products/distribution)でインストーラを公開している。`wget`コマンドを用いて、ダウンロードする。`wget`は指定したURLのファイルをカレントディレクトリ上にダウンロードするコマンドである。
```shell
$ apt-get update
$ apt-get install wget
$ wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh   # リンク先の Anaconda3-2019.10-Linux-x86_64.sh をダウンロード
$ bash Anaconda3-2019.10-Linux-x86_64.sh   # インストーラを実行
```
Anacondaのインストールが完了したが、PATHを通していないため、このままでは実行できない。ubuntuでPATHを通すにはrootディレクトリ上の`.profile`ファイルに設定を追記する必要がある。
```shell
$ apt-get install vim
$ vim ~/.profile
```
vimで`.profile`を開いたら、ファイルの末尾に`PATH="$PATH:/opt/mono/3.10/bin"`を追記する。次に、以下のコマンドを実行して`.profile`への変更を反映する。
```shell
$ source ~/.profile   # .profileへの変更を反映する
```
PATHを通したため、anacondaでインストールしたpythonが実行できるようになる。次のコマンドを実行すると、python3の対話モードが起動する。
```shell
$ python3
```
対話モードを抜けるには、`exit()`と入力すれば良い。
### pipを利用する方法
pipはPython Package Index(PyPI)上に公開されているPythonパッケージをインストールするシステムである。PyPIには誰でも自由にパッケージの公開ができるため、Anacondaに比べて利用できるパッケージが非常に多い。

はじめに、コンテナを作成する。ターミナルで次のコマンドを実行する。
```shell
$ docker run -it --name pipython ubuntu:18.04
```
python3,pipはどちらも`apt-get`コマンドでインストールできる。
```shell
$ apt-get update
$ apt-get install python3 python3-pip
```
`apt-get`はインストールしたいパッケージを並べて書くことで、まとめてインストールすることもできる。

次のコマンドを実行すると、python3の対話モードが起動する。
```shell
$ python3
```
対話モードを抜けるには、`exit()`と入力すれば良い。

また、pipを用いたパッケージのインストールはシェル上で行う。例えば、numpyをインストールする場合、次のコマンドを実行する。
```shell
$ pip install numpy
```

## pythonイメージを利用した環境構築