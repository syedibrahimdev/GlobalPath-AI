import sys
print("Starting Test...")
try:
    from flask import Flask
    print("Flask Imported")
    app = Flask(__name__)
    print("Flask Initialized")
except Exception as e:
    print(f"Error: {e}")
print("End Test")
