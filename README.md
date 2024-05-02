# DVD rental app
I made this project to get faniliar with python. It was purely for educational purposes.

### This is a docker app containing two services;

<ul>
    <li>
        db - A service containing a PostgreSQL database.
    </li>
    <li>
        backend - A service running an Python Flask API.
    </li>
</ul>

### I started this project with a few things in mind;

<ul>
    <li>
        Show skills - First and foremost I needed to create something to showcase programming capabilities.
    </li>
    <li>
        Docker - I was interested in containerized applications and wanted to learn to use docker.
    </li>
    <li>
        Python - I studied in Java so I wanted to try my hands at a different language and so decided to learn python.
    </li>
    <li>
        SQL - I needed to brush up on SQL. 
    </li>
</ul>

### Usage

The application can be seen in action by following the steps below.

In order to use this application you first of all need to have docker installed - https://www.docker.com/. \
After downloading and installing docker (If you didn't have it already) you need to clone the repository. \
\
Once you have the repository cloned and docker installed you need to open a terminal and navigate to the \
folder containing the project and run the command `docker compose up`. \
\
Now the docker app should be up and running on your computer the last thing we need is a UI for the app, \
you can find one I created in React here: \
https://github.com/EinarLogiOskars/react-frontend.

### Testing

To run the tests, again navigate to the project directory in a terminal and run `docker-compose exec backend pytest -v`.
