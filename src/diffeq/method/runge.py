
def runge_rule(y_i: float, y_i_half: float, p: int, eps: float) -> bool:
    '''
    Правило Рунге.
    '''
    return abs(y_i - y_i_half) / (2 ** p - 1) <= eps
