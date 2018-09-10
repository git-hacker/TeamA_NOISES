# N.O.I.S.E.S.

Noise Optimization & Intelligent Speech Enhancement System

This project attempts to magnify telephone conversation proficiency for truck drivers in specific environmental settings.

# Prereqs

1. Python 3.6: This project requires you to have a working Python 3.6 environment on your local system.
2. Tensorflow: This project adopts the power of neural networks to achieve certain functionality. Theoretically, Tensorflow 1.6+ would work, but I uses 1.8.0 on my system. Use `pip install tensorflow==1.8.0` to install Tensorflow in your Python 3 environment
3. Keras: The deep learning framework that we used on top of Tensorflow to speedup the neural network architecture implementations. Use `pip install Keras==2.1.6` to install
4. librosa: This python library serves as a tool to process the I/O of signal files. Installation `pip install librosa`
5. oct2py: A python wrapper of the open-source Matlab/Octave interpreter, serves as a tool to execute certain algorithm that we implemented in Matlab. `pip install oct2py`
6. numpy: One of the most crucial library that we use throughout the whole project, through which we used to manipulate vectors, matrices, and tensors. `pip install numpy`
7. Django: The functionalities are served in the form of RESTful APIs, which are implemented with Django 2.0.6. `pip install Django==2.0.6`
8. Any web servers that serves local static html files. I used `http-server`. To install, `npm install -g http-server`

# Run

### Clone the project
`git clone https://github.com/git-hacker/TeamA_NOISES.git`

### Run the API server

1. `cd` to the `/path/to/this/repo/Service` directory where the django project is located.
2. `python manage.py runserver 0.0.0.0:60000` to start the server

### Run frontend page

1. `cd` to the `/path/to/this/repo/Web` directory where the frontend codes are located.
2. `http-server` to start serving the web page.
3. visit http://localhost:8080 
