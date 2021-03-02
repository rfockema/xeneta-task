# Xeneta tasks

It took me around 6 hours to complete the tasks. It took me longer than I expected, because I never built a service from scratch before using flask.

# Task 2

For the batch processing task I would create 2 API's, where files can be uploaded containing the price data.

The first API, will accept compressed csv files for a start, it can be extended to accept other file types if needed. All the files however need to conform to the specified format. The second API, will also accept files containing the price data, however how the files are processed will depend on the data source ID. This API requires more development work, because for each data source functionality will need to be added, on how to process the data for the specific source. The ideal situation is that most data can be converted to fit the format required for the first API.

For both API's the files will be backed up on object storage, for example AWS S3. After the files are backed up a worker can start to write the data to the DB. The amount of records written to the DB per session can be configured. The worker will track how many records have been written for the specific file. If a session fails, the worker knows how many records has been written successfully for the file and it can start the session again without writing duplicate data. For each session the data format will be validated before trying to write to the DB. After the all the data and the file has been written to the DB, the file can be removed from the object storage.

# Task 1 Setup

I dockerized the application using docker-compose.
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
 
   * `origin=[string]`
   * `destination=[string]`
   * `date_from=[string: YYYY-MM-DD]`
   * `date_to=[string: YYYY-MM-DD]`

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
 
   * `origin=[string]`
   * `destination=[string]`
   * `date_from=[string: YYYY-MM-DD]`
   * `date_to=[string: YYYY-MM-DD]`

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
