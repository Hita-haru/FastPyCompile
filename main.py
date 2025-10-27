from google import genai
import json
import os
import subprocess

client = genai.Client()

def main():
    print("AI Pythonコンパイラ")
    path = input("コンパイルしたいPythonファイルのパスを入力 >>>")
    print (f"Pythonファイル: {path}のコンパイルを開始します....")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    responce = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents="あなたは優秀かつ経験豊富なプログラマーです。以下のPythonのプログラムをC++に変換し、Json形式で\"code\"キーに変換後のコードを入力してください。C++をコンパイルする環境はLinuxのClang++、C++17でコンパイルします。もし変換できない部分があった場合、一部であれば\"note\"キーにその部分の説明を入れて、主要部分に変換できないところがあった場合は\"ERROR_1\"と出力し、入力されたコードがPythonのコードでない場合は\"ERROR_2\"と出力してください。以下が変換したいPythonのコードです。\n```python\n" + code + "\n```",
        config={
            "response_mime_type": "application/json"
        }
    )
    response_text = responce.text

    if response_text == "ERROR_1":
        print("コードの変換に失敗しました。\n予想される問題: >主要部分が変換できない<\n強制終了します....")
        exit()
    elif response_text == "ERROR_2":
        print("コードの変換に失敗しました。\n予想される問題: >入力されたコードがPythonのコードではない<\n強制終了します....")
        exit()
    else:
        print("コードの変換に成功しました。コンパイルを開始します。")

    response_json = json.loads(response_text)
    note = response_json.get("note", "")
    print(f"変換できなかった部分があります。以下の説明を参照してください。\n{note}")
    converted_code = response_json["code"]
    with open("source.cpp", "w", encoding="utf-8") as f:
        f.write(converted_code)
    
    print("C++コードをsource.cppに保存しました。コンパイルを実行します。")
    
    source_file = "source.cpp"

    if input("exeファイルで出力しますか？(Y/n) >>>") .lower() == 'y':
        output_file = "out.exe"
    else:
        output_file = "out.out"


    compile_command = [
        'clang++',
        source_file,
        '-o',
        output_file,
        '-Wall',  # 警告をすべて表示するオプション
        '-std=c++17' # 使用するC++の規格を指定
    ]
    try:
        subprocess.run(compile_command, check=True)
        print(f"コンパイルが成功しました。出力ファイル: {output_file}")
    except subprocess.CalledProcessError as e:
        print("コンパイル中にエラーが発生しました。")
        print(e)
    print("処理が完了しました。")

if __name__ == "__main__":
    main()