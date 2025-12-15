# AIトーク会 デモ手順書（ローカル Python + VSCode）

## 📋 事前準備チェックリスト

- [ ] Python 3.9以上がインストールされている
- [ ] VSCodeがインストールされている
- [ ] OpenAI APIキーを用意
- [ ] 必要なライブラリをインストール済み
- [ ] 発表用のスクリーンに画面共有できる

---

## 🔧 環境セットアップ（発表前に実施）

### 1. 作業フォルダを作成

```bash
mkdir ai-talk-demo
cd ai-talk-demo
```

### 2. 仮想環境を作成（推奨）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. 必要なライブラリをインストール

```bash
pip install openai langchain langchain-openai langchain-chroma chromadb
```

### 4. 環境変数にAPIキーを設定

**方法A: .envファイルを使う（推奨）**

```bash
# .env ファイルを作成
echo OPENAI_API_KEY=sk-xxxxx > .env
```

```bash
# python-dotenv もインストール
pip install python-dotenv
```

**方法B: 直接環境変数を設定**

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-xxxxx"

# Windows (コマンドプロンプト)
set OPENAI_API_KEY=sk-xxxxx

# Mac/Linux
export OPENAI_API_KEY=sk-xxxxx
```

### 5. VSCodeでフォルダを開く

```bash
code .
```

---

## 📁 ファイル構成

以下の2ファイルを作成しておく：

```
ai-talk-demo/
├── .env                  # APIキー（方法Aの場合）
├── demo1_stateless.py    # デモ1: ステートレスの実演
└── demo2_langchain.py    # デモ2: LangChainの実演
```

---

## 🎯 デモ1: LLM APIはステートレス（名前を覚えない）

### ファイル: `demo1_stateless.py`

```python
"""
デモ1: LLM APIはステートレス
- LLMは毎回「記憶喪失」であることを実演

使い方:
    python demo1_stateless.py 1-1    # 名前を伝える
    python demo1_stateless.py 1-2    # 名前を聞く（忘れている）
    python demo1_stateless.py 1-3    # 履歴を渡すと答えられる
    python demo1_stateless.py all    # 全て実行
"""

import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def demo_1_1():
    """1回目: 名前を伝える"""
    print("=" * 60)
    print("【デモ1-1】名前を伝える")
    print("=" * 60)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "私の名前は良（りょう）です。覚えておいてください。"}
        ]
    )
    
    print("📤 送信: 私の名前は良です。覚えておいてください。")
    print("-" * 60)
    print("📥 応答:")
    print(response.choices[0].message.content)
    print()

def demo_1_2():
    """2回目: 名前を聞く（別リクエスト）"""
    print("=" * 60)
    print("【デモ1-2】名前を聞く（別リクエスト = 履歴なし）")
    print("=" * 60)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "私の名前を教えてください。"}
        ]
    )
    
    print("📤 送信: 私の名前を教えてください。")
    print("-" * 60)
    print("📥 応答:")
    print(response.choices[0].message.content)
    print()

def demo_1_3():
    """3回目: 履歴を含めて聞く"""
    print("=" * 60)
    print("【デモ1-3】履歴を含めて聞く（アプリがやっていること）")
    print("=" * 60)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "私の名前は良（りょう）です。覚えておいてください。"},
            {"role": "assistant", "content": "良さんですね！覚えました。"},
            {"role": "user", "content": "私の名前を教えてください。"}
        ]
    )
    
    print("📤 送信: 過去の会話履歴 + 新しい質問")
    print("-" * 60)
    print("📥 応答:")
    print(response.choices[0].message.content)
    print()

