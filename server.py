import socket
import json
import math

def floor(x):
    # floor(double x): 10 進数 x を最も近い整数に切り捨て、その結果を整数で返す。
    return math.floor(x)

def nroot(n, x):
    # nroot(int n, int x): 方程式 rn = x における、r の値を計算する。
    return x ** (1 / n)

def reverse(s):
    # reverse(string s): 文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返す。
    return s[::-1]

def validAnagram(str1, str2):
    # validAnagram(string str1, string str2): 2 つの文字列を入力として受け取り，2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返す。
    return sorted(str1) == sorted(str2)

def sort(strArr):
    # sort(string[] strArr): 文字列の配列を入力として受け取り、その配列をソートして、ソート後の文字列の配列を返す。
    return sorted(strArr)

functions = {
    "floor": floor,
    "nroot": nroot,
    "reverse": reverse,
    "validAnagram": validAnagram,
    "sort": sort
}

def handle_request(data):
    request = json.loads(data) # 引数dataをjsonに変換する
    func = functions.get(request['method']) # クライアントが送るrequestから、methodを抜き出す

    # param_typesの型検証
    param_types = request.get('param_types', [])  # クライアントが送るrequestから、param_typesを抜き出す
    if not validate_params(request['params'], param_types):
        return json.dumps({"error": "Parameter type mismatch", "id": request['id']})

    result = func(*request['params']) # クライアントが送るrequestから、paramsを抜き出す
    return json.dumps({"result": result, "result_type": str(type(result).__name__), "id": request['id']})  # json形式に変更して返す。

def validate_params(params, param_types):
    # string型とint型のみ判定する
    for param, expected_type in zip(params, param_types): # zipにして各々チェック
        if expected_type == "string" and not isinstance(param, str):
            return False
        elif expected_type == "integer" and not isinstance(param, int):
            return False
    return True

def server():
    # 通常のTCPでの処理
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 12345))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                response = handle_request(data.decode())
                conn.sendall(response.encode())


if __name__ == '__main__':
    server()
