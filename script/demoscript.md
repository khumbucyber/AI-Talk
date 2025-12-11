# AIトーク会 デモ手順書

## 📋 事前準備チェックリスト

- [ ] Google Colabにアクセスできる
- [ ] OpenAI APIキーを用意（環境変数 or 直接入力）
- [ ] インターネット接続が安定している
- [ ] 発表用のスクリーンに画面共有できる

---

## 🎯 デモ1: LLM APIはステートレス（名前を覚えない）

### 目的
「LLMは毎回記憶喪失」であることを実際に見せる

### セル1: ライブラリのインストール

```python
# 必要なライブラリをインストール
!pip install openai langchain langchain-openai langchain-chroma chromadb -q
print("✅ インストール完了")
```

### セル2: APIキーの設定

```python
import os
from google.colab import userdata

# Colabのシークレットから取得する場合
os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY')

# または直接入力（発表時は事前に設定しておく）
# os.environ["OPENAI_API_KEY"] = "sk-xxxxx"

print("✅ APIキー設定完了")
```

### セル3: OpenAI クライアントの準備

```python
from openai import OpenAI
client = OpenAI()
print("✅ OpenAI クライアント準備完了")
```

### セル4: 【デモ本番】1回目のリクエスト - 名前を伝える

```python
# ========================================
# 🎤 説明ポイント:
# 「まず、私の名前を伝えて覚えてもらいます」
# ========================================

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "私の名前は良（りょう）です。覚えておいてください。"}
    ]
)

print("📤 送信: 私の名前は良です。覚えておいてください。")
print("=" * 50)
print("📥 応答:")
print(response.choices[0].message.content)
```

**💬 発表時の説明:**
> 「はい、AIが『覚えました』と言いましたね。では次に、新しいリクエストで名前を聞いてみます」

### セル5: 【デモ本番】2回目のリクエスト - 名前を聞く（別リクエスト）

```python
# ========================================
# 🎤 説明ポイント:
# 「これは"別のリクエスト"です。さっきの会話履歴は渡していません」
# ========================================

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "私の名前を教えてください。"}
    ]
)

print("📤 送信: 私の名前を教えてください。")
print("=" * 50)
print("📥 応答:")
print(response.choices[0].message.content)
```

**💬 発表時の説明:**
> 「見てください。『覚えました』と言っていたのに、名前がわからないと言っています。
> これがステートレスということです。APIは前のリクエストのことを何も覚えていません。」

### セル6: 【補足デモ】履歴を渡すと覚えているように見える

```python
# ========================================
# 🎤 説明ポイント:
# 「では、アプリが裏でやっていることを再現します。
#   過去の会話履歴を"一緒に渡す"とどうなるか見てみましょう」
# ========================================

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "私の名前は良（りょう）です。覚えておいてください。"},
        {"role": "assistant", "content": "良さんですね！覚えました。"},
        {"role": "user", "content": "私の名前を教えてください。"}  # ← 新しい質問
    ]
)

print("📤 送信: 過去の会話履歴 + 新しい質問")
print("=" * 50)
print("📥 応答:")
print(response.choices[0].message.content)
```

**💬 発表時の説明:**
> 「今度は名前を答えられました！
> これは学習したわけではなく、過去の会話を"入力に含めた"から答えられただけです。
> ChatGPTなどのアプリは、裏側でこれを自動的にやっています。」

---

## 🎯 デモ2: LangChainで外部メモリ検索（RAG）

### 目的
「必要な情報だけを検索して渡す」仕組みを見せる

### セル7: LangChain の準備

```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

print("✅ LangChain 準備完了")
```

### セル8: 【デモ本番】外部メモリ（過去の情報）を作成

```python
# ========================================
# 🎤 説明ポイント:
# 「これはアプリが保存している"外部メモリ"のイメージです。
#   過去の会話から抽出した情報が保存されています」
# ========================================

# 過去のメモ（外部メモリ）
memory_texts = [
    "ユーザーはJavaとSpring Bootでバックエンド開発をしている",
    "最近はマイクロサービスアーキテクチャに関心がある",
    "DockerとWSL2の環境で開発している",
    "Kafkaを使ったイベント駆動設計を勉強中",
    "フロントエンドはReactとTypeScriptを使用"
]

# ベクトルDBに保存（Embedding化）
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = Chroma.from_texts(memory_texts, embeddings)

print("📝 外部メモリに保存された情報:")
print("=" * 50)
for i, text in enumerate(memory_texts, 1):
    print(f"  {i}. {text}")
```

