# Customer Analytics — Big Data Pipeline (CSCI461)

## Team Members
- Noran Elhalwagui
- Ayten Hassan
- Myar Sadek
- Menna Sherief

## Requirements Checklist
- Docker base image: `python:3.11-slim`
- Packages installed: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `scipy`, `requests`
- Workdir in container: `/app/pipeline/`
- Pipeline scripts copied to: `/app/pipeline/`
- Container starts with interactive bash shell

## How To Build And Run (Docker)
From inside the `customer-analytics/` folder:

### Option A — Run step-by-step (interactive)
1. Build the image:
   - `docker build -t customer-analytics:latest .`
2. Run the container:
   - `docker run -it --name customer-analytics-pipeline customer-analytics:latest`
3. Inside the container, run the pipeline starting from the raw dataset:
   - `python ingest.py results/data_raw.csv`
4. Exit the container shell:
   - `exit`
5. Cleanup (recommended):
   - `docker rm -f customer-analytics-pipeline`

Why cleanup?
- If you don’t remove the container, it stays on your machine and you may get a “name already in use” error on the next run, and it will continue to take disk space.

### Option B — One command to run + export results (recommended)
From the repository root (the folder that contains `customer-analytics/`):
- `./customer-analytics/summary.sh`

By default, `summary.sh` uses `customer-analytics/results/data_raw.csv` as the input dataset. If your raw dataset is stored elsewhere, pass it as an argument:
- `./customer-analytics/summary.sh /path/to/data_raw.csv`

This will:
- Build the Docker image
- Run the full pipeline inside a container
- Copy outputs into `customer-analytics/results/` on the host
- Stop and remove the container automatically

## Execution Flow (Script Chaining)
The pipeline is chained exactly in this order:
1. `ingest.py` reads the input dataset path (CLI arg) and saves `data_raw.csv`, then calls `preprocess.py`.
2. `preprocess.py` performs:
   - Data cleaning (missing values, duplicates)
   - Feature transformation (encoding + scaling)
   - Dimensionality reduction (PCA)
   - Discretization (binning)
   Then saves `data_preprocessed.csv` and calls `analytics.py`.
3. `analytics.py` generates textual insights and writes:
   - `insight1.txt`, `insight2.txt`, `insight3.txt`
   Then calls `visualize.py`.
4. `visualize.py` generates 3 plots in one figure and saves `summary_plot.png`, then calls `cluster.py`.
5. `cluster.py` runs K-Means and writes `clusters.txt`.

## Outputs
After running, these files are generated in the container (and copied to `customer-analytics/results/` by `summary.sh`):
- `data_raw.csv`
- `data_preprocessed.csv`
- `insight1.txt`, `insight2.txt`, `insight3.txt`
- `summary_plot.png`
- `clusters.txt`

## Sample Outputs
Example insights:
- `insight1.txt`: "The dataset contains 40677 rows and 16 columns."
- `insight2.txt`: "The average value of rating is 4.41."
- `insight3.txt`: "The most frequent value in rating_category is Medium."

Example clustering counts:
- `Cluster 0: 40456 samples`
- `Cluster 1: 215 samples`
- `Cluster 2: 6 samples`

Screenshot/sample plot:
- See `customer-analytics/results/summary_plot.png`

## Notes
- If you run scripts locally (outside Docker), install dependencies with:
  - `pip install -r customer-analytics/requirements.txt`
