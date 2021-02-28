# Task 1 Setup

I dockerized the application using docker-compose.
So to run the application docker is required.
To run the application complete the following steps:

Clone this repo and then run the following in the repo's directory:

```bash
docker-compose build

docker-compose up -d
```

The application should now be hosted on http://localhost:5000/
Navigating to this url should display "The server is running!"

## Endpoints:

### Rates
----
  Returns json data about the average price per day for the given geographic groups.

* **URL**

  /rates

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `origin=[string]`
   `destination=[string]`
   `date_from=[string: YYYY-MM-DD]`
   `date_to=[string: YYYY-MM-DD]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
    ```
    [
        {
            "day": "2016-01-01",
            "average_price": 129
        },
        {
            "day": "2016-01-02",
            "average_price": 139
        },
        ...
    ]
    ```
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `Invalid or missing input`

### Rates null
----
  Returns json data about a the average price per day for the given geographic groups, days with less than 3 prices are null.

* **URL**

  /rates_null

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `origin=[string]`
   `destination=[string]`
   `date_from=[string: YYYY-MM-DD]`
   `date_to=[string: YYYY-MM-DD]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
    ```
    [
        {
            "day": "2016-01-01",
            "average_price": 129
        },
        {
            "day": "2016-01-02",
            "average_price": null
        },
        ...
    ]
    ```
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `Invalid or missing input`

### Price
----
  Upload price for given date range

* **URL**

  /price

* **Method:**

  `POST`
  
*  **BODY Params**

   **Required:**
 
    ```
    {
        "origin": string,
        "destination": string,
        "date_from": string, (format: YYYY-MM-DD)
        "date_to": string, (format: YYYY-MM-DD)
        "price": number
    }
    ```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
    ```
    {'result': 'success'}
    ```
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `Invalid or missing input`
