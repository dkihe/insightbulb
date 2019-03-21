# Insightbulb

![March-20-2019](/img/03-20-2019.png)

A simple webapp to control Yeelight bulbs!  Powered with python!

**Fork us!**

Getting started:

You'll want to make sure you have virtualenv installed.
* ```$ virtualenv --version```

If you don't see a version number run:
* ```$ sudo pip install virtualenv```

After, ```cd``` into the project directory and run:
* ```virtualenv venv```

If you are using an IDE like pycharm, the environment will most likely
be started automatically for you.  If you are using a lightweight editor, you 
will probably have to run ```$ . venv/bin/activate``` for macOS and Linux.
If you are a windows user: ```$ venv/Scripts/activate``` is for you.
After running ```$ deactivate``` will bring you back to reality.

For a more detailed description, see the easy to read Flask [docs](http://flask.pocoo.org/docs/1.0/).

Once your environment is set up run the following:
* ```$pip install -r requirements.txt```


You'll also want to be making changes in the development environment:

* ```$ export FLASK_ENV=development```

To get things up and running:

* ```$ flask run```

You're all set!
