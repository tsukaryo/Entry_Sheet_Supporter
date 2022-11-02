# DockerTemplate

Docker+Djangoのテンプレートです。**作業が終わったらこのファイル（README.md）を削除してください。**

## プロジェクトの始め方

1. [このページ](https://github.com/SIX1-REPO/DockerTemplate)の**Use this Template** を選択
    
    ![https://user-images.githubusercontent.com/48053582/170398125-cbe922fb-a242-4ed4-b49e-4608484ed7e2.png](https://user-images.githubusercontent.com/48053582/170398125-cbe922fb-a242-4ed4-b49e-4608484ed7e2.png)
    
2. プロジェクト名を入力し，**Create repostory from template**を選択
    
    ![https://user-images.githubusercontent.com/48053582/170401566-63317f33-2898-48b4-a818-655d69ee44f1.png](https://user-images.githubusercontent.com/48053582/170401566-63317f33-2898-48b4-a818-655d69ee44f1.png)
    
3. `git clone`でローカルに落とす
4. クローンしたディレクトリで`python initialize.py init`を実行してSECRET KEYの初期化
5. *作業開始！*

## アプリの起動

### ローカル

- Dockerを立ち上げる。
    
    ```
    docker-compose build
    docker-compose up -d
    ```
    
- [http://localhost:8000/](http://localhost:8000/) にアクセスして確認。

### Heroku（Heroku CLIを使う場合）

- まずHerokuにログインする。
    
    ```
    heroku login
    ```
    
- 次にappを作成して、リモートを追加する。
    
    ```
    heroku create <app名>
    heroku git:remote -a <app名>
    ```
    
- 環境変数を設定する。
    
    ```
    python initialize.py heroku
    ```
    
- Herokuのgitにpushする。
    
    ```
    git push heroku <ブランチ名>
    ```
    
    - `git status`で現在のブランチを確認できる。

- ページが立ち上がっているか確認。
    
    ```
    heroku open
    ```
    

## 補足

### migrateについて

- ローカルのDockerで作業を行う際は、必要に応じてmigrateを行う必要がある。
- Herokuに新しいリリースを作成したときには、自動でmigrateされるようになっている。

### runtime.txtに関して

- 現在サポートされているランタイムを指定する必要がある。
- [https://devcenter.heroku.com/ja/articles/python-support#supported-runtimes](https://devcenter.heroku.com/ja/articles/python-support#supported-runtimes)

### コンテナを起動中にパッケージをインストールする

- `-user`オプションを付けて`pip install`を実行することで、Dockerを起動している状態でもライブラリをインストールすることができる。
    
    ```
    docker-compose run app pip install -r requirements.txt --user
    ```
    
- 内部的には、PYTHONUSERBASEという環境変数を使い、パッケージのインストール先を`/pip-lib`内に指定している。 ( 参考：[https://asukiaaa.blogspot.com/2020/07/docker-python-pip-install-without-rebuilding.html](https://asukiaaa.blogspot.com/2020/07/docker-python-pip-install-without-rebuilding.html) )

### initialize.py

Djangoの秘密鍵に関するプログラムが書かれている。

- `python initialize.py init`で秘密鍵の作成ができる。
- `python initialize.py heroku`でHerokuの環境変数に秘密鍵を設定できる。

以上の操作を行ったら、このファイルは削除しても構わない。

### .gitignore

- 自動生成される不要なファイルは追加したほうがいいです。
- VSCodeなら`.vscode`、PyCharmなら`.idea`など
