# GateFactory

<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/GateFactory/master/docs/img/factory.png" alt="GateFactory"/>
</p>

## Installation

```
pip install gate
```

or install it on development mode:

```
git clone https://github.com/mertyildiran/GateFactory.git
cd GateFactory/
pip install -e .
```

### Run the Examples

#### Easy Classification Example

```
git clone https://github.com/mertyildiran/GateFactory.git
cd GateFactory/
python3 examples/classification_easy.py
```

#### Medium Classification Example

Download [CIFAR-10 python version](https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz) and place `CIFAR-10/original/cifar-10-batches-py/` folder inside `GateFactory/examples/` directory like:

```
cd ~/Downloads/
wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
tar -zxvf cifar-10-python.tar.gz
mv cifar-10-batches-py/ ~/Documents/GateFactory/examples/
```

and then run the example:

```
cd ~/Documents/GateFactory/
python3 examples/classification_medium.py
```

#### Render LaTeX

```
apt install texlive texlive-pictures
pdflatex factory.tex
sensible-browser factory.pdf
```
