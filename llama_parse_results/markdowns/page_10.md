

72

in (a) and (b), respectively. Therefore, from consideration of Case a, b and c,

$$\sup_{\{B_k\}_{k=-\infty}^{\infty}} \sum_{k=-\infty}^{\infty} \max \{\mu_{0,W} (B_k|w) - \mu_{1,W} (B_k^D|w), 0\}$$

$$= \sup_{\{b_k\}_{k=-\infty}^{\infty}} \sum_{k=-\infty}^{\infty} \max \left\{ F_{0,W} (b_k|w) - F_{1,W} \left(\frac{t_1 - t_W}{t_0 - t_W} b_{k+1} - \frac{t_1 - t_0}{t_0 - t_W} w|w\right), 0 \right\}$$

where $$\frac{t_0-t_W}{t_1-t_0}\delta + w \leq b_{k+1} \leq b_k$$. Consequently, the sharp upper bound is written as follows: letting $$F_{\Delta,W}^U (\delta|w)$$ be the sharp upper bound on $$\Pr (Y_1 - Y_0 \leq \delta|W = w)$$,

$$F_{\Delta}^U (\delta)$$

$$= \int F_{\Delta,W}^U (\delta|w) dF_W (w)$$

$$= \int \left\{ 1 - \sup_{\{B_k\}_{k=-\infty}^{\infty}} \sum_{k=-\infty}^{\infty} \max \{\mu_{0,W} (B_k|w) - \mu_{1,W} (B_k^D|w), 0\} \right\} dF_W$$

$$= 1 + \int \inf_{\{b_k\}_{k=-\infty}^{\infty}} \sum_{k=-\infty}^{\infty} \min \left\{ F_{1,W} \left(\frac{t_1 - t_W}{t_0 - t_W} b_{k+1} - \frac{t_1 - t_0}{t_0 - t_W} w|w\right) - F_{0,W} (b_k|w), 0 \right\} dF_W$$

where $$\frac{t_0-t_W}{t_1-t_0}\delta + w \leq b_{k+1} \leq b_k$$. ■

# Appendix B

Appendix B presents the procedure used to compute the sharp lower bound under MTR in Section 4 and Section 5. The following lemma is useful for reducing computational costs:

**Lemma B.1** Let

$$\{a_k\}_{k=-\infty}^{\infty} \in \arg\max_{\{a_k\}_{k=-\infty}^{\infty} \in \mathcal{A}_{\delta}} \sum_{k=-\infty}^{\infty} \max \{F_1 (a_{k+1}) - F_0 (a_k), 0\},$$

where $$\mathcal{A}_{\delta} = \{\{a_k\}_{k=-\infty}^{\infty} : 0 \leq a_{k+1} - a_k \leq \delta \text{ for each integer } k\}$$.

It is innocuous to assume that $$\{a_k\}_{k=-\infty}^{\infty}$$ satisfies $$a_{k+2} - a_k > \delta$$ for each integer $$k$$.

**Proof.** I will show that for any sequence $$\{a_k\}_{k=-\infty}^{\infty} \in \mathcal{A}_{\delta}$$ satisfying $$a_{k+2} - a_k \leq \delta$$ for some integer $$k$$, one can construct $$\{\tilde{a}_k\}_{k=-\infty}^{\infty} \in \mathcal{A}_{\delta}$$ with $$\tilde{a}_{k+2} - \tilde{a}_k > \delta$$ for each integer $$k$$ and

$$\sum_{k=-\infty}^{\infty} \max \{F_1 (a_{k+1}) - F_0 (a_k), 0\} \leq \sum_{k=-\infty}^{\infty} \max \{F_1 (\tilde{a}_{k+1}) - F_1 (\tilde{a}_k), 0\}.$$