import config



# OD calc => c1*v1 = c2*v2, solve for v1
def od_volume(x):
    return (config.target_od*config.total_vol)/x


# echo_cell_calc
def round_volume(x):
    return 25*round(x/25)


def h2o_topup(x):
    return config.total_vol-config.pre_vol-x


def num2well(num):
    alpha = "ABCDEFGHIJKLMNOP"
    #alpha = "ACEGIKMO"
    get_well = lambda x: f"{alpha[x%16]}{x//16+1}"
    get_well = lambda x: f"{alpha[x%16]}{x//16+1}"
    return get_well(num)


def pos2well(col:int, row:int)->str:
    #rows = "ABCDEFGHIJKLMNOP"
    rows = "ACEGIKMO"
    return f"{rows[row]}{col}"