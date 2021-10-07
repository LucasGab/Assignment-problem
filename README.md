# Assignment-problem

A python solver of assignments problems (Operational research and problem optimization).

## Requirements

Just run pip install -r requirements.txt
Pulp for python: <https://github.com/coin-or/pulp>

GUROBI:

<https://www.gurobi.com/academia/academic-program-and-licenses/>

<https://www.gurobi.com/downloads/gurobi-software/>

<https://www.gurobi.com/documentation/7.0/quickstart_linux/software_installation_guid.html>

After install, run:

```bash
/opt/gurobi912/linux64/ sudo python3 setup.py install

export GUROBI_HOME="/opt/gurobi912/linux64"

export PATH="${PATH}:${GUROBI_HOME}/bin"

export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"
```
