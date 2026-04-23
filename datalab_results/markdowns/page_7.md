

where

$$A=\frac{(x_3^2+y_2^2)^d|x_3^2+(y_3-y_1)^2|^d}{(x_3^2+(y_2-y_1)^2)^d(x_3^2+y_3^2)^d},$$
 (A9)

$$B=\frac{[(x_3-x_1)^2+(y_2-y_1)^2]^d}{(x_3-x_1)^{2d}}\times\frac{[(x_3-x_1)^2+(y_3-y_2)^2]^d}{[(y_3-y_1)^2+(x_3-x_1)^2]^d},$$
 (A10)

and

$$C=\frac{|x_1^2+y_1^2|^d|x_1^2+(y_2-y_1)^2|^d}{|x_1|^{2d}|y_2^2+x_1^2|^d}.$$
 (A11)

We write

$$ABC-B-C+1=(A-1)BC+(B-1)(C-1).$$
 (A12)

It is apparent from Eq. (A12) that the leading singularity originates from the first term,  $(A-1)BC\approx A-1\approx-2d(y_1-0)(y_3-y_2)$ . Introducing new variables as in the Sec. III and integrating over  $x_3$  we obtain

$$\Sigma^{(6)}=2d\mathrm{i}\frac{(Ja^d)^6\Gamma(5-6d)}{(-\mathrm{i}(\omega-k_y))^{5-6d}}\times\int_0^\infty\prod_{i=1}^3d\xi_i\frac{\xi_1^{1-2d}\xi_2^{-2d}\xi_3^{1-2d}}{(\alpha+\xi_1+\xi_2+\xi_3)^{5-6d}}.$$
 (A13)

Here again, the integrals are divergent on the upper limit. Similarly to the previous section we differentiate it once with respect to the variable  $\alpha$  introduced in Eq. (14) in order to isolate the leading logarithmic singularity,

$$\frac{\partial\Sigma^{(6)}}{\partial\alpha}=-2d\mathrm{i}\alpha^{-1}\frac{(Ja^d)^6\Gamma(6-6d)}{(-\mathrm{i}(\omega-k_y))^{5-6d}}\times\int_0^\infty\prod_{i=1}^3d\xi_i\frac{\xi_1^{1-2d}\xi_2^{-2d}\xi_3^{1-2d}}{(1+\xi_1+\xi_2+\xi_3)^{6-6d}}.$$
 (A14)

The remaining integrals are easily evaluated. The subsequent integration over  $\alpha$  restores the singularity in the

self energy correction,

$$\Sigma^{(6)}=2d\frac{-\mathrm{i}(Ja^d)^6\Gamma(1-2d)\Gamma^2(2-2d)}{(-\mathrm{i}(\omega-k_y))^{5-6d}}\times(\log\alpha+C),$$
 (A15)

where  $C$  is an integration constant. The singular part of Eq. (A15) is given by Eq. (24).

# Appendix B: Leading singularities at the shadow mass shell, $\omega\sim k_y$ to the fourth order.

In this appendix we evaluate the singular contributions to the Green function at the shadow mass shell,  $\omega\sim k_y$  to fourth order in the coupling constant. We start with the expression (A1) introduced in App. A1. In contrast to the discussion in App. A1 we anticipate the singularity at  $\omega=k_y$  to come from the region  $y_2\gg x_2$ , and introduce new variables accordingly,  $x_2=\xi y_2$ ,  $y_1=\eta y_2$ . Performing integration over  $y_2$  we obtain

$$\Sigma^{(4)}=\mathrm{i}(Ja^d)^4\int_0^\infty d\xi\int_0^1d\eta\frac{\Gamma(3-4d)\eta^{-2d}(1-\eta)^{-2d}}{\left[(-\mathrm{i}((\omega-k_y)+(\omega-k_x)\xi))\right]^{3-4d}}\times\left[\frac{|(1-\eta)^2+\xi^2|^d|\eta^2+\xi^2|^d}{|1+\xi^2|^d|\xi|^{2d}}-1\right].$$
 (B1)

We notice that the singularity at  $\omega\sim k_y$  comes from the region of small  $\xi$ . Therefore we keep only the first term in the square brackets in Eq. (B1). After performing remaining integrations over  $\xi$  we obtain

$$\Sigma^{(4)}=\frac{\mathrm{i}(Ja^d)^4\Gamma(1-2d)\Gamma(2-2d)\alpha^{2-2d}}{(-\mathrm{i}(\omega-k_x))^{3-4d}}.$$
 (B2)

We stress that contrary to the mass shell singularities discussed in App. A, where it was important to compute the self-energy, at the shadow mass shell it is enough to consider the Green function itself.

1. Ar. Abanov, A. V. Chubukov and J. Schmalian, Adv. Phys. **52**, 119 (2003) and references therein.
2. S. Sachdev, M. A. Metlitski, Y. Qi and C. Xu, arXiv: 0907.3732 and references therein.
3. M. Khodas and A. M. Tsvelik, arXiv:0910.3967.
4. N. Doiron-Leyraud *et.al.*, Nature (London) **447**, 565 (2007).
5. E. A. Yelland *et.al.*, Phys. Rev. Lett. **100**, 047003 (2008).
6. S. Sachdev, arXiv:0907.0008.