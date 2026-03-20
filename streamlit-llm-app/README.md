# streamlit-llm-app

## 事前準備

1. GitHub で `streamlit-llm-app` という名前のリポジトリを作成する
2. リポジトリ作成時に `.gitignore` は `Python` を選ぶ
3. 作成したリポジトリを PC にクローンする
4. クローンしたフォルダを VS Code で開く
5. 仮想環境を作成して有効化する
6. `pip install -r requirements.txt` を実行する
7. `.env.example` を参考に `.env` ファイルを作り、`OPENAI_API_KEY` を設定する

## ローカル実行

```bash
streamlit run app.py
```

## デプロイ時の注意

- Streamlit Community Cloud では Python 3.11 を選ぶ
- `OPENAI_API_KEY` は GitHub に上げず、Secrets に設定する

## 提出物

- `app.py`
- `requirements.txt`
