## Requirements to run the project
- The project was created in a linux environment, POP OS 22.04. The commands follow this system, and may vary if you use another OS
- Python 3.10
- Possibility to run make commands (Makefile)

## Start project
##### Just enter the command below in the terminal
```bash
make install
```
###### The command above: start the container, install the dependencies and generate the populated database

###### [Run project with venv](docs/start_project_venv.md)
## Rotes
PS: To make it easier, I exported the [Postman collection](https://drive.google.com/drive/folders/1UD04eMe_aF2aHHJmRTCFw_3iMzDIypqt?usp=sharing), just use the Flask API
In the login route, I used the ```Basic Auth```, sent in the ```header```. The body is sent empty
```
POST http://localhost:5000/api/login/
```
Header
```json
{
  "Authorization": "Basic bWFpc3RvZG9zOm1haXN0b2Rvcw==",
  "Content-Type": "application/json"
}
```

After login, you will have access to the token and just send it also in the Header in Authorization, but now as Bearer Token
```
POST http://localhost:5000/api/cashback
```
Header
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1haXN0b2RvcyIsImV4cCI6MTY3NTY0NTY4MX0.4a05Kp75AfwgGntyq-iyv-F1rH2TILH18CzygcTV3fM",
  "Content-Type": "application/json"
}
```

Body
```json
{
    "sold_at": "2023-01-02 00:00:00",
    "customer": {
       "document": "68175541016",
       "name": "JOSE DA SILVA"
    },
    "total": "100.00",
    "products": [
       {
          "type": "A",
          "value": "10.00",
          "qty": 1
       },
       {
          "type": "B",
          "value": "10.00",
          "qty": 9
       }
    ]
}
```

As the data sending API was offline at the time of project creation, the response is being defaulted to

```status_code: 400```
```json
{
    "error_message": "Max number of elements reached for this resource!"
}
```

###### All incoming and outgoing data as well as cashback calculations are kept in the database in the LogAPI table. For each request, just check it

## Run all tests on container
```bash
make test
```
###### PS: If the container is not running, run ```make up```

## Project creation logic
#### TODO
- #### Priority
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
  - I thought a lot about removing or obfuscating the CPF within the database, but because it was a challenge I decided to keep it for the evaluation
- [x] Refactor code
- [x] [Login](https://medium.com/@hedgarbezerra35/api-rest-com-flask-autenticacao-25d99b8679b6)
  - [ ] Authorization
  - I'm relying on the book I have, [Web Development with Flask](https://www.amazon.com.br/Flask-Web-Development-Miquel-Grinberg/dp/1491991739)
- [x] Automate database creation in sqlite
- [x] Create unit tests


- #### Bonus
- [x] Add the user who requested the cashback in the LogAPI
- [ ] Find an equivalent of Django's finalize response for Flask, and avoid so much LogAPI repetition
- [x] Use Docker

#### Step by step
The idea of creating an API that receives a payload and calculates the cashback and passes it on to another API is relatively simple. My idea in this project was to make it well structured, as if it were for my team.

Every process and reasoning can be seen by the commits, in fact I was created from "zero", my mastery is in Django and as soon as I was informed that I couldn't use it I went straight to Flask. 2 years ago I created a Flask project that I believed was my apse, but I was completely wrong kkkkk, because when I was trying to reuse what I had written there... I saw that doing it from scratch would be better, it was like a legacy system. Everything was very complex, I basically needed an endpoint (this was what I thought at first and then I created others) the data validations were very tangled... anyway, I preferred to focus on "relearning" Flask.

I prioritized making a well-structured and long-lasting project, implementing good practices, making it simple and easy to understand so that other devs who wanted to could continue with the work. As I said earlier, I created this project with the idea that it was for my team.

Finally, I would like to have finalized everything that I added in TODO but unfortunately time did not allow it.
