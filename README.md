# TODO:

Use https://github.com/zeromq/pyzmq with FastAPI to create distributed application montitoring. This is just an exercise - DO NOT use in production.


1. Create multiple docker images with "microservices" and one docker compose file to run them all [DONE].
2. Create central monitoring server which will receive info from each service. Central server will serve montitoring page with data from each service. [DONE]
3. Create web page that displays performance of each service in real time (use web sockets and zeromq). Use http://smoothiecharts.org/ to display performance graphs. [DONE]

<img width="1790" alt="Screenshot 2021-03-25 at 10 53 18" src="https://user-images.githubusercontent.com/16268031/112456983-923ddc00-8d5b-11eb-8869-9dbab0c07742.png">


