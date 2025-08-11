# RealEstate AI MVP (local)

## Setup (macOS)

1. Open Terminal.
2. Create project folder (if not already): `cd ~/Projects` then `mkdir realestate-ai-mvp && cd realestate-ai-mvp`
3. Unzip the project files (if you downloaded the zip) or clone the repo.
4. Create a Python virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
5. Upgrade pip and install dependencies:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```
6. Run the pipeline:
   ```bash
   python src/data_prep.py
   python src/train_valuation.py
   python -m src.scoring
   ```
   (On some systems `python -m src.scoring` helps with relative imports.)
7. Run the dashboard:
   ```bash
   streamlit run src/streamlit_app.py
   ```
   Open the URL shown in Terminal (usually http://localhost:8501).

## Notes
- If you have Apple Silicon (M1/M2), use the system `python3` or install Python via Homebrew (`brew install python@3.11`) if `python3` is older.
- If any package fails during install, try `pip install --upgrade pip` first and then retry.
- Replace `data/sample_properties.csv` with your real data later; keep same column names or adapt scripts.
