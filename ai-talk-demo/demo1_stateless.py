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
            {"role": "user", "content": "さきほど覚えて頂いた者ですが、私の名前を言えますよね？"}
        ]
    )
    
    print("📤 送信: さきほど覚えて頂いた者ですが、私の名前を言えますよね？")
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