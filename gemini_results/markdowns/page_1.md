be formulated for the general SINR regime as follows:

$$
\begin{aligned}
\underset{p_{n,k,l}}{\text{minimize}} \quad & \log_2 \prod_{l=1}^L \prod_{k=1}^K \prod_{n=1}^N \left( \frac{\sigma^2 + I_{n,l}}{p_{n,k,l}h_{n,k,l} + \sigma^2 + I_{n,l}} \right)^{\alpha_{n,k,l}} \\
\text{subject to} \quad & \sum_{n=1}^N \alpha_{n,k,l}p_{n,k,l} \leq P_{k,\max}, \quad \forall k, \forall l
\end{aligned} \tag{12}
$$

Note that the numerator and denominator in (12) are posynomials and minimizing a ratio between two posynomials is referred to be a truly non-convex NP hard intractable problem known as complimentary GP. However, this problem can be transformed into GP by letting the denominator $f(p) = p_{n,k,l}h_{n,k,l} + \sigma^2 + I_{n,l} = \sum_{l=1}^L \sum_{k=1}^K u_{n,k,l}(p)$ and approximating the denominator $f(p)$ with a monomial using the arithmetic/geometric mean inequality as follows:

$$
\sum_{l=1}^L \sum_{k=1}^K u_{n,k,l}(p) \geq \prod_{l=1}^L \prod_{k=1}^K \left( \frac{u_{n,k,l}(p)}{s_{n,k,l}} \right)^{s_{n,k,l}} \tag{13}
$$

where $s_{n,k,l} = \frac{u_{n,k,l}(p_0)}{f(p_0)}$. Thus, the problem can be solved by extending the single condensation method presented in [14] for multi-cell scenario. The details of centralized scheme A are presented in Algorithm 2.

## B. Centralized Scheme A: Complexity Analysis

The initial allocation phase has a complexity of $O(KN^2)$ which is the same as Algorithm 1. Next, we perform a one dimensional search for the user in cell $l$ with maximum incremental throughput at subcarrier $n$. The process is repeated for each subcarrier and cell. Thus, the computational complexity of this step is $O(KNL)$. Since, the process continues until convergence, (i.e., $M$ iterations), the complexity of this step can be written as $O(KNLM)$. Finally, the total complexity of subcarrier allocation phase is $O(KN^2 + NKLM)$.

The complexity of Phase II is difficult to determine, however, it can be measured in terms of the degree of difficulty (DoD) that in turn relies on the number of constraints and variables associated with the GP [15]. Since we are dealing with $LK$ power constraints and $LKN$ power variables, the total computational complexity of centralized scheme A is $O(KN^2 + NKLM) + DoD(LKN)$. Apparently it seems that implementing centralized GP/successive GP based schemes may not