## Instrucciones

#### Parte de Anaconda.

* `conda --version` para asegurarnos que tenemos el programa _anaconda_ instalado.
* `conda list` lista de paquetes que el programa _anaconda_ instalo en nuestra pc.
* `conda env list` listar todos los environment de conda existentes.
* `conda env create -f environment.yml` para crear un environment de conda, con todas las dependencias requeridas.
* `conda activate curso_ing_datos` para activar el environment.
* `conda deactivate` para salir del environment.

#### Parte de Jupyter.

Con el environment de conda activado hacemos:

* `jupyter notebook` levantar la aplicación _Jupyter_.

**Dentro de un notebook**.

* presionando `b` añade una nueva celda debajo de donde esta posicionado.
* presionando `dd` elimina la celda donde esta posicionado.
* presionando `p` visualizas toda la lista de comandos existentes en _Jupyter_.
* presionando `m` lo definimos como una celda de _Markdown_.
* Dentro de una celda de _Markdown_, presionando `ctrl + enter` lo transforma por su correspondiente visualización.

## Ejecucion.

`python newspaper_receipe.py eluniversal_2020_05_10_articles.csv`
