# Django Stream Framework Example

You can log in to your account or register as a new user if you don't have an account. When you pin items on the trending page, they will appear in the feeds of your followers. There are two feed pages Flat and Aggregated, they both have a different purpose.

- The flat Feed page contains all the feeds pinned by your followers.
- Aggregated Feed page contains group activities from all followers combined.

Pin a few items and have a look at the Flat and Aggregated feed pages.


<p align="center">
    <img width="800" alt="Screenshot 2021-06-05 at 21 46 17" src="https://user-images.githubusercontent.com/46227224/120898254-a9485680-c647-11eb-8044-53e913cb6c8f.png">
    <img width="800" alt="Screenshot 2021-06-05 at 21 46 37" src="https://user-images.githubusercontent.com/46227224/120898259-b1a09180-c647-11eb-9d75-2ba9aebf7f01.png">
</p>


## Installation

1. git clone docker branch

    ```bash
    $ git clone -b docker https://github.com/Saadmairaj/django_stream_framework.git
    ```

2. Change directory to `django_stream_framework`

    ```bash
    $ cd django_stream_framework
    ```

3. Run the following command to run it locally

    ```bash
    $ docker-compose up -d
    ```
    
    Redis server should also start running with the docker-compose command

  ### Administration credentials:
  ```
  user:   admin 
  pass:   admin
  ```
