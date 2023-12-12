# Weather App

Fetches data from openweathermap.org displays and stores it into a database

## To make it work

Follow the instructions below to get the app up and running on your machine.

1.  Activate virtual environment
    ```shell
    python3 -m venv venv && source venv/bin/activate
    ```
1.  Make sure you recreate the same environment by installing what's in the requirements file
    ```shell
    pip install -r requirements.txt
    ```

1.  Or install everything individually
    ```shell
    pip install Flask
    ```
    ```shell
    pip install requests
    ```
    ```shell
    pip install Flask-SQLAlchemy
    ```
    ```shell
    pip install pytest
    ```
    ```shell
    pip install prometheus-flask-exporter
    ```

2. Tell the system which is the application file
    ```shell
    export FLASK_APP=app.py
    ```

## Database Handling

When running the program database should be created but if it didnt then please follow the following steps

1.  Create database
    ```shell
    flask create_db
    ```

## Run the Web App

1.  Run tests
    ```shell
    flask run
    ```

## Testing

1.  Unit tests
    ```shell
    python3 -m unittest appTest.py
    ```
2. Integration Test

    ```shell
    pytest appTest.py
    ```
    ```shell
    pytest appTest_integration.py
    ```
    
## Production Monitoring

Please make sure you have Prometheus installed:

```bash
brew install prometheus
```

Modify /usr/local/etc/prometheus.yml to match the example below. For homebrew modify /opt/homebrew/etc/prometheus.yml

```yaml
  scrape_configs:
  - job_name: 'weather_app'
    static_configs:
      - targets: ['127.0.0.1:5000']
    metrics_path: '/metrics'
```
Now, when Prometheus scrapes metrics from your Flask app, it will look for the /metrics endpoint on http://127.0.0.1:5000/metrics. (make sure the server is running)