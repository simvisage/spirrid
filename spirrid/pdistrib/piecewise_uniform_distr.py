'''
Created on 04.07.2013

@author: acki
'''

from scipy.stats.distributions import rv_continuous
import numpy as np


class piecewise_uniform_gen(rv_continuous):

    a_lower = 0.1
    a_upper = .5
    b_lower = .7
    b_upper = 2.0
    ratio = 0.8

    '''a and b , lower and upper area of distribution. ratio is weighting : a/(a+b)'''
    def _pdf(self, x):
        return self.ratio / (self.a_upper - self.a_lower) * (x <= self.a_upper) * (x >= self.a_lower) \
            + (1. - self.ratio) / (self.b_upper - self.b_lower) * (x >= self.b_lower) * (x <= self.b_upper)

    def _cdf(self, x):
        return self.ratio * (x - self.a_lower) / (self.a_upper - self.a_lower) \
                * (x <= self.a_upper) * (x >= self.a_lower) \
                + self.ratio * (x > self.a_upper) * (x < self.b_lower) \
                + (self.ratio + (1. - self.ratio) * (x - self.b_lower) \
                / (self.b_upper - self.b_lower)) * (x >= self.b_lower) * (x <= self.b_upper) \
                + 1.0 * (x > self.b_upper)

    def _ppf(self, x):
        return (x <= self.ratio) * (self.a_lower + (self.a_upper - self.a_lower) * x / self.ratio)\
            + (x > self.ratio) * (self.b_lower + (self.b_upper - self.b_lower) * (x - self.ratio) / (1 - self.ratio))

    def _stats(self):
        return 0, 0, 0, 0
        '''
        return ( ( a_lower + a_upper ) * ratio + ( b_lower + b_upper ) * ( 1 - ratio ) ) / 2., \
             ratio / 3. / ( a_upper - a_lower ) * ( a_upper ** 3 - a_lower ** 3 ) + \
             ( 1 - ratio ) / 3. / ( b_upper - b_lower ) * ( b_upper ** 3 - b_lower ** 3 ) - \
             ( ( ( a_lower + a_upper ) * ratio + ( b_lower + b_upper ) * ( 1 - ratio ) ) / 2. ) ** 2\
             , 0.0, 0.0
             '''

piecewise_uniform = piecewise_uniform_gen(a=0.0, name='piecewise_uniform')

if __name__ == '__main__':
    from matplotlib import pyplot as plt

    pu = piecewise_uniform

    P = np.linspace(0.0001, .999, 300)
    x = np.linspace(0.0, 2.0, 300)
    plt.plot(P, pu._ppf(P))
    plt.plot(pu._cdf(x), x, color='red', lw=2, ls='dashed')
    plt.show()
