# Bally's Interactive Data Engineering Assessment

## Q1
SQL query is present in the `q1.sql` file.

## Q2
### Build
The solution makes use of Flask and MySQL. It can be built using the including `docker-compose.yml`. To build and run, execute the below command in the same directory as `docker-compose.yml`.
```
docker compose up
```
The Flask application will then be running on `localhost:5000`.
The Docker build process includes a step to initialise all test data required.

---
## Using the API

### The total win amount for a given member

Make a request to the `/wins` endpoint.

> A `member_id` must be supplied.

Example:
```
localhost:5000/wins?member_id=1001
```

### The total wager amount for a given member

Make a request to the `/wagers` endpoint.

> A `member_id` must be supplied.

Example:
```
localhost:5000/wagers?member_id=1001
```

### The number of wagers placed by a given member

Make a request to the `/count-placed` endpoint.

> A `member_id` must be supplied.

Example:
```
localhost:5000/count-placed?member_id=1001
```

### Optional Arguments

All end points also accept the following additional arguments:

- `game_id` - Filter results to a specific game
- `month` - Filter results to a given month in the year. `YYYYMM` Format.

Example:
```
http://localhost:5000/count-placed?member_id=1001&game_id=2057&month=201709
```



