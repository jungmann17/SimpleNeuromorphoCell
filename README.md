# SimpleNeuromorphoCell
Create a simple single cell model from morphology made in Cell Builder (NEURON)
1. Open Cell Builder GUI from NEURON.
2. Build and define topology, geometry, and biophysics of a cell in Cell Builder.
3. Export model template: click Management > Export > Export to file (select directory and name the file CellTemplate.hoc)
4. Download SimpleSingleNeuromorphoCell.zip from GitHub
5. Unzip it then put the model template (make sure it is named CellTemplate.hoc) you just downloaded into the unzipped folder.
6. Run Model Generator with this command: python ModelGenerator.py.
7. Follow the prompts and insert the information asked for and then your model will be outputted.
8. Run your new model using this command: python NewModel.py
