

![](770fa0497770252dc22b4fa902ebb384_img.jpg)

Figure 12 displays nine plots arranged in a 3x3 grid, comparing the True DTE (solid black line), Makarov lower bound (dashed red line), Makarov upper bound (dotted red line), and New lower bound (solid blue line). The x-axis ranges from 0 to 30, and the y-axis ranges from 0 to 1. The plots are labeled with parameters  $k_1$  and  $k_2$  in the top right corner of each subplot:

- Row 1:  $k_1=1, k_2=1$ ;  $k_1=1, k_2=10$ ;  $k_1=1, k_2=40$
- Row 2:  $k_1=5, k_2=1$ ;  $k_1=5, k_2=10$ ;  $k_1=5, k_2=40$
- Row 3:  $k_1=10, k_2=1$ ;  $k_1=10, k_2=10$ ;  $k_1=10, k_2=40$

The legend indicates: True DTE (solid black), Makarov lower (dashed red), Makarov upper (dotted red), New lower bound (solid blue).

Figure 12: New bounds v.s. Makarov bounds

$F_0$  and  $F_1$  over the support causes more triangles having positive probability lower bounds, which leads the improvement of my new lower bound. On the other hand, the Makarov lower bound gets no such informational gain because it uses only one triangle while my new lower bound takes advantage of *multiple* triangles.

# 5 Application to the Distribution of Effects of Smoking on Birth Weight

In this section, I apply the results presented in Section 3 to an empirical analysis of the distribution of smoking effects on infant birth weight. Smoking not only has a direct impact on infant birth weight, but is also associated with unobservable factors that affect infant birth weight. I identify marginal distributions of potential infant birth weight with and without smoking by making use of a state cigarette tax hike in Massachusetts (MA) in January 1993 as a source of exogenous variation. I focus on pregnant women who change their smoking behavior from smoking to nonsmoking in response to the tax increase. To identify the distribution of smoking effects, I impose a MTR restriction that smoking has nonpositive effects on infant birth weight with probability one. I propose an estimation procedure and report estimates of the DTE