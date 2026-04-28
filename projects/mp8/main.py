'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 3 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP8
Student 1: <Holly Li>, <wli682>
Student 2: None
Student 3: None
'''

# Add imports used throughout the project here
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


class UserPredictor:
    def __init__(self):
        self.model = DecisionTreeClassifier(
            max_depth=8,
            random_state=320,
            class_weight="balanced"
        )
        self.columns = None
        self.id_col = "user_id"

    def _make_features(self, users, logs):
        users = users.copy()
        logs = logs.copy()

        if self.id_col not in users.columns:
            self.id_col = users.columns[0]

        X = pd.DataFrame(index=users[self.id_col])

        # only numeric columns from users
        for col in users.columns:
            if col != self.id_col and pd.api.types.is_numeric_dtype(users[col]):
                X[col] = users[col].values

        # log count
        X["log_count"] = logs.groupby(self.id_col).size()

        # seconds features
        if "seconds" in logs.columns:
            sec = logs.groupby(self.id_col)["seconds"].agg(["sum", "mean", "max"])
            sec.columns = ["seconds_sum", "seconds_mean", "seconds_max"]
            X = X.join(sec)

        X = X.fillna(0)
        return X

    def fit(self, train_users, train_logs, train_y):
        X = self._make_features(train_users, train_logs)

        if isinstance(train_y, pd.DataFrame):
            y = train_y.iloc[:, -1]
        else:
            y = train_y

        self.columns = X.columns
        self.model.fit(X, y)

    def predict(self, test_users, test_logs):
        X = self._make_features(test_users, test_logs)
        X = X.reindex(columns=self.columns, fill_value=0)
        return self.model.predict(X)