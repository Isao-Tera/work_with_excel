# How to Use AWS Lambda 

# Lambda Functions

# Lambda Layers
## Why do we need to use layers?
Lambdaはserverlessサービスだが、実際にはAWS Linux2上で動作する。
Pythonの関数をLambdaで実行したい場合、Pythonや基本モジュールはインストール済み。
しかし、外部ライブラリ（Numpy, Pandas）はインストールされていないので、Lambda実行前にインストールする必要がある。
Lambda関数ごとに外部ライブラリをインストールのはめんどくさい！！
→　Layersという機能 [公式ドキュメント](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/configuration-layers.html)
　　別々のLambda関数で__共通のライブラリを使用__できる！

## How to use Layers
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
    ssh -i /path/my-key-pair.pem my-instance-user-name@my-instance-public-dns-name


#
#