def show_help():
    print("""
使い方: python demo1_stateless.py [デモ番号]

デモ番号:
    1-1    名前を伝える（「覚えました」と返る）
    1-2    名前を聞く（忘れている！）
    1-3    履歴を渡すと答えられる
    all    全て順番に実行
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == "1-1":
        demo_1_1()
    elif arg == "1-2":
        demo_1_2()
    elif arg == "1-3":
        demo_1_3()
    elif arg == "all":
        demo_1_1()
        demo_1_2()
        demo_1_3()
    else:
        show_help()
```

### 発表時の操作手順

```bash
# ターミナルで順番に実行
python demo1_stateless.py 1-1    # → 「覚えました」と返る
python demo1_stateless.py 1-2    # → 「わかりません」と返る
python demo1_stateless.py 1-3    # → 名前を答えられる
```

1. **`1-1` を実行** → 「覚えました」と返る
   - 説明：「名前を伝えて、覚えてもらいました」
2. **`1-2` を実行** → 「わかりません」と返る
   - 説明：「別のリクエストなので、完全に忘れています。これがステートレス」
3. **`1-3` を実行** → 名前を答えられる
   - 説明：「履歴を一緒に渡すと答えられる。ChatGPTアプリは裏でこれをやっている」

---

## 🎯 デモ2: LangChainで外部メモリ検索（RAG）

### ファイル: `demo2_langchain.py`

```python
"""
デモ2: LangChainで外部メモリ検索
- 必要な情報だけを検索して渡す仕組みを実演

使い方:
    python demo2_langchain.py 2-1    # 外部メモリを作成
    python demo2_langchain.py 2-2    # Docker関連を検索
    python demo2_langchain.py 2-3    # フロントエンド関連を検索
    python demo2_langchain.py 2-4    # 検索結果でLLMに質問
    python demo2_langchain.py all    # 全て実行
"""

import sys
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
client = OpenAI()

# 過去のメモ（外部メモリ）
MEMORY_TEXTS = [
    "ユーザーはJavaとSpring Bootでバックエンド開発をしている",
    "最近はマイクロサービスアーキテクチャに関心がある",
    "DockerとWSL2の環境で開発している",
    "Kafkaを使ったイベント駆動設計を勉強中",
    "フロントエンドはReactとTypeScriptを使用"
]

def create_db():
    """ベクトルDBを作成"""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma.from_texts(MEMORY_TEXTS, embeddings)

def demo_2_1():
    """外部メモリを作成"""
    print("=" * 60)
    print("【デモ2-1】外部メモリ（過去の情報）を作成")
    print("=" * 60)
    
    print("📝 外部メモリに保存された情報:")
    print("-" * 60)
    for i, text in enumerate(MEMORY_TEXTS, 1):
        print(f"  {i}. {text}")
    print()
    print("✅ ベクトルDBに保存完了")
    print()

def demo_2_2():
    """質問に関連する情報だけを検索"""
    print("=" * 60)
    print("【デモ2-2】質問に関連する情報だけを検索")
    print("=" * 60)
    
    db = create_db()
    query = "Dockerの開発環境を最適化したい"
    results = db.similarity_search(query, k=2)
    
    print(f"🔍 質問: {query}")
    print("-" * 60)
    print("📋 検索結果（関連度が高い情報）:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}")
    print()

def demo_2_3():
    """別の質問で試す"""
    print("=" * 60)
    print("【デモ2-3】別の質問で検索")
    print("=" * 60)
    
    db = create_db()
    query = "フロントエンドの技術スタックについて教えて"
    results = db.similarity_search(query, k=2)
    
    print(f"🔍 質問: {query}")
    print("-" * 60)
    print("📋 検索結果（関連度が高い情報）:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}")
    print()

def demo_2_4():
    """検索結果を使ってLLMに質問"""
    print("=" * 60)
    print("【デモ2-4】検索結果を使ってLLMに質問")
    print("=" * 60)
    
    db = create_db()
    query = "Dockerの開発環境を最適化したい"
    results = db.similarity_search(query, k=2)
    
    context = "\n".join([doc.page_content for doc in results])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"以下はユーザーに関する情報です:\n{context}"},
            {"role": "user", "content": query}
        ]
    )
    
    print(f"🔍 質問: {query}")
    print("-" * 60)
    print(f"📋 LLMに渡したコンテキスト:")
    print(f"  {context}")
    print("-" * 60)
    print("📥 LLMの応答:")
    print(response.choices[0].message.content)
    print()

def show_help():
    print("""
使い方: python demo2_langchain.py [デモ番号]

デモ番号:
    2-1    外部メモリの内容を表示
    2-2    Docker関連の検索
    2-3    フロントエンド関連の検索
    2-4    検索結果をLLMに渡して回答生成
    all    全て順番に実行
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == "2-1":
        demo_2_1()
    elif arg == "2-2":
        demo_2_2()
    elif arg == "2-3":
        demo_2_3()
    elif arg == "2-4":
        demo_2_4()
    elif arg == "all":
        demo_2_1()
        demo_2_2()
        demo_2_3()
        demo_2_4()
    else:
        show_help()
```

### 発表時の操作手順

```bash
# ターミナルで順番に実行
python demo2_langchain.py 2-1    # 外部メモリの内容を表示
python demo2_langchain.py 2-2    # Docker関連が検索される
python demo2_langchain.py 2-3    # フロントエンド関連が検索される
python demo2_langchain.py 2-4    # LLMが回答
```

1. **`2-1` を実行** → 5つの情報が表示される
   - 説明：「これが外部メモリに保存された情報です」
2. **`2-2` を実行** → Docker関連が検索される
   - 説明：「Dockerについて聞くと、関連する情報だけが検索されます」
3. **`2-3` を実行** → フロントエンド関連が検索される
   - 説明：「質問を変えると、検索結果も変わります」
4. **`2-4` を実行** → LLMが回答
   - 説明：「検索した情報をLLMに渡して、パーソナライズされた回答を得ます」

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
| `OPENAI_API_KEY` エラー | `.env` ファイルを確認、または環境変数を再設定 |
| `ModuleNotFoundError` | `pip install` を再実行 |
| Rate limit エラー | 数秒待ってから再実行 |
| Chroma エラー | `pip install chromadb --upgrade` |

---

## 💡 VSCode での実行Tips

### ターミナルで実行（推奨）
```bash
# デモ1
python demo1_stateless.py 1-1
python demo1_stateless.py 1-2
python demo1_stateless.py 1-3

# デモ2
python demo2_langchain.py 2-1
python demo2_langchain.py 2-2
python demo2_langchain.py 2-3
python demo2_langchain.py 2-4
```

### ヘルプを表示
```bash
python demo1_stateless.py
python demo2_langchain.py
```

### 発表時のコツ
- VSCodeのターミナルを大きく表示しておく
- 矢印キー（↑）で前のコマンドを呼び出し、番号だけ変えて実行するとスムーズ

---

## 📁 発表前の最終チェック

```bash
# 仮想環境を有効化
venv\Scripts\activate  # Windows

# デモ1のテスト
python demo1_stateless.py 1-1
python demo1_stateless.py 1-2
python demo1_stateless.py 1-3

# デモ2のテスト
python demo2_langchain.py 2-1
python demo2_langchain.py 2-2
python demo2_langchain.py 2-3
python demo2_langchain.py 2-4
```

問題なく動作すれば準備完了です！🎉
