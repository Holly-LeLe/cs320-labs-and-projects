# Flask File structure 

When first looking at a Flask python file, you might be thinking this looks a lot different than any of the python files you have written before, and for the most part your right.

## Use of Decorators

As it is probably the first time many of you have seen these, and they can be a little confusing at first. At a very high level decorators decorators are a way to pass a function, into another function. And you might be thinking why would I want to do that and well, they are not super commonly used. Here, below is an example of decatories that I stole from a Greeks for Greeks article. 

```python
# A simple decorator function
def decorator(func):
  
    def wrapper():
        print("Before calling the function.")
        func()
        print("After calling the function.")
    return wrapper

# Applying the decorator to a function
@decorator
def greet():
    print("Hello, World!")

greet()
```

Output:
```
Before calling the function.
Hello, World!
After calling the function.
```

Because of the @decorator on the 'greet' function, when that function is called it calls the decorator function, which is passed as argument 'func'. 

So in Flask when we see something along the lines of:
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, world!"
```

In this very simiple example the Flask decorator is taking the url of the visitor and if ends in '/' the user's web-client will end up rendering the html that is return from the home() function. 

## Module-level Entry point check

Another thing that might be new to you is the following that is commonly found at the bottom of flask python files:

```python
if __name__ == "__main__":
    app.run(debug=True)
```

Because python is an interpreted lanuage there is commonly not a "main" function like we see in other more "traditional" languages, like Java or C. What this tells the interpretor is when this file is ran from the command line (like python3 flaskapp.py), run the following code. In this explain it called app.run(debug=True), which is starting a flask website. 


