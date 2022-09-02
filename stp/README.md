# Dockerのインストールと基本操作

この章では、はじめにDockerのインストールを行う。次にUbuntuのコンテナを用いて基本的なLinuxコマンドと、Dockerコマンドをいくつか学ぶ。

## Dockerのインストール

[Docker公式サイト](https://www.docker.com/)からDocker Desktopをインストールする。インストールの手順について説明することはしないが、必要に応じて以下の記事を参考にすると良い。
* [WindowsにDocker Desktopをインストール](https://docs.docker.jp/desktop/windows/install.html#windows-docker-desktop)
* [MacにDocker Desktopをインストール](https://docs.docker.jp/desktop/mac/install.html)

また、以降でDockerを動かすときは、Docker Desktopの起動を前提とする。Docker Desktopが起動していない状態で、Dockerコマンドを実行した場合、
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
```

のようなエラーメッセージが表示される。

## 各種用語

次節で出てくる専門的な用語をまとめておく。必要に応じて参照すると良い。

### カーネル
カーネルは、OSの基本機能の役割を担う。CPUやメモリなどのハードウェアリソースとソフトウェアの連携を管理する。
### Linuxディストリビューション
Linuxとは、狭義的にはLinuxカーネルのことを指す。Linuxカーネルとその他のソフトウェアをパッケージ化したものをLinuxディストリビューションという。Linuxディストリビューションにもいくつか種類があるが、本資料では主にUbuntuを用いる。
### シェル
ユーザーからの命令をLinuxカーネルに伝えるプログラムをシェルという。Linuxのデフォルトのシェルはbashである。
### イメージ
コンテナを作成する際に、そのベースとなるものをイメージという。1つのイメージから複数のコンテナを作成することも可能である。また、イメージは[Docker Hub](https://hub.docker.com/)からダウンロードすることができる。Docker Hubでは、個人や企業、団体が作成したイメージが公開されている。
### apt-getコマンド
apt-getコマンドは、Linuxでソフトウェアの導入や管理、削除に用いられるパッケージ管理システムの一つである。よく使うapt-getコマンドをいくつか紹介する。

* `apt-get update`

    インストール可能なパッケージの一覧を更新する。実際のパッケージのインストール、アップグレードなどは行われない。
* `apt-get upgrade`

    パッケージの一覧をもとに、インストール済みのパッケージを更新する。パッケージの一覧が古いままだと意味がないため、`apt-get update`と合わせて使う。
* `apt-get install ****`

    パッケージの一覧をもとに、パッケージ「 **** 」をインストールする。

## Dockerの基本操作

ここでは、Linuxディストリビューションの1つであるUbuntuのイメージを用いてDockerの基本操作を学ぶ。ターミナルで、次のコマンドを実行する。
```shell
$ docker pull ubuntu:18.04
```
`docker pull`はDocker Hubから、イメージをダウンロードするコマンドである。ここでは、ubuntu 18.04のイメージを取得している。このイメージをベースにコンテナを作成する。
```shell
$ docker run -it ubuntu:18.04
```
`root@******:/# `のように表示されれば、作成したコンテナのシェルに接続できている。ここからは、このシェルに入った状態で、Linuxコマンドをいくつか実行してみる。
```shell
$ ls   # カレントディレクトリ上のファイルを一覧表示する
> bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var

$ cd home   # カレントディレクトリをhomeに変更
$ ls
> 

$ mkdir mydir   # カレントディレクトリにmydirという名前のディレクトリを作成
$ ls
> mydir
```
`ls`でカレントディレクトリ上のファイル名を確認後、`cd`でカレントディレクトリをhomeに変更し、homeディレクトリ上に`mkdir`でmydirディレクトリを作成した。
次に、Linuxで広く利用されるテキストエディタVimをインストールし、テキストファイルを編集してみる。

```shell
$ apt-get update
$ apt-get install vim
```