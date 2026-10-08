import sys
print("Python:", sys.version)
try:
    import flask
    print("Flask:", flask.__version__)
except Exception as e:
    print("Flask ERROR:", e)

try:
    import sklearn
    print("scikit-learn:", sklearn.__version__)
except Exception as e:
    print("scikit-learn ERROR:", e)

try:
    import joblib
    print("joblib: OK")
except Exception as e:
    print("joblib ERROR:", e)

try:
    import pandas
    print("pandas:", pandas.__version__)
except Exception as e:
    print("pandas ERROR:", e)

try:
    import app
    print("Backend import: OK")
    print("Routes:")
    for rule in app.app.url_map.iter_rules():
        print(" ", rule)
except Exception as e:
    print("Backend import ERROR:", repr(e))
    raise
