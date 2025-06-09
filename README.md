# けんサ君 – Tavily × Gemini で実現する AI 検索 & 要約 LINE Bot

LINE 上で自然言語検索と要約をシームレスに提供する Bot アプリ **「けんサ君」** を開発しました。  
本リポジトリには、設計からデプロイまでの一連のプロセスをまとめています。

> **モバイル推奨**  
> PC クライアントではリッチメニューが一部制限されます。スマートフォンでのご利用をおすすめします。

<p align="center">
  <img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3856953/9b460491-5142-4c7f-97cf-686aa6f3f156.png" alt="QR – add friend" width="240"/>
</p>

---

## 目次

1. [アプリ概要](#アプリ概要)  
2. [使用技術](#使用技術)  
   - [外部 API](#外部-api)  
   - [機密情報の管理](#機密情報の管理)  
   - [CI/CD](#cicd)  
3. [アーキテクチャ](#アーキテクチャ)  
4. [主要機能](#主要機能)  
5. [今後の展望](#今後の展望)  
6. [参考文献](#参考文献)

---

## アプリ概要

けんサ君は **LINE** で動く検索 Bot です。  
ユーザーが自然言語で入力したクエリを **Tavily API** で検索し、  
結果を **Gemini** が短く要約して返信します。  
「必要な情報だけを最速で得る」ことを目指し、  
履歴がチャットに残る LINE ならではの利便性も確保しました。

---

## 使用技術

| 区分 | 技術 |
| --- | --- |
| フレームワーク | FastAPI |
| フロントエンド | HTML / Tailwind CSS / JavaScript (リッチメニュー) |
| 言語 | Python |
| 外部 API | LINE Messaging API / Tavily Search API / Gemini API |
| データベース | PostgreSQL |
| スケジューラ | APScheduler |
| コンテナ | Docker / Docker Compose |
| インフラ | AWS (EC2, ACM, ELB, EIC, IAM, Secrets Manager) |
| CI/CD | GitHub Actions (OIDC で IAM ロール切替) |

### 外部 API

| API | 用途 | 公式ドキュメント |
| --- | --- | --- |
| Messaging API | LINE Bot とのメッセージ送受信 | <https://developers.line.biz/ja/docs/messaging-api/overview/> |
| Tavily API | 高速・高精度な Web 検索 | <https://docs.tavily.com/documentation/api-reference/introductio> |
| Gemini API | 生成 AI による要約 | <https://ai.google.dev/gemini-api/docs?hl=ja> |

### 2.2． 機密情報の管理方法 ###
機密情報（APIキーやデータベースのユーザ、またAWSの認証情報など）はGithub SecretとAWS Secret Managerで管理しており、コンテナ内には機密情報が保存されないような構成となっています。docker-compose時にDBコンテナのみ.envファイルを参照しますが、CI/CD時に動的に作成/削除を行う設定になっているため、EC2インスタンス内には残らない仕組みになっています。

### 2.3．CI/CD ##
リポジトリへのプッシュをトリガーに自動でデプロイを行う CI/CD パイプラインを構築しています。GitHub Actions のワークフローでは、OIDC（OpenID Connect）を使って GitHub から発行される一時的なトークンを AWS IAM ロールの引き受けに利用し、長期的なアクセスキーをリポジトリに置くことなく安全に認証を行います。認証後は AWS CLI を介して EC2 インスタンスに対してデプロイ用のコマンドを実行し、コードのフェッチ、コンテナの再ビルド、環境変数ファイルの動的生成と削除までを一連のスクリプトで自動化します。これにより、EC2インスタンスへの不要なポート開放や鍵の管理をなくし、最小権限の IAM ポリシーでセキュアかつ高速なデプロイを実現しています。


## 3. アーキテクチャ
構築したアプリケーションの大まかなアーキテクチャが以下になります。（※ユーザが利用した場合のフローのみを落とし込んでいるためCI/CDは省略しています）

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3856953/55155996-badc-4d0f-bb9d-55c35d9bf17a.png)

MessagingAPIで登録可能なWebhookエンドポイントは **https://** のみなので、独自ドメインを取得しAWS Certificate Managerで証明書を発行しELBに関連付けることで、Meesaging API-ELB間はHTTPS通信が行われるようにしました。デプロイ時にはできる限り無料枠内に抑えるために必要最小限の構成となっています。

また、今回は単一のインスタンスに3つのDockerコンテナを立ち上げていますが、ポートを公開しているのはWebhookのエンドポイントのみであり、スケジューラは外向きの通信のみ許可、DBはDocker仮想ブリッジ内でのみの通信を許可しています。そのため、EC2のインバウンドは送信元がELBとメンテナンス用のSSH接続を行うEC2 Connect Instance Endpointのみを許可しています。そのため、EC2インスタンスと外部との通信を最小限に抑える構成になっています。


## 4．アプリ機能
### 基本機能
- **検索機能**
ユーザが入力した情報を基にTavilyがWEB検索し、最もスコアの高い（関連度が高いと思われる）記事が3つFlexMessage形式で返答されます。入力時は自然言語での入力が可能であり、よりチャットに近い形式での検索も実現できます。また，「詳細を見る」をクリックすると元URLのページに遷移することができ、より詳細な情報を確認できます。

    ![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3856953/51722b19-62e6-4829-ab52-aeb4ce1bf34c.png)

### リッチメニュー
- **言語選択**
検索機能の使用時に出力される際の言語を切り替えることができるようになります。言語切り替えの対象言語は日本語、英語、フランス語、ドイツ語、スペイン語、韓国語、中国語、ロシア語の8種類に対応しています。そのため、その言語の学習をしたいときなどに言語選択を行うと検索しながら言語を学習することもできるようになります。
 
    ![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3856953/a7da161b-0498-40e5-a13a-44d5966e667a.png)
    　
- **定期通知**
毎朝8:00に、ユーザーが登録した Web ページを自動で巡回し、前回チェック時点から更新があった場合はその差分を LINE メッセージでお知らせします。たとえば、推しのアーティストのライブ情報サイトやブログの更新、公式ニュースリリースのチェックなどに活用できます。

    ![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3856953/6f14b06d-0d23-40d2-989b-1a6a2e5ab86f.png)
　
- **モード選択**
検索機能の利用時におけるモードを切り替えることが可能になります。モードは「一般（デフォルト）」と「ニュース」の二つがあります。「一般（デフォルト）」では、最適化したWEB検索を提供しますが、「ニュース」ではニュースに特化した検索を行い、最新のニュースを幅広く提供することが可能になります。通勤時や通学時に友人などにLINEで連絡した後に、ふとニュースを検索しチャット上に残しておくことができるようになります。
