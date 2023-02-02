TODO
- [x] Function to validate CPF
- [ ] [Validate input data](https://www.youtube.com/watch?v=Y_GQdxRSnIg)

##### Run httpie in terminal, for test

```bash
echo '{"sold_at":"2026-01-02 00:00:00","customer":{"document":"68175541016","name":"JOSE DA SILVA"},"total":"100.00","products":[{"type":"A","value":"10.00","qty":1},{"type":"B","value":"10.00","qty":9}]}' | http :5000/api/cashback

HTTP/1.1 200 OK
Connection: close
Content-Length: 17
Content-Type: application/json
Date: Thu, 02 Feb 2023 19:55:17 GMT
Server: Werkzeug/2.2.2 Python/3.10.8

{
    "message": "ok"
}

```