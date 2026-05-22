from flask import Flask  # type: ignore

app = Flask(__name__)  # type: ignore[reportUnknownVariableType]

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # type: ignore[reportUnknownMemberType]
