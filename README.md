# KBTU map bot

Bot is created for finding fastest path to some location at KBTU

## About

Bot written on **python** with computation part on **c++**

## Details

### Integration with c++

Use following commands to compile cpp file into python module

c++ -O3 -Wall -shared -std=c++11 -fPIC \`python3 -m pybind11 --includes\` 
graph.cpp -o graph\`python3-config --extension-suffix\`

**_Note:_** integration with **c++** done with **pybind11**

### Contributors

1. [@mebr0](https://github.com/MeBr0) - Yergali Azamat
2. [@thesafatem](https://github.com/thesafatem) - Safargaliyev Temirlan
