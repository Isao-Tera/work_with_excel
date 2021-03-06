# Lambda Layers
## Why do we need to use layers?
Lambdaはserverlessサービスだが、実際にはAWS Linux2上で動作する。
Pythonの関数をLambdaで実行したい場合、Pythonや基本モジュールはインストール済み。
しかし、外部ライブラリ（Numpy, Pandas）はインストールされていないので、Lambda実行前にインストールする必要がある。
Lambda関数ごとに外部ライブラリをインストールのはめんどくさい！！
→　Layersという機能 [公式ドキュメント](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/configuration-layers.html)
　　別々のLambda関数で__共通のライブラリを使用__できる！

## How to make Layers
- Overview
    Lambdaが動作する同じ環境（AWS Linux2）に利用するPython Librariesをインストール、ライブラリをzip化、zip fileをLayersにアップロード
1. Provision Lmazon Linux2
    - enough t2.micro
    - VPC is default
    - strage is no change
    - security group is createing new, SSH / TCP protocal / port No. 22 
2. EC2のキーペアを Windows Subsystem for Linux2に送付
    \\wsl$でUbuntuにアクセス -> windowsからWSLにpemファイルをコピー
    WSL ターミナルウィンドウで、Windows から WSL に .pem ファイル (インスタンスの起動時に指定したキーペアの場合) をコピーする場合
    * cp /mnt/<Windows drive letter>/path/my-key-pair.pem ~/WSL-path/my-key-pair.pem

3. WSLを使用してEC2 Linuxインスタンスに接続
    ssh -i /path/my-key-pair.pem ec2-user@public-ipv4-address
    ssh -i lambda-layer.pem ec2-user@54.157.141.132

    下記エラーが発生した場合、chmod 600 path/file.pem
    権限を与える、変更するにはchmodコマンドを使う
    600はrw-------(所有者のみ読み書き可能)
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    Permissions 0644 for './layers/lambda-layer.pem' are too open.
    It is required that your private key files are NOT accessible by others.
    This private key will be ignored.
    Load key "./layers/lambda-layer.pem": bad permissions
    ec2-user@54.157.141.132: Permission denied (publickey,gssapi-keyex,gssapi-with-mic).

4. EC2にpython3.8をインストール [Qiita参考](https://qiita.com/hiren/items/17984191da2ab8955174)
    * sudo amazon-linux-extras install -y python3.8
    
5. pyenvを作成する
    * sudo yum install gcc gcc-c++ make git openssl-devel bzip2-devel zlib-devel readline-devel sqlite-devel
    * git clone https://github.com/yyuu/pyenv.git ~/.pyenv
    * echo 'export PYENV_ROOT="${HOME}/.pyenv"' >> ~/.bashrc
    * echo 'if [ -d "${PYENV_ROOT}" ]; then' >> ~/.bashrc
    * echo 'export PATH=${PYENV_ROOT}/bin:$PATH' >> ~/.bashrc
    * echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    * echo 'fi' >> ~/.bashrc
    * source ~/.bashrc
    * pyenv install --list|grep 3.8
    * pyenv install 3.8.5
    * pyenv global 3.8.5
    * python --version
    * pip --version

6. pandasをインストール　[Qiita参考](https://qiita.com/thimi0412/items/4c725ec2b26aef59e5bd)
    * pip install -t ./path pandas

7. pandasライブラリがあるdirectoryをzipfile化
    * zip pandas.zip ./layer-lambda

8. EC2からファイルをダウンロード
    ※　EC2との接続をオフにする
    scpというコマンドを使うことで、サーバー上のファイルをダウンロードしたり、自分のPCからサーバーへアップロードできる
    ファイルをダウンロードする
    * scp -i ~/my.pem ec2-user@xxx.xxx.xxx.xxx:/home/ec2-user/sample.log ./
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^ 　　　^^
                                          サーバー上のファイルパス      ダウンロード先
    * scp -i lambda-layer.pem ec2-user@54.157.141.132:/home/ec2-user/pandas.zip ./
9. zipファイルをS3に置いて、LambdaでLayerを作成する
10. Lambda関数でLayerを設定する

#　サックと外部ライブラリを使いたい！！
    [先人の作ってくれたLayerを使う](https://github.com/keithrozario/Klayers)
    [↑の説明](https://qiita.com/polarbear08/items/202752d5ffcb65595bd9)
