

![](770fa0497770252dc22b4fa902ebb384_img.jpg)

Figure 3 displays two plots comparing the efficiency of three MCMC algorithms (All Blocked, All Scalar, and Auto Blocking) across varying model structures.

The left plot shows Efficiency (effective samples / time) versus Correlation (0.2, 0.5, 0.8). The right plot shows Efficiency (effective samples / time) versus Model size (N) (20, 50, 100).

In both plots, the Auto Blocking algorithm consistently achieves the highest efficiency, especially as correlation increases or model size grows. The All Scalar algorithm generally performs better than All Blocked sampling.

Figure 3: Efficiency results for two contrived model structures: varying sized blocks of fixed correlation (left), and fixed sized blocks of varying correlation (right).

# Random Effects Model

In the random effects model (Table 1), automated blocking generates an MCMC algorithm identical to the Informed Blocking algorithm (blocking each  $\alpha_i$ ,  $\beta_i$  pair), which produces a tenfold improvement in Efficiency over the most efficient static algorithm – for this model, All Scalar sampling. The cut height  $h = 0.1$  indicates that only the  $\alpha_i$ ,  $\beta_i$  pairs exhibit posterior correlations above 0.9. The Informed Cross-Level algorithm requires a substantially longer Runtime and produces a high ESS, which results in nearly identical Efficiency as the efficiently blocked Auto Blocking algorithm.

# Auto-Regressive Model

In the auto-regressive model (Table 1), an AR process value exhibited the slowest mixing under All Scalar sampling. When all 24 model parameters (AR process values, fixed effects, and one hyper-parameter) are blocked, the algorithm Runtime is nearly halved. This decrease in Runtime is largely due to the dependency structure inherent to the AR process. Scalar sampling of AR process values requires nearly a three-fold increase in density evaluations of the process values (since it’s a