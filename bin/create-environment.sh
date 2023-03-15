#!/usr/bin/zsh

CONDA=$HOME/anaconda3/condabin/conda

echo "Specify the environment name, or type ENTER to use dblp-converter"
read name
if [ -z "$name" ]; then
    name="dblp-converter"
fi

$CONDA create --yes --name "$name" python=3.10
$CONDA install --yes --name "$name" -c conda-forge poetry==1.3.2
$CONDA install --yes --name "$name" -c conda-forge chardet
$CONDA update --all --yes --name "$name"

echo "Activate the environment (conda activate $name) and run \"poetry install\""