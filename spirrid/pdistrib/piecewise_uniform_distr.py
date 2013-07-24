'''
Created on 04.07.2013

@author: acki
'''
'''
Created on 20.06.2011

@author: axel
'''

from scipy.stats.distributions import rv_continuous
from numpy import pi, cos, sin, arccos
from scipy.stats.distributions import rv_continuous
import numpy as np
class piecewise_uniform_gen( rv_continuous ):
    import numpy as np
    '''a and b , lower and upper area of distribution. ratio is weighting : a/(a+b)'''
    def _pdf( self, x ):
        a_lower, a_upper, b_lower, b_upper, ratio = 0.0, 0.03, 0.03, 0.95, 0.83
        return 1 / ( a_upper - a_lower ) * ratio * ( x <= a_upper ) * ( x < b_lower ) * ( x >= a_lower ) + 1 / ( b_upper - b_lower ) * ( 1 - ratio )\
        *( x > a_upper ) * ( x >= b_lower ) * ( x <= b_upper ) + ( x <= a_upper ) * ( x >= b_lower ) * ( 1 / ( a_upper - a_lower ) * ratio + 1 / ( b_upper - b_lower ) * ( 1 - ratio ) )
        
    def _cdf( self, x ):
        a_lower, a_upper, b_lower, b_upper, ratio = 0.0, 0.03, 0.03, 0.95, 0.83
        return ( x - a_lower ) / ( a_upper - a_lower ) * ratio * ( x <= a_upper ) * ( x < b_lower ) * ( x >= a_lower ) + ( x > a_upper ) * ( x < b_lower ) * ratio\
            + ( ratio + ( x - b_lower ) / ( b_upper - b_lower ) * ( 1 - ratio ) ) * ( x >= b_lower ) * ( x <= b_upper ) * ( x > a_upper ) + ( x > b_upper )\
            + ( x < b_upper ) * ( x <= a_upper ) * ( x >= b_lower ) * ( ( x - b_lower ) / ( b_upper - b_lower ) * ( 1 - ratio ) + ( x - a_lower ) / ( a_upper - a_lower ) * ratio )
    def _ppf ( self, x ):
        a_lower, a_upper, b_lower, b_upper, ratio = 0.0, 0.03, 0.03, 0.95, 0.83
        return ( x <= ratio ) * ( a_lower + ( a_upper - a_lower ) * x / ratio )\
            + ( x > ratio ) * ( b_lower + ( b_upper - b_lower ) * ( x - ratio ) / ( 1 - ratio ) )

    def _stats( self ):
        return 0, 0, 0, 0
        '''
        return ( ( a_lower + a_upper ) * ratio + ( b_lower + b_upper ) * ( 1 - ratio ) ) / 2., \
             ratio / 3. / ( a_upper - a_lower ) * ( a_upper ** 3 - a_lower ** 3 ) + \
             ( 1 - ratio ) / 3. / ( b_upper - b_lower ) * ( b_upper ** 3 - b_lower ** 3 ) - \
             ( ( ( a_lower + a_upper ) * ratio + ( b_lower + b_upper ) * ( 1 - ratio ) ) / 2. ) ** 2\
             , 0.0, 0.0
             '''

piecewise_uniform = piecewise_uniform_gen( a = 0.0, name = 'piecewise_uniform' )

if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt
    
    ini = piecewise_uniform

    x_ppf = np.linspace( 0, 1, 1000 )
    plt.plot( x_ppf, ini._ppf( x_ppf ) )
    plt.show()

            
        
