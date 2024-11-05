# Visualisaties van de cursu Data Analysis & Visualisation - Master Data science


This is the repository for the project within Master of Applied Data Science course "Data Analysis & Visualisation".
Auteur: Francesca Paulin (Studentnr 1882135)

# Setup the virtual environment
1. First, make sure you have python >= 3.11. You can check the version with `python --version`.
2. Make sure `rye` is there. Alternatively, use `pip` to install your environment.
    - check if it is installed by executing `rye --help`
3. Install the dependecies: navigate to the MADS-DAV folder where the `pyproject.toml` is located 
4. run `rye sync`.


# Run the visualisations

Download a chat from Whatsapp and put it in the `data/processed` folder.
In config.toml change the filename settings accordingly. 
input = <name of the source file>
csv = <name of the csv file> should be something like :"whatsapp-XXX-XXX.csv"
current = <name of the parq file> should be something like :"whatsapp-XXX-XXX.parq"

```bash
source .venv/bin/activate
```
For Windows:

```bash
source .venv/Scripts/activate
```

This will activate your virtual environment.
You can check which python is being used by running:
```bash
which python
```

After this, you can run the visualization with the following command, indicating the week number for the visualisation you want to see (number 1-5):

```bash
visualizer --week <nr>
```

```bash
visualizer --all  # to run all the visualizations
```
