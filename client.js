const net = require('net'); // モジュールのインポート
const client = new net.Socket(); // クライアントソケットの作成
const request = JSON.stringify({ // JSON形式でリクエストを準備, param_types?
    method: "reverse",
    params: ["hello"],
    param_types: ["string"],
    id: 1
});

client.connect(12345, 'localhost', () => { // ポート番号、ホスト名（or IPアドレス）、接続成功時のコールバック関数（＊今回はなし）
    console.log('Connected to server');
    client.write(request); // netモジュールでは、writeでTCPソケット経由でのサーバーへのデータ送信となる
});

// サーバーからデータを受信したら
client.on('data', (data) => {
    console.log('Received from server:', data.toString()); // 文字列に変えてから表示
    client.destroy();
});

// ソケットが閉じたら、コンソールログで知らせる
client.on('close', () => {
    console.log('Connection closed');
});
