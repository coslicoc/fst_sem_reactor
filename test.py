import pytest
from solver import (
    stop_money_losses,
    reduce_money_losses,
    downtime_loss,
    reduction_loss,
    border_time,
    stop_power_loss,
    reduce_power_loss,
    stop_reactor_power,
    reduce_reactor_power,
    combined_reactor_power,
)

def test_stop_money_losses():
    assert stop_money_losses(0.2, 30, 1500) == 9000
    assert stop_money_losses(0.1, 50, 1000) == 5000
    assert stop_money_losses(0, 30, 1500) == 0  # Нулевая потеря

def test_reduce_money_losses():
    result = reduce_money_losses(0.1, 365, 912, 1095, 1500, 300, 500)
    expected = 0.1 * (500 * (912 - 365) + (500 - 300) * (912 - 1095))
    assert pytest.approx(result, 0.01) == expected

    
    '''result = reduce_money_losses(0.1, 365, 912, 1095, 1500, 700, 500)
    expected = 0.1 * 700 * (912 - 365)
    assert pytest.approx(result, 0.01) == expected
'''


def test_downtime_loss():
    assert downtime_loss(100, 912, 30, 1500, 300, 500) == 30 * 1500  
    assert downtime_loss(950, 912, 30, 1500, 300, 500) == 30 * (1500 - 300)  


def test_reduction_loss():
    result = reduction_loss(365, 912, 1095, 1500, 300, 500)
    expected = 500 * (912 - 365) + (500 - 300) * (1095 - 912)
    assert pytest.approx(result, 0.01) == expected


def test_border_time():
    result = border_time(30, 1095, 912, 1500, 500, 300, 0.2, 0.1)
    expected = 912 - (0.2 * 1500 * 30) / (0.1 * 500)
    assert pytest.approx(result, 0.01) == expected


    result = border_time(30, 1095, 912, 1500, 700, 500, 0.2, 0.1)
    expected = 912 - (0.2 * 1500 * 30) / (0.1 * 700)
    assert pytest.approx(result, 0.01) == expected


def test_stop_power_loss():
    result = stop_power_loss(0.5, 30, 1500, 500, 1095, 912)
    expected = 30 * 1500 * 0.5 * 912 + 30 * 0.5 * (1500 - 500) * (1095 - 912)
    assert pytest.approx(result, 0.01) == expected


def test_reduce_power_loss():
    result = reduce_power_loss(0.5, 500, 300, 1095, 912)
    expected = 0.5 * (0.5 * 912**2 - 912 * 1095 + 1095**2) * 300 + 0.5 * 1095 * 500 * (912 - 1095)
    assert pytest.approx(result, 0.01) == expected


def test_stop_reactor_power():
    assert stop_reactor_power(100, 50, 30, 1500) == 1500  
    assert stop_reactor_power(60, 50, 30, 1500) == 0  
    assert stop_reactor_power(90, 50, 30, 1500) == 1500  


def test_reduce_reactor_power():
    assert reduce_reactor_power(100, 150, 1500, 300) == 1500  
    assert reduce_reactor_power(200, 150, 1500, 300) == 1200  


def test_combined_reactor_power():
    assert combined_reactor_power(40, 50, 150, 30, 1500, 300) == 1500  
    assert combined_reactor_power(60, 50, 150, 30, 1500, 300) == 0  
    assert combined_reactor_power(160, 50, 150, 30, 1500, 300) == 1200  
