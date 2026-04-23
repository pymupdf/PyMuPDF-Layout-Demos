

Now I present the constrained optimization procedure to compute the sharp lower bound under MTR. I pay particular attention to the special case where  $a_{k+1} - a_k = \delta$  for each integer  $k$  at the optimum. In this case, the lower bound reduces to

$$\sup_{0\le y\le\delta}\sum_{k=-\infty}^\infty \max\left(F_1\left(y+(k+1)\delta\right)-F_0\left(y+k\delta\right),0\right), \tag{B.1}$$

and computation of (B.1) poses a simple one-dimensional optimization problem.

Let

$$V(\delta)=\sup_{0\le y\le\delta}\sum_{k=-\infty}^\infty \max\left(F_1\left(y+(k+1)\delta\right)-F_0\left(y+k\delta\right),0\right),$$

and

$$V_K(\delta)=\max_{y\in\{y^*+k\delta\}_{k=-\infty}^\infty}\sum_{k=-K}^K \max\left(F_1\left(y+(k+1)\delta\right)-F_0\left(y+k\delta\right),0\right),$$

where  $y^*\in \arg\max_{0\le y\le\delta}\sum_{k=-\infty}^\infty \max\left(F_1\left(y+(k+1)\delta\right)-F_0\left(y+k\delta\right),0\right)$  and  $K$  is a nonnegative integer.

**Step 1.** Compute  $V(\delta)$ .

**Step 2.** To further reduce computational costs, set  $K$  to be a nonnegative integer satisfying  $|V(\delta)-V_K(\delta)|<\varepsilon$  for small  $\varepsilon>0$ .<sup>24</sup>

**Step 3.** For  $J=K$ , solve the following optimization problem:

$$\sup_{\{a_k\}_{k=-J}^J\in\mathcal{S}_\delta^{J,K}(y)}\sum_{k=-J}^J \max\left\{F_1\left(a_{k+1}\right)-F_0\left(a_k\right),0\right\}, \tag{B.2}$$

where

$$\mathcal{S}_\delta^{J,K}(y)=\left\{\{a_k\}_{k=-J}^J;a_J\le y+K\delta,a_{-J}\ge y-K\delta,0\le a_{k+1}-a_k\le\delta,\delta$$

**Step 4.** Repeat Step 3 for  $J=K+1,\dots,2K$ .<sup>25</sup>

It is not straightforward to solve the problem (B.2) numerically in Step 3; the function  $\max\{x,0\}$  is nondifferentiable. Furthermore in practice, marginal distribution functions are often estimated in a complicated

<sup>24</sup>I put  $\varepsilon=10^{-5}$  for the implementation in Section 4 and Section 5.

<sup>25</sup>By Lemma B.1, I considered  $J=K, K+1, \dots, 2K$  for the sequence  $\{a_k\}_{k=-J}^J$  and compared the values of local maxima achieved by  $\{a_k\}_{k=-J}^J$  with  $V_K(\delta)$