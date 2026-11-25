# TAP Python

## Set up the environment

1. Install Python 3.
2. Open PowerShell in the project folder.
3. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. Install the project packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run the notebooks

From the project folder, start Jupyter:

```powershell
jupyter notebook
```

In the Jupyter page, open the notebook you want to run and run its cells from top to bottom. If prompted to select a kernel, choose the Python environment created in `.venv`.

Notebooks are in the project folder and in the `day-12`, `day-14`, and `day-15` folders. Some exercises use the CSV files in `data`, so keep that folder in place.

