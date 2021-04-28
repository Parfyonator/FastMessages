# Fast Messages

API has one endpoint for GET and POST requests.

* **Method:**
  
  `GET`

  * **URL**

    `/messages/<key>`

  * **URL Params**

    **Optional:**

    `timeout=[integer]` (time to wait for message in seconds)

  * **Success Responses:**

    **Code:** `200` <br>
    **Body:** <br>
    ```
    {
        "message": <retrieved message>
    }
    ```

  * **Error Responses:**

    **Code:** `404` <br>
    **Body:** <br>
    ```
    {
        "detail": "Message with given key not found."
    }
    ```
  
    **Code:** `422` <br>
    **Body:** <br>
    ```
    {
        "detail": [
            {
                "loc": [
                    "query",
                    "timeout"
                ],
                "msg": <error message>,
                "type": <error type>
            }
        ]
    }
    ```

  `POST`

  * **URL**

    `/messages/<key>`

  * **Data Params**

    **Required:**

    `value=[string]` (message) <br>
    `ttl=[integer]` (time to live in db in seconds)

  * **Success Responses:**

    **Code:** `200` <br>
    **Body:** <br>
    ```
    null
    ```

  * **Error Responses:**

    **Code:** `409` <br>
    **Body:** <br>
    ```
    {
        "detail": "Message with given key already exist."
    }
    ```

    **Code:** `422` <br>
    **Body:** <br>
    ```
    {
        "detail": [
            {
                "loc": [
                    "body",
                    "ttl"
                ],
                "msg": <error message>,
                "type": <error type>
            }
        ]
    }
    ```

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

Run tests:

```
pytest
```

## Run in Docker

App:

```
docker-compose up
```

Tests:

```
docker-compose -f docker-compose.test.yml up
```
