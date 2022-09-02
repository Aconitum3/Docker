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
* `apt-get moo`

    Supter Cow Powersを持った牛が現れる。

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
次に、Linuxで広く利用されるテキストエディタのvimをインストールし、テキストファイルを編集してみる。

```shell
$ apt-get update   # インストール可能なパッケージの一覧を更新
$ apt-get install vim   # vimをインストール

$ cd mydir
$ touch test.txt   # カレントディレクトリにtest.txtという名前のファイルを作成
$ vim test.txt   # vimでtest.txtファイルを開く
```
`apt-get`で、vimをインストールし、`touch`で作成したtest.txtファイルを`vim`コマンドで開いている。ここでは、vimの簡単な操作方法のみを説明する。vimには4つモードがあり、これらのモードを切り替えながら編集を行う。vim起動直後はnormalモードで`i`キーを押すとinsertモードに切り替わる。insertモードでは主に文字の入力などを行う。insertモードからnormalモードにはエスケープキーで切り替える。nomralモードの状態で`ZZ`を入力すると、保存して終了ができる。試しにtest.txtに好きな文字列を入力し、保存してみると良い。

`cat`で書き込んだ内容を確認してみる。
```shell
$ cat test.txt   # test.txtファイルの中身を確認
> I like SUSHI.   # 書き込んだ内容が出力される
```

Ctrl+P, Ctrl+Qでシェルから抜けることができる。この操作をdetachという。シェルから抜けた状態で次のコマンドを実行する。
```shell
$ docker ps
> CONTAINER ID   IMAGE          COMMAND   CREATED       STATUS         PORTS     NAMES
  ************   ubuntu:18.04   "bash"    *******       Up ***                   *****
```
`docker ps`で、起動中のコンテナを確認することができる。NAMESはコンテナ名で、`docker run`でコンテナ名を指定しない場合、ランダムに決まる。再度、シェルに入るには次のコマンドを実行する。
```shell
$ docker attach {-- CONTAINER ID or NAMES --}
```
`{}`はコンテナIDかコンテナ名のどちらかを入力する。例えば、コンテナ名が`my_con`ならば、`docker attach my_con`とすれば良い。

シェルに入った状態で、次のコマンドを実行する。
```shell
$ exit
```
`exit`はbashを終了するコマンドである。このコンテナは、bashが終了すると停止する。`docker ps`で確認してみる。
```shell
$ docker ps
> CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
起動しているコンテナは1つもない。再度コンテナを起動するには、次のコマンドを実行する。
```shell
docker start {-- CONTAINER ID or NAMES --}
```
作成したコンテナを削除してみる。コンテナのシェルに入っているなら`exit`で抜けた後に、次のコマンドを実行する。
```shell
$ docker ps -a
> CONTAINER ID   IMAGE           COMMAND   CREATED   STATUS        PORTS     NAMES
  ************   ubuntu:18.04    "bash"    *******   Exited ***              *****

$ docker rm {-- CONTAINER ID or NAMES --}
$ docker ps -a
> CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
`docker ps -a`は起動していないコンテナも含めて全てのコンテナの状態を表示するコマンドである。`docker rm`は指定したコンテナを削除するコマンドである。

最後に、いくつかのオプションを加えて、同じイメージからコンテナを作成する。次のコマンドを実行する。
```shell
$ docker run -it -d --name test ubuntu:18.04
$ docker ps
> CONTAINER ID   IMAGE          COMMAND   CREATED         STATUS         PORTS     NAMES
  ************   ubuntu:18.04   "bash"    *******         Up ***                   test
```
`-d`と`--name test`について説明する。`-d`はコンテナをdetachedモードで起動するオプションである。デフォルトのforegroundモードと異なり、detachedモードで起動したコンテナは、起動時にシェルに入ることがなく、バックグラウンドで動作する。`--name`はコンテナ名を指定するオプションである。上の例ではコンテナ名を`test`にした。`-it`については後で説明するが、このオプションを付けないとコンテナが起動直後に停止する。