**💬 発表時の説明:**
> 「5つの情報が外部メモリに保存されています。
> でも毎回これを全部LLMに渡すのは効率が悪いですよね。
> トークン数も増えるし、関係ない情報はノイズになります。」

### セル9: 【デモ本番】質問に関連する情報だけを検索

```python
# ========================================
# 🎤 説明ポイント:
# 「今の質問に"意味的に近い"情報だけを検索します」
# ========================================

query = "Dockerの開発環境を最適化したい"

# 関連する情報を検索（上位2件）
results = db.similarity_search(query, k=2)

print(f"🔍 質問: {query}")
print("=" * 50)
print("📋 検索結果（関連度が高い情報）:")
for i, doc in enumerate(results, 1):
    print(f"  {i}. {doc.page_content}")
```

**💬 発表時の説明:**
> 「5つの情報のうち、Dockerに関連する情報だけが検索されました。
> これがベクトル検索、RAGの基本的な仕組みです。」

### セル10: 【デモ本番】別の質問で試す

```python
# 別の質問で試す
query2 = "フロントエンドの技術スタックについて教えて"

results2 = db.similarity_search(query2, k=2)

print(f"🔍 質問: {query2}")
print("=" * 50)
print("📋 検索結果（関連度が高い情報）:")
for i, doc in enumerate(results2, 1):
    print(f"  {i}. {doc.page_content}")
```

**💬 発表時の説明:**
> 「質問を変えると、検索される情報も変わります。
> これにより、LLMには"今の質問に必要な情報だけ"を渡せるんです。」

### セル11: 【まとめデモ】検索結果を使ってLLMに質問

```python
# ========================================
# 🎤 説明ポイント:
# 「検索した情報をLLMに渡して、回答を生成させます」
# ========================================

query = "Dockerの開発環境を最適化したい"
results = db.similarity_search(query, k=2)

# 検索結果をコンテキストとしてまとめる
context = "\n".join([doc.page_content for doc in results])

# LLMに質問（検索結果を含めて）
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"以下はユーザーに関する情報です:\n{context}"},
        {"role": "user", "content": query}
    ]
)

print(f"🔍 質問: {query}")
print("=" * 50)
print(f"📋 LLMに渡したコンテキスト:\n{context}")
print("=" * 50)
print("📥 LLMの応答:")
print(response.choices[0].message.content)
```

**💬 発表時の説明:**
> 「このように、外部メモリから必要な情報を検索して、
> それをLLMに渡すことで、パーソナライズされた回答が得られます。
> これがChatGPTのメモリ機能やCopilotの仕組みの基本です。」

---

## 🎤 発表時のまとめコメント（読み上げ用）

> 今日のデモで見ていただいたように、
>
> 1. **LLM APIはステートレス**です。毎回「初対面」として処理されます。
>
> 2. **覚えているように見える**のは、アプリが裏で会話履歴を渡しているからです。
>
> 3. **効率よく情報を渡す**ために、LangChainのようなフレームワークで
>    「必要な情報だけ検索して渡す」仕組みが使われています。
>
> AIを「学習させる」のではなく、「どうコンテキストを渡すか」が重要だということが、
> このデモでイメージできたのではないでしょうか。

---

## ⚠️ トラブルシューティング

| 問題 | 対処法 |
|------|--------|
| APIキーエラー | `os.environ["OPENAI_API_KEY"]` を再設定 |
| Rate limit | 数秒待ってから再実行 |
| Chromaエラー | `!pip install chromadb -q` を再実行 |
| Import エラー | セル1のインストールを再実行 |

---

## 📁 Colabノートブック構成（推奨）

```
セル1:  インストール
セル2:  APIキー設定
セル3:  クライアント準備
─────────────────────
セル4:  デモ1-1 名前を伝える     ← デモ開始
セル5:  デモ1-2 名前を聞く
セル6:  デモ1-3 履歴を渡す
─────────────────────
セル7:  LangChain準備
セル8:  デモ2-1 外部メモリ作成   ← デモ2開始
セル9:  デモ2-2 検索（Docker）
セル10: デモ2-3 検索（フロント）
セル11: デモ2-4 LLMに質問
```

**💡 Tips:** セル1〜3とセル7は発表前に実行しておくとスムーズです
