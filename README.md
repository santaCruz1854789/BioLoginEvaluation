# BioLoginEvaluation
The repository for the evaluation part of BioLogin!

# Setup
Make sure to download Python 3.11.9 before proceeding with the setup.

Create a virtual environment with the Python3.11.9 interpreter:
```bash
python3.11 -m venv verification_env
```

Then activate it:
```bash
source verification_env/bin/activate
```

Install the dependencies from the requirements.txt file:
```bash
pip install -r requirements.txt
```

Create the following path on the root of the project:
Datasets/CASIA/archive/casia-webface/
```bash
mkdir -p Datasets/CASIA/archive/casia-webface/
```

Finally, download the [CASIA-WebFace](https://www.kaggle.com/datasets/debarghamitraroy/casia-webface) dataset and insert the **train.idx**, **train.lst**, **train.rec** files in the directory we just created.

# Creating the evaluation dataset
Run these scripts in the following order to generate the evaluation dataset:
1) CASIA_Dataset_generator.py
2) evaluation_database_generator.py

The evaluation dataset is going to be located inside the freshly created *Eval_Dataset* directory.

# Computing the graphs
After generating the evaluation dataset, set up the necessary parameters in the constants.py file and then run
```bash
python3 metrics_computations.py
```
The *det*, *roc* and *eer* graphs will be located in the graph folder.
