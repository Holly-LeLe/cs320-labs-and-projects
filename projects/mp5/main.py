'''
Important!
Enter your full name (as it appears on Canvas) and NetID.
If you are working in a group (maximum of 3 members), include the full names and NetIDs of all your partners.
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP5
Student 1: Holly Li, wli682
Student 2: zhengyang yu, zyu447
Student 3: renxiang chao, rchao5
'''

import io
import re
import time
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask, jsonify, make_response, request, render_template, Response

# the source of my data is:
# https://www.kaggle.com/datasets/sadiajavedd/students-academic-performance-datasetz

app = Flask(__name__)
last_requests = {}

home_visits = 0
donate_counts = {"A": 0, "B": 0}
df = pd.read_csv("main.csv")

def save_dashboard_examples():
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) == 0:
        return

    # dashboard1.svg
    fig, ax = plt.subplots()
    ax.hist(df[numeric_cols[0]].dropna(), bins=10)
    ax.set_xlabel(numeric_cols[0])
    ax.set_ylabel("Frequency")
    ax.set_title(f"Histogram of {numeric_cols[0]} (bins=10)")
    fig.savefig("dashboard1.svg")
    plt.close(fig)

    # dashboard1-query.svg
    fig, ax = plt.subplots()
    ax.hist(df[numeric_cols[0]].dropna(), bins=25)
    ax.set_xlabel(numeric_cols[0])
    ax.set_ylabel("Frequency")
    ax.set_title(f"Histogram of {numeric_cols[0]} (bins=25)")
    fig.savefig("dashboard1-query.svg")
    plt.close(fig)

    # dashboard2.svg
    if len(numeric_cols) >= 2:
        plot_df = df[[numeric_cols[0], numeric_cols[1]]].dropna()
        fig, ax = plt.subplots()
        ax.scatter(plot_df[numeric_cols[0]], plot_df[numeric_cols[1]])
        ax.set_xlabel(numeric_cols[0])
        ax.set_ylabel(numeric_cols[1])
        ax.set_title(f"{numeric_cols[1]} vs {numeric_cols[0]}")
        fig.savefig("dashboard2.svg")
        plt.close(fig)

    # dashboard3.svg
    fig, ax = plt.subplots()
    ax.boxplot(df[numeric_cols[0]].dropna())
    ax.set_ylabel(numeric_cols[0])
    ax.set_title(f"Boxplot of {numeric_cols[0]}")
    fig.savefig("dashboard3.svg")
    plt.close(fig)

save_dashboard_examples()


@app.route("/")
def home():
    global home_visits
    home_visits += 1

    with open("templates/index.html") as f:
        html = f.read()

    if home_visits <= 10:
        if home_visits % 2 == 1:
            version = "A"
        else:
            version = "B"
    else:
        if donate_counts["A"] >= donate_counts["B"]:
            version = "A"
        else:
            version = "B"

    if version == "A":
        html = html.replace('href="/donate.html"', 'href="/donate.html?from=A"')
        html = html.replace("Donate", "Donate to Support Version A")
    else:
        html = html.replace('href="/donate.html"', 'href="/donate.html?from=B"')
        html = html.replace("Donate", "Donate to Support Version B")

    return html


@app.route("/browse.html")
def browse():
    table = df.to_html(index=False, float_format=lambda x: f"{x:.15f}")
    return render_template("browse.html", table=table)


@app.route("/browse.json")
def browse_json():
    ip = request.remote_addr
    now = time.time()

    if ip in last_requests:
        seconds_since_last_request = now - last_requests[ip]
        if seconds_since_last_request < 60:
            retry_after = int(60 - seconds_since_last_request)
            response = make_response("Too Many Requests", 429)
            response.headers["Retry-After"] = str(retry_after)
            return response

    last_requests[ip] = now
    return jsonify(df.to_dict(orient="records"))


@app.route("/visitors.json")
def visitors():
    return jsonify(list(last_requests.keys()))


@app.route("/email", methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if len(re.findall(r"^[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z]{3}$", email)) > 0:
        with open("emails.txt", "a") as f:
            f.write(email + "\n")

        with open("emails.txt", "r") as f:
            num_subscribed = len(f.readlines())

        return jsonify(f"thanks, your subscriber number is {num_subscribed}!")

    return jsonify("Stop being so careless. Please enter a valid email address.")


@app.route("/donate.html")
def donate():
    source = request.args.get("from")

    if source in donate_counts:
        donate_counts[source] += 1

    with open("templates/donate.html") as f:
        html = f.read()

    return html


def get_numeric_columns():
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    return numeric_cols


@app.route("/dashboard1.svg")
def dashboard1():
    numeric_cols = get_numeric_columns()

    if len(numeric_cols) == 0:
        return Response("No numeric columns found", mimetype="text/plain")

    col = numeric_cols[0]
    bins = request.args.get("bins", default=10, type=int)

    fig, ax = plt.subplots()
    ax.hist(df[col].dropna(), bins=bins)
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    ax.set_title(f"Histogram of {col} (bins={bins})")

    output = io.StringIO()
    fig.savefig(output, format="svg")
    plt.close(fig)

    return Response(output.getvalue(), mimetype="image/svg+xml")


@app.route("/dashboard2.svg")
def dashboard2():
    numeric_cols = get_numeric_columns()

    if len(numeric_cols) < 2:
        return Response("Need at least two numeric columns", mimetype="text/plain")

    x_col = numeric_cols[0]
    y_col = numeric_cols[1]

    plot_df = df[[x_col, y_col]].dropna()

    fig, ax = plt.subplots()
    ax.scatter(plot_df[x_col], plot_df[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{y_col} vs {x_col}")

    output = io.StringIO()
    fig.savefig(output, format="svg")
    plt.close(fig)

    return Response(output.getvalue(), mimetype="image/svg+xml")

@app.route("/dashboard3.svg")
def dashboard3():
    numeric_cols = get_numeric_columns()

    if len(numeric_cols) == 0:
        return Response("No numeric columns found", mimetype="text/plain")

    col = numeric_cols[0]

    fig, ax = plt.subplots()
    ax.boxplot(df[col].dropna())
    ax.set_ylabel(col)
    ax.set_title(f"Boxplot of {col}")

    output = io.StringIO()
    fig.savefig(output, format="svg")
    plt.close(fig)

    return Response(output.getvalue(), mimetype="image/svg+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=False)  # don't change this line!