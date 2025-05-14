# Linebot アプリケーション 🤖📰

> *パーソナライズされたニュース配信で、あなたの情報収集をスマートに*

![LINE Bot](https://img.shields.io/badge/LINE-Bot-00c300)
![Python 3.x](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📱 機能一覧

* 🔍 **パーソナライズされたニュース配信** - ユーザーの興味に合わせた情報を厳選
* 📝 **リアルタイム要約** - 長い記事もAIが素早く要約
* ⏰ **定期配信** - 毎朝の情報収集をサポート

---

## 💬 使用方法

### 🔗 LINE Botとの友だち追加

1. QRコードを読み取るか、LINE IDで友だち追加してください
2. 友だち追加後、自動的な初期メッセージが表示されます
3. リッチメニューの「トピック設定」から興味のある分野を選択してください

### 🎮 基本的な操作

#### 🏷️ トピック設定
リッチメニューから「トピック設定」を選択し、興味のあるニュースカテゴリーを選びます。複数選択可能です。

#### 📋 ニュース要約の取得
1. LINE Botにキーワードや話題を送信すると、関連するニュースを自動的に検索し要約を返信します
2. 返信される要約には、タイトル・要約・URL・発信元・発信日時が含まれます

#### 📬 購読設定
以下のコマンドをメッセージとして送信することで、定期配信の設定を変更できます：
- `subscribe` - 定期配信を開始
- `unsubscribe` - 定期配信を停止
- `status` - 現在の購読状態を確認

### ⏱️ 定期配信

購読設定をONにしている場合、毎朝9時に設定したトピックに基づいた最新ニュースの要約が自動的に配信されます。

---

## 🛠️ 技術スタック

| カテゴリ | 技術 |
|---------|------|
| バックエンド | Python 3.x, FastAPI |
| データベース | PostgreSQL, SQLAlchemy |
| メッセージング | LINE Bot SDK |
| AI & 自然言語処理 | Google Generative AI |
| スケジューリング | APScheduler |

詳細は `requirements.web.txt` をご参照ください。

---

## 🚀 セットアップ

### 📋 前提条件

- Python 3.xがインストールされていること
- PostgreSQLデータベースへのアクセス
- LINE Developersアカウントと設定済みのMessaging APIチャネル
- Google AI Studioのアクセスキー

### 📥 インストール

1. リポジトリをクローン
   ```bash
   git clone https://github.com/yourusername/Linebot.git
   cd Linebot
   ```

2. 依存パッケージのインストール
   ```bash
   pip install -r requirements.web.txt
   ```

### ⚙️ 環境設定

1. `.env`ファイルを作成し、以下の環境変数を設定
   ```
   # データベース設定
   DATABASE_URL=postgresql://username:password@localhost:5432/linebot_db
   
   # LINE Messaging API設定
   LINE_CHANNEL_SECRET=your_channel_secret
   LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
   
   # Google AI API設定
   GOOGLE_API_KEY=your_google_api_key
   
   # アプリケーション設定
   APP_ENV=development  # development または production
   LOG_LEVEL=INFO
   ```

2. データベースのマイグレーション
   ```bash
   alembic upgrade head
   ```

### 🐳 Dockerでの実行

1. Dockerコンテナのビルドと起動
   ```bash
   docker-compose up -d
   ```

2. ログの確認
   ```bash
   docker-compose logs -f app
   ```

3. コンテナの停止
   ```bash
   docker-compose down
   ```

### 💻 ローカル環境での実行

1. アプリケーションの起動
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. スケジューラーの個別起動（オプション）
   ```bash
   python -m app.scheduler
   ```

### 🔌 Webhook URL設定

LINE Developersコンソールで以下のWebhook URLを設定してください：
- 本番環境: `https://yourdomain.com/webhook/line`
- 開発環境: ngrokなどを使用して `http://localhost:8000/webhook/line` を公開

### 🚢 デプロイ

本番環境へのデプロイ方法には以下のオプションがあります：

1. Herokuへのデプロイ
   ```bash
   heroku create
   git push heroku main
   ```

2. AWS ECSを使用したデプロイ
   - `deploy/ecs`ディレクトリ内のCloudFormationテンプレートを使用

---

## 📜 ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。

---

## 👨‍💻 コントリビューション

プロジェクトへの貢献は大歓迎です！バグ報告や機能提案は[Issue](https://github.com/yourusername/Linebot/issues)から、コード貢献は[Pull Request](https://github.com/yourusername/Linebot/pulls)からお願いします。

---

## 📞 お問い合わせ

質問や提案がある場合は、[example@email.com](mailto:example@email.com)までご連絡ください。