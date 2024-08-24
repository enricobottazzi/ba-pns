# barabasi-albert-network-distribution

Experiments on BA algorithm, based on https://arxiv.org/abs/cond-mat/9910332

Compared to the traditional BA algorithm, the generated graph is directed. This means that at every time increment, we add a new vertex with $m$ incoming edges and $m$ outgoing edges. Both incoming and outgoing edges are assigned following the linear preferential attachment rule defined in the paper.

```
pip install -r requirements.txt
python3 main.py
```
