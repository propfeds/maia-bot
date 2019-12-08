from typing import Any

# Hinting Any type since it can be yet another expression
def f_c(temp_f: Any) -> float:
    return (eval(str(temp_f))-32.0)/1.8

def c_f(temp_c: Any) -> float:
    return (eval(str(temp_c))*1.8)+32.0

def in_cm(length_in: Any) -> float:
    return eval(str(length_in))*2.54

def cm_in(length_cm: Any) -> float:
    return eval(str(length_cm))/2.54

def mi_km(dist_mi: Any) -> float:
    return eval(str(dist_mi))*1.609344

def km_mi(dist_km: Any) -> float:
    return eval(str(dist_km))/1.609344
