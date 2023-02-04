TODO
- [x] Function to validate CPF
- [x] [Validate input data](https://www.youtube.com/watch?v=Y_GQdxRSnIg)
  - In this video I got the idea of how to validate data in a separate file and that was very similar to Django's serializer
- [x] Perform the sum of received values and check if they are the same as the total coming in the payload
  - I validated taking into account that the value is being sent and this was a requirement at the time of project construction. Particularly, I wouldn't even return an error, I would just add the products at this moment and pass the sum value forward to avoid a bottleneck, as it is a challenge, I just validated it and returned the error.
- [x] Validate the sale date of the products
- [x] [Create a database in sqlite](https://www.youtube.com/watch?v=3h8K29U5_HA)
  - Here I took advantage of the simplicity of how he made the initial insertions, so as not to worry about creating methods to put data in the database
  - PS: Just before the challenge I was studying GraphQL with this video lol, that's why I took this reference
- [x] Validate product type
- [x] Add cashback for each product
- [x] Calculate cashback
- [x] Send the calculated cashback to the Mais Todos API
- [x] Save all requests and responses
- [ ] Refactor code
- [ ] Automate database creation in sqlite
- [ ] Create unit tests

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
