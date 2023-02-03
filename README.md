TODO
- [x] Function to validate CPF
- [x] [Validate input data](https://www.youtube.com/watch?v=Y_GQdxRSnIg)
- [x] Perform the sum of received values and check if they are the same as the total coming in the payload
  - I validated taking into account that the value is being sent and this was a requirement at the time of project construction. Particularly, I wouldn't even return an error, I would just add the products at this moment and pass the sum value forward to avoid a bottleneck, as it is a challenge, I just validated it and returned the error.
- [x] Validate the sale date of the products
- [x] [Create a database in sqlite](https://www.youtube.com/watch?v=3h8K29U5_HA)
- [x] Validate product type
- [x] Add cashback for each product
- [x] Calculate cashback
- [ ] Send the calculated cashback to the Mais Todos api
- [ ] Save all requests and responses
- [ ] Automate database creation in sqlite
- [ ] Create unit tests
- [ ] Refactor code

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
