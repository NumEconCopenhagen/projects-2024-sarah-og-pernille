import sympy as sm
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, widgets

class SolowModel:
    def __init__(self, s, delta, n, B, alpha):
        self.s = s
        self.delta = delta
        self.n = n
        self.B = B
        self.alpha = alpha

    def steady_state_capital(self):
        solow_ss_k = lambda k: k - ((self.s*self.B*k**self.alpha+(1-self.delta)*k)/(1+self.n))
        result_k = optimize.root_scalar(solow_ss_k,bracket=[0.1,100],method='brentq')
        print(result_k)
        return result_k.root

    def steady_state_output(self, k_star):
        solow_ss_y = lambda y: y - (self.B*k_star**self.alpha)
        result_y = optimize.root_scalar(solow_ss_y,bracket=[0.1,100],method='brentq')
        print(result_y)
        return result_y.root
    
    def steady_state_capital_bisect(self):
        solow_ss_k_bisect = lambda k: k - ((self.s * self.B * k ** self.alpha + (1 - self.delta) * k) / (1 + self.n))
        result_k_bisect = optimize.root_scalar(solow_ss_k_bisect, bracket=[0.1, 100], method='bisect')
        print(result_k_bisect)
        return result_k_bisect.root

    def steady_state_output_bisect(self, k_star):
        solow_ss_y_bisect = lambda y: y - (self.B * k_star ** self.alpha)
        result_y_bisect = optimize.root_scalar(solow_ss_y_bisect, bracket=[0.1, 100], method='bisect')
        print(result_y_bisect)
        return result_y_bisect.root    


    def basic_solow_diagram(self, k, n, s, B, alpha, delta, kmax, kline):
        # Definition of the values of k, the growth rate of k and the diagonal line
        k_values = np.linspace(0, kmax, 1000)
        k_growth = s * B * k_values ** alpha
        diagonal = (n + delta) * k_values

        # Calculation of steady state for capital per capita
        k_star = ((B * s) / (n + delta)) ** (-1 / (alpha - 1))

        # The figure size and the two graphs
        plt.figure(figsize=(8, 5))
        plt.plot(k_values, diagonal, label=r'$(n+\delta)k_t$', color='black')
        plt.plot(k_values, k_growth, label=r'$y_t = sBk_t^{\alpha}$', color='mediumorchid')

        # The steady state point, the starting point and the labels:
        plt.axvline(x=kline, linestyle='--', color='royalblue', label=r'$k_0$')
        plt.axvline(x=k_star, linestyle='--', color='gold', label=r'$k*$')
        plt.xlim(0, kmax)
        plt.xlabel('$k_t$')
        plt.ylabel('$k_{t+1}$')
        plt.legend()
        plt.title('The Basic Solow Diagram')
        plt.grid(True)
        plt.show()

    def interactive_plot_basic(self):
        interact(self.basic_solow_diagram,
                 k=widgets.fixed(0),
                 alpha=widgets.FloatSlider(description=r'α', min=0, max=0.9, step=0.05, value=1/3),
                 delta=widgets.FloatSlider(description=r'δ', min=0, max=0.1, step=0.01, value=0.05),
                 s=widgets.FloatSlider(description='s', min=0.01, max=0.8, step=0.05, value=0.2),
                 n=widgets.FloatSlider(description='n', min=0.01, max=0.1, step=0.005, value=0.02),
                 B=widgets.fixed(1),
                 kmax=widgets.IntSlider(description='x axis', min=1, max=30, step=10, value=100),
                 kline=widgets.FloatSlider(description='k_0', min=0, max=100, step=0.1, value=20))


class SolowModelTech:
    def __init__(self, s, delta, n, g, alpha):
        self.s = s
        self.delta = delta
        self.n = n
        self.g = g
        self.alpha = alpha

    def steady_state_capital_t(self):
        solow_ss_k_t = lambda k: k - ((self.s * k ** self.alpha + (1 - self.delta) * k) / ((1 + self.n) * (1 + self.g)))
        result_k_t = optimize.root_scalar(solow_ss_k_t, bracket=[0.1, 100], method='brentq')
        return result_k_t.root

    def steady_state_output_t(self, k_star):
        solow_ss_y_t = lambda y: y - (k_star ** self.alpha)
        result_y_t = optimize.root_scalar(solow_ss_y_t, bracket=[0.1, 100], method='brentq')
        return result_y_t.root
    

    def solow_diagram(self, k, n, s, g, alpha, delta, kmax_t, kline_t):
        # Definition of the values of k, the growth rate of k and the diagonal line
        k_values_t = np.linspace(0, kmax_t, 1000)
        k_growth_t = s * k_values_t ** alpha
        diagonal_t = (n + g + delta + n * g) * k_values_t

        # Calculation of steady state for capital per capita
        k_star_t = ((delta + g * n + g + n) / s) ** (1 / (alpha - 1))

        # The figure size and the two graphs
        plt.figure(figsize=(8, 5))
        plt.plot(k_values_t, diagonal_t, label=r'$(\delta+g*n+g+n)k_t$', color='black')
        plt.plot(k_values_t, k_growth_t, label=r'$y_t = sk_t^{\alpha}$', color='mediumorchid')

        # The steady state point, the starting point and the labels:
        plt.axvline(x=kline_t, linestyle='--', color='royalblue', label=r'$k_0$')
        plt.axvline(x=k_star_t, linestyle='--', color='gold', label=r'$k*$')
        plt.xlim(0, kmax_t)
        plt.xlabel('$\~{k}_t$')
        plt.ylabel('$\~{k}_{t+1}$')
        plt.legend()
        plt.title('The Solow Diagram with technological growth')
        plt.grid(True)
        plt.show()

    def interactive_plot(self):
        interact(self.solow_diagram,
                 k=widgets.fixed(0),
                 alpha=widgets.FloatSlider(description=r'α', min=0, max=0.9, step=0.05, value=1/3),
                 delta=widgets.FloatSlider(description=r'δ', min=0, max=0.1, step=0.01, value=0.05),
                 s=widgets.FloatSlider(description='s', min=0.01, max=0.8, step=0.05, value=0.2),
                 n=widgets.FloatSlider(description='n', min=0.01, max=0.1, step=0.005, value=0.02),
                 g=widgets.FloatSlider(description='g', min=0, max=0.8, step=0.002, value=0.02),
                 kmax_t=widgets.IntSlider(description='x axis', min=1, max=30, step=10, value=100),
                 kline_t=widgets.FloatSlider(description='k_0', min=0, max=100, step=0.1, value=20))


