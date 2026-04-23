

23

| Correlation | All Blocked | All Scalar | Auto Blocking |
| ----------- | ----------- | ---------- | ------------- |
| 0.2         | \~230       | \~850      | \~850         |
| 0.5         | \~160       | \~420      | \~420         |
| 0.8         | \~50        | \~310      | \~310         |


| Model size (N) | All Blocked | All Scalar | Auto Blocking |
| -------------- | ----------- | ---------- | ------------- |
| 20             | \~1400      | \~1400     | \~7000        |
| 50             | \~250       | \~250      | \~1700        |
| 100            | \~50        | \~50       | \~850         |


Figure 3: Efficiency results for two contrived model structures: varying sized blocks of fixed correlation (left), and fixed sized blocks of varying correlation (right).

## Random Effects Model

In the random effects model (Table 1), automated blocking generates an MCMC algorithm identical to the Informed Blocking algorithm (blocking each <sub>α<sub>i</sub></sub>, <sub>β<sub>i</sub></sub> pair), which produces a tenfold improvement in Efficiency over the most efficient static algorithm – for this model, All Scalar sampling. The cut height h = 0.1 indicates that only the <sub>α<sub>i</sub></sub>, <sub>β<sub>i</sub></sub> pairs exhibit posterior correlations above 0.9. The Informed Cross-Level algorithm requires a substantially longer Runtime and produces a high ESS, which results in nearly identical Efficiency as the efficiently blocked Auto Blocking algorithm.

## Auto-Regressive Model

In the auto-regressive model (Table 1), an AR process value exhibited the slowest mixing under All Scalar sampling. When all 24 model parameters (AR process values, fixed effects, and one hyper-parameter) are blocked, the algorithm Runtime is nearly halved. This decrease in Runtime is largely due to the dependency structure inherent to the AR process. Scalar sampling of AR process values requires nearly a three-fold increase in density evaluations of the process values (since it's a