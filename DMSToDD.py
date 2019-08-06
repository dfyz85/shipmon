import math
def deg_to_dms(deg, type='lat'):
        decimals, number = math.modf(deg)
        print decimals, number
        d = int(number)
        m = float(decimals * 60)
        mins, m_int = math.modf(60 * deg)
        s = int( 60 * mins )
        compass = {
            'lat': ('N','S'),
            'lon': ('E','W')
        }
        compass_str = compass[type][0 if d >= 0 else 1]
        return 'DMS: {} {} {} {}'.format(abs(d), int(abs(m)), abs(s), compass_str), 'GPS: {} {:.3f} {}'.format(abs(d), m, compass_str)
print deg_to_dms(55.49218)