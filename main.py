from google import genai
import json
import os
import subprocess
import shlex
import sys

client = genai.Client()

def main():
    print("AI Pythonコンパイラ")
    path = input("コンパイルしたいPythonファイルのパスを入力 >>>")
    print (f"Pythonファイル: {path}のコンパイルを開始します....")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    if input("exeファイルで出力しますか？(Y/n) >>>") .lower() == 'y':
        output_file = "out.exe"
    else:
        output_file = "out.out"

    prompt = f"""あなたは優秀かつ経験豊富なプログラマーです。以下のPythonのプログラムをC++に変換してください。
C++をコンパイルする環境はLinuxのClang++、C++17です。
変換後のC++コードは`source.cpp`というファイル名で保存されます。
コンパイル後の出力ファイル名は`{output_file}`にしてください。

レスポンスはJson形式で、以下のキーを含めてください:
- `code`: 変換後のC++コード
- `command`: `source.cpp`をコンパイルして`{output_file}`を生成するためのClang++コマンドライン文字列

もし変換できない部分があった場合、一部であれば`note`キーにその部分の日本語の説明を入れてください。
主要部分に変換できないところがあった場合はERROR_1とだけ出力してください。
入力されたコードがPythonのコードでない場合はERROR_2とだけ出力してください。

以下が変換したいPythonのコードです。
```python
{code}
```"""

    if (sys.argv[0] == "-p"):
        model1 = "gemini-2.5-pro"
        print("\"-p\"オプションによりGemini 2.5 PROが選択されました")
    else:
        model1 = "gemini-2.5-flash"
    responce = client.models.generate_content(
        model = model1,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )
    try:
        response_text = responce.text
        if response_text == "ERROR_1":
            print("コードの変換に失敗しました。\n予想される問題: >主要部分が変換できない<\n強制終了します....")
            exit()
        elif response_text == "ERROR_2":
            print("コードの変換に失敗しました。\n予想される問題: >入力されたコードがPythonのコードではない<\n強制終了します....")
            exit()

        
        # APIからの応答がJSONかどうかを確認
        try:
            response_data = json.loads(response_text)
            if isinstance(response_data, dict):
                print("コードの変換に成功しました。コンパイルを開始します。")
                note = response_data.get("note", "")
                if note:
                    print(f"変換できなかった部分があります。以下の説明を参照してください。\n{note}")
                if "code" not in response_data or "command" not in response_data:
                    print("エラー: 変換されたコードまたはコンパイルコマンドが見つかりません。")
                    exit()
                converted_code = response_data["code"]
                compile_command_str = response_data["command"]
            else:
                print("エラー: APIからの応答が正しい形式ではありません。")
                exit()
        except json.JSONDecodeError:
            print("エラー: APIからの応答をJSONとして解析できませんでした。")
            print(f"受信した応答: {response_text}")
            exit()
    except json.JSONDecodeError:
        print("JSONのパースに失敗しました。APIからの応答が正しいJSON形式ではありません。")
        exit()
    with open("source.cpp", "w", encoding="utf-8") as f:
        f.write(converted_code)
    
    print("C++コードをsource.cppに保存しました。コンパイルを実行します。")
    
    compile_command = shlex.split(compile_command_str)

    try:
        subprocess.run(compile_command, check=True)
        print(f"コンパイルが成功しました。出力ファイル: {output_file}")
    except subprocess.CalledProcessError as e:
        print("コンパイル中にエラーが発生しました。")
        print(e)
    print("処理が完了しました。")

if __name__ == "__main__":
    main()
