# Task-Scheduler

Task-Scheduler is a lightweight application built to auto-schedule your daily/weekly/monthly/yearly routine with the motto of "Time Management? -> piece of cake".

  - built with **django** and **mysql**
  - no external dependencies
  - **Api** extensions available
  - **CLI** for terminal lovers:)

### Installation

TaskScheduler requires [Python](https://www.python.org/) 3.x to run (mysql-server / mysql-client optional).

Clone this repository.

```sh
$ git clone git@github.com:nirabhratapaswi/Task-Scheduler.git
$ cd Task-Scheduler
$ pip3 install -r ./requirements.txt
```

For production environments... (*coming soon*)

```sh
$ 
```

### Setting up Database, and Testing

TaskScheduler assumes you have mysql installed and set up. We need to create a new user and database.

Go to mysql shell
```sh
$ sudo mysql -u root -p
```
Enter your admin password, then inside the shell
```sh
> CREATE DATABASE TaskScheduler
> CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
> GRANT ALL PRIVILEGES ON TaskScheduler.* TO 'your_username'@'localhost';
> GRANT ALL PRIVILEGES ON test_.* TO 'your_username'@'localhost';
```
Replace **your_username** and **your_password** with actual username and password values you want.
Exit the shell by `ctrl+d`
Now you are ready to run the migrations and test
```sh
$ python3 manage.py migrate
$ python3 manage.py test TaskScheduler/
```
Check for errors if any, if not then application works fine:)

### Running the server

Continuing in shell
```sh
$ python3 manage.py runserver
```

### Using the GUI (to be updated soon)

Go to http://localhost:8000/taskscheduler and enjoy:)

### Command Line Interface (CLI)

Whilst in the project directory, there will be various command in the format
```sh
$ python manage.py <major_command> <sub_command_specification>
```
**major_commands** include patterns like add, delete and schedule. **sub_command_specification** is passed along with *major_command* to specify the type of listing or operation to be done. Usage combinations:
* addTask
* deleteTasks
* addBlocked
* deleteBlocked
* listTasks
    - all
    - done
    - undone
    - priority
    - deadlineover
* listBlocked
    - all
    - left
* schedule

### Docker (*coming soon*)
Task-Scheduler is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8000, so change this within the Dockerfile if necessary. When ready, simply use the Dockerfile to build the image.

```sh
$ cd Task-Scheduler
$ # docker commands (*coming soon*)
```
This will create the Task-Scheduler image and install necessary dependencies.

### Todos

 - Write Tests
 - Add configurable Scheduling Algorithms

License
----

MIT


**Free Software, Hell Yeah!**
