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

#### コード例

```python
# Tavily Search
from tavily import AsyncTavilyClient
client = AsyncTavilyClient(api_key=TAVILY_API_KEY)
results = await client.search(query=text)

# Gemini 要約
from google import genai
client = genai.Client(api_key=GEMINI_API_KEY)
resp = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt,
)
