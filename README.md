# Barabasi-Albert Payment Network Simulation

Simulation of a Payment Network based on [BA99]. The result is a simulated network that cointains:
- A directed graph, where an edge `(i, j)` represents an obligation from firm `i` to firm `j` 
- An amount matrix, where the entry [i][j] indicates the amount that firm `i` owes to firm `j`

The resulting network shows:
a) the degree of the nodes in the network shows a scale free distribution (see `degree_distribution.png`)
b) the total amount of incoming and outgoing obligations of the nodes shows a scale free distribution (see `amount_distribution.png`)

Both the results are in line with the findings, from real-world dataset, of [Ber+21] and [Tam+12]

### Run

```
pip install -r requirements.txt
python3 main.py
```

### References

- [BA99](https://arxiv.org/abs/cond-mat/9910332)
- [SC13](https://www.degruyter.com/document/doi/10.5018/economics-ejournal.ja.2013-28/html)
- [Ber+21](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0250115)
- [Tam+12](https://www.worldscientific.com/doi/abs/10.1142/S2010194512007805?srsltid=AfmBOooZusoYKrxo5O33WceSPhyF1w8D1KTfvlZ__5e5uf0i2huuntMS)