import math
from scipy.stats import norm
from scipy.optimize import newton


def black_scholes_call(S, K, T, r, sigma):
    try:
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        N_d1 = norm.cdf(d1)
        N_d2 = norm.cdf(d2)
        call_price = S * N_d1 - K * math.exp(-r * T) * N_d2
        return call_price
    except ValueError:
        return None

def implied_volatility_call(option_price, S, K, T, r):
    call_price = black_scholes_call(S, K, T, r, 0.2)  # Using a fixed initial guess (0.2 in this example)

    if call_price is None:
        return None

    def black_scholes_call_diff(sigma):
        return call_price - option_price
    try:
        implied_vol = newton(black_scholes_call_diff, x0=0.2)
        return implied_vol
    except RuntimeError:
        return 0

def black_scholes_put(S, K, T, r, sigma):
    try:
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        N_minus_d1 = norm.cdf(-d1)
        N_minus_d2 = norm.cdf(-d2)

        put_price = K * math.exp(-r * T) * N_minus_d2 - S * N_minus_d1
        return put_price
    except ValueError:
        return None


def implied_volatility_put(option_price, S, K, T, r):
    put_price = black_scholes_put(S, K, T, r, 0.2)  # Using a fixed initial guess (0.2 in this example)

    if put_price is None:
        # Handle the math domain error here.
        # For example, you can return None or raise a custom exception.
        return None

    def black_scholes_put_diff(sigma):
        return put_price - option_price

    try:
        implied_vol = newton(black_scholes_put_diff, x0=0.2)
        return implied_vol
    except RuntimeError:
        return 0


