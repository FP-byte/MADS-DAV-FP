# Visualisaties van de cursu Data Analysis & Visualisation - Master Data science

# Run the visualisations

Download a chat from Whatsapp and put it in the `data/processed` folder.
In config.toml change the settings accordingly. 
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
visualizer --all True # to run all the visualizations
```
