# AIdist
### ～Distinguish between AI-generated images and photographs～

![IMAGE ALT TEXT HERE](https://user-images.githubusercontent.com/106128166/197309294-6b473a1f-deec-4a2a-9bbf-8a513652fd9d.png)


## 製品概要
### 背景(製品開発のきっかけ、課題等）
![image](https://user-images.githubusercontent.com/106128166/197311484-07f9cbfd-e465-4469-98d7-85377f4f7445.png)

近年の急速なAI技術の発展のなかでも、画像処理に関する発展はもっとも目覚ましい。特に直近ではフリーワードを入力すればAIが自動で画像を生成してくれる「Stable Diffusion」などはSNSを中心に盛り上がりを見せている。このような技術は人々の生活に彩りを与えている一方で、9月下旬に起こった静岡県の水害に関するツイートが物議を醸したことに代表されるように、AIによって生成されたフェイク画像をあたかも現実に起こったものとして拡散されている事例が散見される。AIが生成する精密な画像は人がさらっと見ただけでは、フェイク画像か否かを判別するのは難しい。

### 製品説明（具体的な製品の説明）・解決できること
<br>本アプリケーションによって、ユーザが簡単にフェイク画像か否かを判定することができ、世の中にあふれる情報を正確にキャッチアップできるようになるだろう。

「AIdist ~Distinguish between AI-generated images and photographs~」は、人の顔画像がフェイク画像である可能性をパーセンテージで示し、具体的にどの部分が怪しいのかを明示するアプリケーションである。
### 想定ユーザ
- 世界中の、情報の信憑性に不安を抱いている人

### 特長
#### 1. 特長1
- ユーザが入力した画像をフェイク画像である可能性を５秒で出力
#### 2. 特長2
- AIがフェイク画像と判断した根拠を提示

## 本アプリの使用方法

※ 現在は人の顔画像のみの入力を前提としたシステム

1.カレントディレクトリをB_2215にし、flask runを実行
http://127.0.0.1:5000に接続

2.「その画像を診断してみよう!」をクリック
![image](https://user-images.githubusercontent.com/106128166/197315700-3f2cb0dc-af20-4e37-804a-a6dbfc721de2.png)



3.左下の「Upload」をクリック、診断したい画像を選択
診断したい範囲を選択し、「OK!」、「CHECK!」を順に押すとAI診断中画面に推移する。
![image](https://user-images.githubusercontent.com/106128166/197314868-c7a7506e-2663-4dc4-91bb-a2132926a758.png)
![image](https://user-images.githubusercontent.com/106128166/197314991-e9bb0220-485b-4eb1-900d-204ea697e147.png)
<img width="1400" alt="スクリーンショット 2022-10-22 11 25 44（2）" src="https://user-images.githubusercontent.com/106128166/197315096-c952eac2-69f9-4a25-8826-fd9b4f420abc.png">

4.診断結果が表示される
フェイクの可能性を上部に、アップロードした画像を左に、AIの判断基準を右に示す
![image](https://user-images.githubusercontent.com/106128166/197315621-bd5ae74e-dcc7-4b67-b6cb-0964b5981ba7.png)


### 注力したこと（こだわり等）・ハッカソンで開発した独自機能・技術
- 独自のデータセットを用いて、独自のAIモデルを構築した。
- ユーザエクスペリエンスを想定したユーザインターフェースの開発


## 開発技術
#### 活用した技術・独自技術・API・データ・フレームワーク・ライブラリ・モジュール
- AIモデルについて
    - 用いたデータセット・・・Large-scale CelebFaces Attributes (CelebA) Datasetランダム抽出した4,000枚の本物画像と「Stable Diffusion」で生成した3,370枚のフェイク画像
    - 用いたモデル・・・CNNを用いた独自モデル

- アプリケーションについて
    - フロントエンド
        - Python, JavaScript, Bootstrap

    - バックエンド
        - Python, Flask, Pytorch, OpenCv

    - インフラ
        - Docker



## 今後の展望
- 現在は顔の画像のみへの対応なので、他のカテゴリへの対応
- 構築を行った独自AIモデルの精度向上
- 本アプリケーションはPCでの利用のみを想定しているため、他のデバイスでの対応


© 2022 from [Tsukuba University](https://www.tsukuba.ac.jp/), presented by てすとべんきょうず