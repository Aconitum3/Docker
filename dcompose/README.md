# Docker Compose

この章では、Docker Composeを用いてコンテナの作成・起動を効率的に行う方法を学ぶ。

## Docker Composeとは
Docker Composeは、複数のコンテナを用いるプロジェクトの構築・実行の手順を自動化するツールである。それらの構成は、`docker-compose.yml`ファイルで定義する。`.yml`はYAMLファイルの拡張子である。YAML(YAML Ain't a Markup Language)ファイルは、設定ファイルの作成などによく使われる。

複数のコンテナを用いるアプリケーションでは、コンテナ間で通信が行われる。Docker Composeは、プロジェクト単位で内部ネットワークを用意し、それらを`docker-compose.yml`に定義する。これらの有用性を示すために、次節ではDocker Composeを用いないコンテナ間通信を実装する。次に、同じ実装を`docker-compose.yml`で定義する。複数コンテナの利用に興味がなければ、読み飛ばして構わないが、`docker-compose.yml`の記法には目を通しておくと良い。

複数のコンテナを用いない場合でも、Docker Composeは非常に便利である。`docker-compose.yml`には、プロジェクトの構成を定義できる。ここで、プロジェクトの構成とは、ポートの割り当て、ボリュームのマウントなどである。次の例を考える。
あるイメージを他人に配布したい。我々は、イメージの配布に加えて、時には非常に長い`docker run`も伝える必要がある。Docker Composeを用いる場合、`Dockerfile`と`docker-compose.yml`を配布し、いくつかの簡潔な`docker-compose`コマンドを伝えるだけで良いのだ。こちらの方が容量も小さくて済む。これといって理由がなければ、`Dockerfile`と`docker-compose.yml`を配布する方が良いだろう。

## コンテナ間通信
Web開発プロジェクトを例に挙げる。Web開発では、Web3層構造という技術がしばしば使われる。Web3層構造では、文字通り、WebアプリケーションをWebサーバー・Appサーバー・DBサーバーの3層の構造で編成する。

![dcompose_1](img/web3architecture.jpg)
出典: [softbank.jp "Web3層アーキテクチャってなに？Alibaba Cloud, AWS, Azure, Google Cloud のWeb3層アーキテクチャを比べてみました"](https://www.softbank.jp/biz/blog/cloud-technology/articles/202206/web-3-tier-architecture/)

上図のように、各層が相互に通信を行っている。この仕組みを実装してみる。本節では、WebサーバーにNiginx、AppサーバーにPythonのGunicorn、DBサーバーにMySQLを使う。しかし、この仕組みはやや難解である。そのため、はじめに基礎編として、DBサーバーとAppサーバーのみを用いたコンテナ通信を実装する。その後に、応用編としてWeb3層構造を実装する。応用編は読み飛ばしても構わない。

### 基礎編　PythonコンテナとMySQLコンテナの通信
はじめにMySQLコンテナを起動する。Docker HubにMySQLのイメージがあるため、それをそのまま使用する。ターミナルで次のコマンドを実行する。
```bash
$ docker pull mysql
$ docker run --name web_db -e MYSQL_ROOT_PASSWORD=my-password -d mysql
```
`-e`オプションは、環境変数を設定するオプションである。`MYSQL_ROOT_PASSWORD`はMySQLのrootアカウントのパスワードであり、コンテナ起動の際に必ず設定する必要がある。

bashに入る。
```bash
$ docker exec -it web_db bash
```
続けて、bashで次のコマンドを実行し、mysqlカーネルを起動する。
```bash
$ mysql --user=root --password=my-password
```
データベースを作成し、テーブルを作成する。mysqlカーネルで次のコマンドを実行する。
```SQL
mysql> CREATE DATABASE db;
mysql> USE db;
mysql> CREATE TABLE students (name VARCHAR(255), age INT);
```
データベース`db`に、テーブル`students`を作成した。ここにいくつかのデータを追加する。
```SQL
mysql> INSERT INTO students (name, age) VALUES ("Taro", 16), ("Hanako", 17), ("Pochi", 3);
mysql> SELECT * FROM students;
```
```SQL
+--------+------+
| name   | age  |
+--------+------+
| Taro   |   16 |
| Hanako |   17 |
| Pochi  |    3 |
+--------+------+
3 rows in set (0.00 sec)
```
データを追加できたため、mysqlとbashから抜ける。コンテナは起動したままにしておく。
```bash
mysql> exit
$ exit
```
MySQLコンテナと通信するためには、ipアドレスを取得する必要がある。コンテナのipアドレスは`docker network`で確認できる。
```bash
$ docker network ls
> NETWORK ID     NAME      DRIVER    SCOPE
  **********     bridge    bridge    local
  **********     host      host      local
  **********     none      null      local

$ docker network inspect bridge
> 
[
    {
        "Name": "bridge",
        "Id": "******",
        "Created": "******",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "******",
                    "Gateway": "******"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "******": {
                "Name": "web_app",
                "EndpointID": "******",
                "MacAddress": "******",
                "IPv4Address": "******",
                "IPv6Address": ""
            },
            "******": {
                "Name": "web_db",
                "EndpointID": "******",
                "MacAddress": "******",
                "IPv4Address": "******",  <-- web_dbのipアドレス
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]
```
`docker network ls`はDockerのネットワーク一覧を表示するコマンドである。`bridge`,`none`,`host`はデフォルトで作成されるネットワークであり、MySQLコンテナは、`bridge`ネットワークに属する。

`docker network inspect ***`は`***`ネットワークの詳細を表示するコマンドである。この詳細から、MySQLコンテナのipアドレスが取得できる。

次に、Pythonコンテナを起動する。ターミナルで次のコマンドを実行する。
```bash
$ docker pull python:3.7
$ docker run -it --name web_app -d python
```
bashに入り、必要なライブラリをインストールする。
```bash
$ docker exec -it web_app bash
```
```bash
$ pip install mysqlclient
$ python3
```
`mysqlclient`はpythonからMySQLにアクセスするためのライブラリである。

ここからは、先ほど取得したMySQLコンテナのipアドレスから、MySQLコンテナのデータベースにPythonコンテナから接続する。pythonカーネルで次を実行する。
```python
import MySQLdb
db_settings = {"host": "******",          # MySQLコンテナのipアドレス
               "user": "root",            # rootユーザー
               "passwd": "my-password",   # MYSQL_ROOT_PASSWORD
               "db": "db",                # データベースの名前
               "charset": "utf8mb4"       # 文字コード
              }
db_conn = MySQLdb.connect(**db_settings)  # データベースに接続
cursor = db_conn.cursor()                 # カーソルを取得
query = "SELECT * FROM students"
cursor.execute(query)                     # クエリを実行
ret = cursor.fetchall()                   # 結果を取得
ret
```
```python
(('Taro', 16), ('Hanako', 17), ('Pochi', 3))
```
以上のように、Pythonコンテナから、MySQLコンテナのデータベースのデータを取得することができた。

### 基礎編　docker-compose.ymlによる実装
本節では、前節の実装を`docker-compose.yml`で定義する。まず、MySQLコンテナを定義しながら、`docker-compose.yml`の基本的な記法を学ぶ。

前節で作成したコンテナは削除しておく。
```bash
$ docker stop web_db
$ docker rm web_db
$ docker stop web_app
$ docker rm web_app
```

MySQLコンテナは次のように定義する。

```yml
# docker-compose.yml

version: "2"
services:
  web_db:
      image: mysql
      environment:
        - MYSQL_ROOT_PASSWORD=my-password
```
`version`は`docker-compose`のバージョンを指定する。最新版は`"3"`だが、本資料では、`"2"`を使う。

プロジェクトで稼働するコンテナを`services`以降で定義する。ここでは、`web_db`という名前のコンテナを定義している。

`image`は`web_db`の元となるイメージを指定する。

`environment`は`web_db`における環境変数を指定する。

試しに、この[`docker-compose.yml`](basic1/docker-compose.yml)からMySQLコンテナを起動してみる。カレントディレクトリに`docker-compose.yml`が存在する状態で、ターミナルで次のコマンドを実行する。
```bash
$ docker-compose up -d
```
`docker-compose up`は、コンテナを作成して起動するコマンドである。`-d`オプションをつけると、バックグランドで起動する。既にコンテナが作成済みの場合、`docker-compose start`が使える。また、コンテナの停止は`docker-compose stop`を使う。コンテナを停止して、さらに削除する場合、`docker-compose down`を使う。

また、`docker-compose`コマンドで起動した任意のコンテナで、コマンドを実行するために、`docker-compose exec`が用意されている。例えば、`web_db`でbashに入るには、次のコマンドを実行する。

```bash
$ docker-compose exec web_db bash
```

Pythonコンテナもプロジェクトに追加したいため、一度コンテナを削除する。
```bash
$ docker-compose down
```
次に、`docker-compose.yml`にPythonコンテナを定義する。はじめに、Dockerfileから作成する。
```Dockerfile
FROM python:3.7
RUN pip install mysqlclient
COPY app.py ./
```

`app.py`には、MySQLコンテナのデータベースからデータを取得するプログラムを記述する。

```python
# app.py

import MySQLdb
db_settings = {"host": "web_db", "user": "root", "passwd": "my-password", "db": "db", "charset": "utf8mb4"}
db_conn = MySQLdb.connect(**db_settings) 
cursor = db_conn.cursor()
query = "SELECT * FROM students"
cursor.execute(query)
ret = cursor.fetchall()
print(ret)
```
`host`には、ipアドレスではなく、MySQLコンテナのサービス名（コンテナ名）を指定すれば良い。

`docker-compose.yml`は次のようになる。

```yml
# docker-compose.yml

version: "2"
services:
  web_db:
      image: mysql
      environment:
        - MYSQL_ROOT_PASSWORD=my-password
  web_app:
      build:
        context: .
        dockerfile: Dockerfile
      tty: true
      depends_on:
        web_db:
          condition: service_started 
```
`build`はDockerfileからコンテナを作成する際に指定する。`context`にDockerfileが存在するディレクトリを指定し、`dockerfile`にDockerfileのファイル名を指定する。

`tty: true`は`docker run`における`-it`オプションと同じである。

`depends_on`では、他サービスとの依存関係を指定する。ここでは、`web_db`との依存関係として、`condition: service_started`を指定した。`service_started`を`condition`で指定すると、依存先のサービスが起動した後に、起動するようになる。つまり、`web_app`は`web_db`が起動するまで、起動しない。

最後に、`web_db`に少し変更を加える。データベース・テーブルを作成し、データを追加する操作をスクリプトファイルにまとめたい。`init.sh`として次のファイルを作成する。
```sh
# init.sh

COMMAND='
CREATE DATABASE db;
USE db;
CREATE TABLE students (name VARCHAR(255), age INT);
INSERT students (name, age) VALUES ("Taro", 16), ("Hanako", 17), ("Pochi", 3);'

mysql --user=root --password=my-password --execute="$COMMAND"
```
MySQLイメージは、`/docker-entrypoint-initdb.d/`というディレクトリに、スクリプトファイルを置くと、コンテナ起動時に自動的に実行される。以上を踏まえた上で、次のようなDockerfileを作成する。
```Dockerfile
FROM mysql:latest
COPY init.sh /docker-entrypoint-initdb.d/
```
ディレクトリ構成は、次のようにする。
```
project/
　├ web_db/
　│ 　├ Dockerfile
　│ 　└ init.sh
　├ web_app/
　│ 　├ Dockerfile
　│ 　└ app.py
　└ docker-compose.yml
```
`docker-compose.yml`は、次のように修正する。
```yml
# docker-compose.yml

version: "2"
services:
  web_db:
      build:
        context: web_db
        dockerfile: Dockerfile
      environment:
        - MYSQL_ROOT_PASSWORD=my-password
  web_app:
      build:
        context: web_app
        dockerfile: Dockerfile
      tty: true
      depends_on:
        web_db:
          condition: service_started 
```
projectディレクトリ下が[このように](basic2)なっていれば良い。

プロジェクトを起動してみる。カレントディレクトリがprojectディレクトリの状態で、次のコマンドを実行する。
```bash
$ docker-compose up -d
$ docker-compose exec web_app python3 app.py
> (('Taro', 16), ('Hanako', 17), ('Pochi', 3))
```
上手くいかない場合、イメージのキャッシュが残っているかもしれない。`docker-compose build`でイメージを再生成できる。
```bash
$ docker-compose build
```

### 応用編　Web3層構造の実装
はじめに、前節で作成したAppサーバー(Pythonコンテナ)にいくつか要素を追加する。まず、`app.py`として次のファイルを作成する。
```python
# app.py

from flask import Flask
import MySQLdb

app = Flask(__name__)    # アプリケーションのインスタンスを作成

@app.route('/')          # rootページを定義
def root():

    db_settings = {"host": "web_db", "user": "root", "passwd": "my-password", "db": "db", "charset": "utf8mb4"}
    db_conn = MySQLdb.connect(**db_settings) 
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM students")
    ret = cursor.fetchall()
    db_conn.close()

    body = "<table><tr><th>name</th><th>age</th></tr>{}</table>".format(
        "".join([
            "<tr><td>{}</td><td>{}</td>".format(name, age)
            for name, age
            in ret
        ])
        )
    page = "<html><head><title>Students</title></head><body>{body}</body><html>"

    return page.format(body=body)
```
`app.py`では、HTTPリクエストがあるとデータベースに接続し、それをテーブルにしたHTMLを返す。

Dockerfileを次のように修正する。
```Dockerfile
# Dockerfile

FROM python:3.7
RUN pip install mysqlclient flask gunicorn
COPY app.py ./
CMD gunicorn app:app --bind 0.0.0.0:80
```
`gunicorn`はDjangoやFlaskなどのWebアプリケーションを動かすHTTPサーバーである。Djangoなどのフレームワークには、サーバーを起動するコマンドがあるが、`gunicorn`のサーバーはそれらのサーバーに比べ速く、安定して動作する。`gunicorn hello:app`は、`hello.py`の`app`というアプリケーションを起動する。また、`--bind`オプションをつけると、ネットワークとポートを指定できる。Dockerのコンテナは`0.0.0.0`でないと、外部からコンテナにアクセスできないのであった。よって、`gunicorn app:app --bind 0.0.0.0:80`は`app.py`の`app`アプリケーションを`0.0.0.0:80`で起動するコマンドである。

次に、Nginxコンテナを作成する。Docker Hubにnginxのイメージが公開されているため、それを元にDockerfileを作成する。Nginxでは、接続先のWebサーバーを指定するとき、それを`default.conf`に記述する。ここでは、詳しい説明は省略するが、次のような`default.conf`を作成する。
```conf
# default.conf

server {
    listen       80;
    server_name  localhost;

    location / {
        proxy_pass http://web_app;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```
`location`の`proxy_pass`に、`http://web_app`を指定する。

Dockerfileは次のようになる。
```Dockerfile
# Dockerfile

FROM nginx:latest
COPY default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

現在のディレクトリ構成は次のようになっている。
```
project/
　├ web_db/
　│ 　├ Dockerfile
　│ 　└ init.sh
　├ web_app/
　│ 　├ Dockerfile
　│ 　└ app.py
　├ web_web/
　│ 　├ Dockerfile
　│ 　└ default.conf
　└ docker-compose.yml
```

最後に、`docker-compose.yml`を修正する。次のように`web_web`を追加する。
```yml
# docker-compose.yml

version: "2"
services:
  web_db:
      build:
        context: web_db
        dockerfile: Dockerfile
      environment:
        - MYSQL_ROOT_PASSWORD=my-password
  web_app:
      build:
        context: web_app
        dockerfile: Dockerfile
      tty: true
      depends_on:
        web_db:
          condition: service_started
  web_web:
      build:
        context: web_web
        dockerfile: Dockerfile
      ports:
       - "80:80"
      depends_on:
        web_app:
          condition: service_started
```
`ports`では、ホストのポートとコンテナのポートをマッピングする。`"8888:6666"`なら、コンテナの`6666`番ポートをホストの`8888`番ポートにマッピングする。

`depends_on`では、`web_app`が起動した後に、`web_web`が起動するようにする。`web_web`が`web_app`を参照するからだ。

projectディレクトリ下が[このように](advanced)なっていれば良い。

プロジェクトを起動してみる。カレントディレクトリがprojectディレクトリの状態で、次のコマンドを実行する。
```bash
$ docker-compose up
```
`localhost:80`にアクセスすると、学生のデータが確認できる。

## Jupyter Lab環境をdocker-composeで作成する
前節では、Web3層構造を例に`docker-compose.yml`の基本的な記法を学んだ。本節では、前章で作成したJupyter Lab環境の[Dockerfile](../dfile/jupyter/Dockerfile)を使って、`docker-compose`で環境を構築する。

次のような、`docker-compose.yml`を作成する。
```yml
# docker-compose.yml

version: "2"
services:
  jupyter:
    build:
     context: .
     dockerfile: Dockerfile
    volumes:
      - ./mountpoint:/home
    ports:
      - "8888:8888"
```
`volumes`では、ホストのディレクトリを、コンテナのディレクトリにマウントしている。ここでは、ホストのカレントディレクトリ内のmountpointディレクトリをコンテナのhomeディレクトリにマウントしている。mountpointディレクトリが存在しない場合、`docker-compose up`を実行した時に自動で作成される。現在のディレクトリ構成は[このように](jupyter)なっている。
```
jupyter/
　├ Dockerfile
　├ docker-compose.yml
　├ requirements.txt
　└ mountpoint/
```
Jupyter Labを起動してみる。ターミナルで次のコマンドを実行する。
```bash
$ docker-compose up
```
ログで出力されるURLにアクセスするとJupyter Labに接続できる。また、コンテナの停止には`Ctrl+C`を入力する方法もある。
