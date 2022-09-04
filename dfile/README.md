# Dockerfile

この章では、Dockerfileの概念を学び、Jupyter Lab環境をDockerfileから作成する。

## Dockerfileとは

Dockerでは、Dockerfileから命令を読み込み、イメージを作成することができる。Dockerfileは拡張子のないテキストファイルであり、イメージを作成するために実行するコマンドを全て含んでいる。いわば、イメージの設計図のようなものである。

ごく簡潔なDockerfileの例を見てみる。

```Dockerfile
FROM busybox:latest
CMD echo "hello world"
```
`FROM`では、作成するイメージのベースとなるイメージ（ベースイメージ）を指定する。ここでは、busybox:latestのイメージを指定した。`CMD`では、Dockerfileから作成したイメージから、コンテナを起動する際に実行するコマンドを指定する。`CMD`はDockerfileで一度だけ指定でき、複数の`CMD`があると最も後ろの`CMD`のみが実行され、その他は無視される。また、`CMD`で指定したコマンドがRoot Processとなる。ここでは、`echo "hello world"`を実行する。`echo`は引数として与えた文字列や変数を出力するコマンドである。つまり、このコンテナは、`hello world`を出力して停止する。

Dockerfileはテキストエディタなどで作成する。`Dockerfile.txt`ではなく、`Dockerfile`のように拡張子はつけない。

このDockerfileから、イメージを作成してみる。カレントディレクトリにDockerfileがある状態で、ターミナルで次のコマンドを実行する。
```shell
$ docker build -t hello:latest ./
```
`docker build`はDockerfileからイメージを作成するコマンドである。引数に、Dockerfileを含むディレクトリを指定する。ここでは、カレントディレクトリ上にDockerfileがあるため、カレントディレクトリを表す`./`を引数に指定した。`-t`はイメージの名前をつけるオプションである。ここでは、`hello:latest`とした。

hello:latestからコンテナを作成してみる。ターミナルで次のコマンドを実行する。
```shell
$ docker run --name hello hello:latest
> hello world
```
ここで、helloコンテナのRoot Processが`echo "hello world"`であるため、`-it`をオプションに付けなくて良いことは理解しておきたい。また、`docker ps`を実行してみると、helloコンテナが停止していることが確認できるはずだ。

## Anacondaを利用したpython3環境をDockerfileで作成する
前章では、Anacondaを利用したpython3環境を作成した。ここでは、いくつかの新しいDockerfile記法を学ぶために、この環境をDockerfileで作成してみる。ubuntu:18.04のイメージをベースに以下を実行する必要がある。
 * anaconda.comから、インストーラをダウンロードする。
 * インストーラを実行する。
 * PATHを通す。
 * Root Processをpython3にする。

以上を満たしたDockerfileは次のようになる。

```Dockerfile
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y wget
RUN wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
RUN bash Anaconda3-2019.10-Linux-x86_64.sh -b

ENV PATH $PATH:/root/anaconda3/bin

CMD python3
```
新たに現れた`RUN`と`ENV`について説明する。

`RUN`では、Dockerfileからイメージを作成する際に、実行されるコマンドを指定する。`RUN`は`CMD`と異なり、複数指定できる。このDockerfileには3つの`RUN`がある。それぞれの内容について、順に説明する。

`RUN apt-get update && apt-get install -y wget`では、`apt-get update`をした後に、`apt-get install`で`wget`をインストールしている。`&&`で複数のコマンドをつなぐことで、1つの`RUN`で複数のコマンドを実行できる。特に、`apt-get update`と`apt-get install`は`&&`でつないで実行する必要がある。これは、1つの`RUN`で`apt-get update`だけを実行すると、キャッシュに問題が発生し、その後の`apt-get install`が失敗するためだ。また、`-y`のオプションも重要である。前章で`apt-get install`などを実行した際、`[Y/n]`のような問い合わせがあったのを覚えているだろうか。`-y`はこのような問い合わせがあった場合に、全て`y`と答えるオプションである。問い合わせを含む`apt-get install`で`-y`のオプションをつけなかった場合、Dockerfileからイメージを作成するのに失敗する。

`RUN wget https://...`では、anaconda.comからインストーラを、`wget`コマンドでカレントディレクトリにインストールしている。

`RUN bash Anaconda3-2019.10-Linux-x86_64.sh -b`では、`bash`コマンドで、インストーラを実行している。`-b`は、全ての問い合わせにデフォルトの値を答えるオプションである。

`ENV`は環境変数`<key>`と値`<value>`のセットで、`ENV <key> <value>`のように指定する。`ENV`では、作成するイメージで利用する環境変数を設定できる。環境変数とは、OSが提供するデータ共有機能の一つであり、PATHもこれに該当する。ここでは、`ENV PATH $PATH:/root/anaconda3/bin`とすることで、AnacondaのPATHを通している。

以上で、動作するDockerfileが作成できた。イメージを作成し、コンテナを起動するとpython3のシェルに入ることができる。しかし、このDockerfileにはいくつか課題が残っている。それらの課題を解決することで、効率的なイメージを構築できる。順に説明する。
 * レイヤが多い。

    まずは、レイヤの概念を理解する必要があるだろう。Dockerのイメージはレイヤという層構造からなる。最下層のレイヤは`FROM`で指定されたベースイメージである。`RUN`などの一部の命令が行われるごとに、新たなレイヤが作成され上に蓄積していく。これらの層が少なければ、イメージのサイズは小さくなる。例えば、この章で作成したDockerfileの`RUN`の部分は次のように改善できる。
    ```Dockerfile
    RUN apt-get update && apt-get install -y \
      wget \
      && wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh \
      && bash Anaconda3-2019.10-Linux-x86_64.sh -b
    ```
    改行の際は` \`を加える。話が少しそれるが、`apt-get install`で複数のパッケージをまとめてインストールする場合、パッケージの重複指定を防ぐためにも、以下の例のように改行し、アルファベット順で並べるのが望ましい。
    ```Dockerfile
    RUN apt-get update && apt-get install -y \
      bzr \
      cvs \
      git \
      marcurial \
      subversion
    ```
 * 余計なファイルが残っている。

    実は、`RUN`の部分はさらに改善できる。`apt-get update`はインストール可能なパッケージのリストの一覧を更新するコマンドであった。`apt-get update`を実行すると、`/var/lib/apt/lists/`にリストの一覧がキャッシュされる。また、Anacondaのインストーラも残ったままである。これらを削除することで、イメージのサイズはさらに小さくなる。最終的な`RUN`の部分は次にようになる。
    ```Dockerfile
    RUN apt-get update && apt-get install -y \
      wget \
      && rm -rf /var/lib/apt/list/* \
      && wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh \
      && bash Anaconda3-2019.10-Linux-x86_64.sh -b \
      && rm Anaconda3-2019.10-Linux-x86_64.sh
    ```
    `rm`はファイルやディレクトリを削除するコマンドである。ディレクトリを削除する場合、`-r`をつける。`-r`をつけても削除する際に、問い合わせがあることがある。`-rf`は問い合わせを無視して問答無用で削除するオプションである。重要なファイルを削除してしまうことがあるため、`-rf`を使う際は十分に気をつけてほしい。
 * a
## Jupyter Lab環境をDockerfileで作成する
## Dockerfileからイメージを作成する