try:
    import flask
    print("Flask ok")
    import flask_sqlalchemy
    print("SQLAlchemy ok")
    import flask_login
    print("Login ok")
    import google.generativeai
    print("GenAI ok")
    import dotenv
    print("Dotenv ok")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")
