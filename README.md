# Docker演習

## 本資料について
本資料では、Dockerの概要を理解し、Dockerを用いて目的に応じた仮想環境を自由に作ることができるようになることを目指す。

## 目次

### [Dockerとは](wid/README.md)

 * 仮想化とは
 * ハイパーバイザーとコンテナ
    * なぜWindowsでLinux系コンテナが動作するのか
 * Dockerの何が良いのか

### [Dockerのインストールと基本操作](stp/README.md)

 * Dockerのインストール
 * 各種用語
 * Dockerの基本操作

 ### [Python3環境の構築](python/README.md)

 * python3のインストール
    * Anacondaを利用する方法
    * pipを利用する方法
 * pythonイメージを利用した環境構築
    * オプション -it について
 * Jupyter Lab環境の構築

 ### [イメージの配布](distimg/README.md)

 * コンテナからイメージを作成する
 * イメージの配布

 ### [Dockerfile](dfile/README.md)

 * Dockerfileとは
 * python3環境(Anaconda)をDockerfileで作成する
 * Jupyter Lab環境をDockerfileで作成する
    * Jupyter Labのtokenを再確認する方法

### [Docker Compose](dcompose/README.md)

 * Docker Composeとは
 * コンテナ間通信
    * 基礎編　PythonコンテナとMySQLコンテナの通信
    * 基礎編　docker-compose.ymlによる実装
    * 応用編　Web3層構造の実装
 * Jupyter Lab環境をdocker-composeで作成する