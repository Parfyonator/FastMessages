# Fast Messages

API has one endpoint for GET and POST requests.

* **Method:**
  
  `GET`

  * **URL**

    `/messages/<key>`

  * **URL Params**

    **Optional:**

    `timeout=[integer]` (time to wait for message in seconds)

  * **Success Response:**

    **Code:** 200 <br>
    **Body:** `{"message": <retrieved message>}`

  * **Error Response:**

    **Code:** 404 <br>
    **Body:** `{"detail": "Message with given key not found."}`

  `POST`

  * **URL**

    `/messages/<key>`

  * **Data Params**

    **Required:**

    `value=[string]` (message) <br>
    `ttl=[integer]` (time to live in db in seconds)

  * **Success Response:**

    **Code:** `200` <br>
    **Body:** `null`

  * **Error Response:**

    **Code:** `409` <br>
    **Body:** `{"detail": "Message with given key already exist."}`


## Run in environment (pip)

Requirements:

  * `Python 3.8`

Setup environment:

```
python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

Start Redis (Docker):

```
docker run --name fastmessagesredis -p 6379:6379 redis:latest
```

Start app:

```
python api.py
```

## Run Application (Docker)

```
docker-compose up
```

## Run tests (Docker)

```
docker-compose -f docker-compose.test.yml up
```
