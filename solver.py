import numpy as np


def get_consts():
    T = float(input("Введите фиксированное время кампании реактора T: "))
    t = float(input("Введите время выхода из строя датчика t: "))
    T_reduce = float(input("Введите момент запланированного снижения мощности t0 (t0 < T): "))
    tau = float(input("Введите время простоя для ремонта tau: "))
    P_nom = float(input("Введите номинальную мощность реактора P_nom: "))
    P_stop = float(input("Введите снижение мощности во время ремонта P_red: ")) # не во время ремонта а вместо ремонта
    P_reduce = float(input("Введите запланированное снижение мощности в конце кампании реактора P_reduce: "))

    beta = float(input("Введите коэффициент потерь за время простоя beta: "))
    gamma = float(input("Введите коэффициент потерь при снижении мощности gamma: "))

    return T, t, T_reduce, tau, P_nom, P_stop, P_reduce, beta, gamma


def get_test_const():
    T = 1095
    t = 365
    T_reduce = 912
    T_stop = 300
    tau = 30
    P_nom = 1500  # float(input("Введите номинальную мощность реактора P_nom: "))
    P_stop = 500  # float(input("Введите снижение мощности во время ремонта P_red: "))
    P_reduce = 300  # float(input("Введите запланированное снижение мощности в конце кампании реактора P_reduce: "))

    beta = 0.2  # float(input("Введите коэффициент потерь за время простоя C_downtime: "))
    gamma = 0.1  # float(input("Введите коэффициент потерь при снижении мощности gamma: "))

    return T, t, T_reduce, T_stop, tau, P_nom, P_stop, P_reduce, beta, gamma


def stop_money_losses(beta, tau, P_nom):
    return beta * tau * P_nom


def reduce_money_losses(gamma, t, t_reduce, T, P_nom, P_reduce, P_stop):
    if P_stop < P_reduce:
        return gamma * P_stop * (t_reduce - t)
    return gamma * (P_stop * (t_reduce - t) + (P_stop - P_reduce) * (t_reduce - T))


# Формулы потерь
# Потери за счет простоя (1)
def downtime_loss(t, t_reduce, tau, P_nom, P_red, P_stop):
    if t < t_reduce:
        return tau * P_nom
    return tau * (P_nom - P_red)


# Потери за счет снижения мощности (2)
def reduction_loss(t, t_reduce, T, P_nom, P_red, P_stop):
    # если P_stop < P_reduce?
    # a = P_stop * (t_reduce - t) + (P_stop - P_red) * (T - t_reduce)
    if t < t_reduce:
        return P_stop * (t_reduce - t) + (P_stop - P_red) * (T - t_reduce)
    return (T - t_reduce) * (P_stop - P_red)


def border_time(tau, T, T_reduce, P_nom, P_stop, P_reduce, beta, gamma):
    '''
    :param tau: время простоя для ремонта
    :param P_nom: номинальная
    :param P_stop: понижение энергии при
    :param P_reduce: понижение энергии при
    :param beta: коэффициент
    :param gamma: коеффициент
    :return: оптимальное время
    '''
    if P_stop < P_reduce:
        return T_reduce - (beta * P_nom * tau) / (gamma * P_stop)
    return T_reduce - (beta * P_nom * tau) / (gamma * P_stop) + (P_stop - P_reduce) * (T_reduce - T) / P_stop


def stop_power_loss(a, tau, P_nom, P_reduce, T, T_reduce):
    Q = tau * P_nom * a * T_reduce + tau * a * (P_nom - P_reduce) * (T - T_reduce)
    return Q


def reduce_power_loss(a, P_stop, P_reduce, T, T_reduce):
    A = a * (0.5 * T_reduce ** 2 - T_reduce * T + T ** 2)
    B = a * T * P_reduce * (T_reduce - T)
    Q = A * P_stop + B
    return Q


def stop_reactor_power(t, t_stop, tau, P_nom):
    """
    :param t:
    :param t_stop:
    :param tau:
    :param P_nom:
    :return:
    """
    if t_stop < t <= t_stop + tau:
        return 0
    return P_nom


def reduce_reactor_power(t, T_reduce, P_nom, P_reduce):
    if t < T_reduce:
        return P_nom
    return P_nom - P_reduce


def combined_reactor_power(t, t_stop, t_reduce, tau, P_nom, P_reduce):
    if t_stop <= t <= t_stop + tau:
        return 0
    if t >= t_reduce:
        return P_nom - P_reduce
    return P_nom
