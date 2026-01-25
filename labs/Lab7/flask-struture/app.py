from flask import Flask
app = Flask(__name__)

user_is_admin = False  # Try changing this later

def require_admin(func):
    def wrapper():
        # If the user is admin, return the function
        # Otherwise, return "Access denied!"
    return wrapper

@app.route("/")
def home():
    return "Welcome to the site!"

# TODO: Add a new route /admin
# If user_is_admin is False, return "Access denied!" (This is handled by the decorator)
# If user_is_admin is True, return "Welcome, admin!"

if __name__ == "__main__":
    app.run("0.0.0.0", "5000", debug=True, threaded=False)