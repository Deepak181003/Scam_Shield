# ScamShield — Complete Backend + Interactive UI

## Stack
- Flask
- scikit-learn
- TF-IDF + Logistic Regression
- CSV dataset
- HTML/CSS/JavaScript
- No React, Vite, Docker, SQLite, or external database

## Project flow

User input → Flask validation → detection engine → ML prediction + rule engine + URL analysis + stage detection → risk aggregation → scam type/stage/red flags/recommendation → result page.

## Backend modules

```text
backend/
├── detector.py          # orchestration
├── rules.py             # rule and scam taxonomy
├── stage_detector.py    # stage signals
├── url_analyzer.py      # URL heuristics
├── scoring.py           # risk aggregation
├── recommendations.py   # safety guidance
└── validation.py        # input validation
```

## API

- `GET /api/health`
- `GET /api/model`
- `GET /api/scam-types`
- `GET /api/stages`
- `POST /api/analyze`
- `POST /api/analyze/batch`

See `docs/BACKEND_API.md`.

## Setup

```bash
pip install -r requirements.txt
python ml/preprocess_data.py
python -m ml.train_model
python -m ml.evaluate_model
python app.py
```

Open `http://127.0.0.1:5000`.

## Backend smoke test

```bash
python tests_backend.py
```

## Important
The Week-3 dataset is a small educational dataset. The risk score is a prototype score, not a calibrated probability of fraud.


## Windows / IDE launch note

The application runs with Flask's development reloader disabled:

```python
app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
```

This avoids the `ValueError: signal only works in main thread of the main interpreter`
error that can occur when Flask is launched from some IDEs, embedded consoles,
or non-main threads.


## Easiest way to run on Windows

1. Extract the ZIP completely.
2. Open the `ScamShield_Backend_Complete` folder.
3. Double-click `start_scamshield.bat`.
4. The launcher installs the required Python packages and starts Flask.
5. Your browser should open automatically at:

`http://127.0.0.1:5000`

If the browser does not open automatically, copy that address into Chrome/Edge.

### If something fails

Run:

```bat
python check_backend.py
```

and copy the complete output.

### Manual start

```bat
python -m pip install -r requirements.txt
python app.py
```

Keep the terminal window open while using the website. Closing it stops the backend.
