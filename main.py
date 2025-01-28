import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from solver import (
    border_time, stop_money_losses, reduce_money_losses, downtime_loss, reduction_loss, stop_power_loss,
    reduce_power_loss, stop_reactor_power, reduce_reactor_power, combined_reactor_power
)


def validate_input(value, name):
    try:
        value = float(value.replace(",", "."))
        if value < 0:
            raise ValueError(f"{name} не может быть отрицательным.")
        return value
    except ValueError:
        raise ValueError(f"Ошибка в параметре '{name}'. Убедитесь, что ввод корректен.")


# Функции для отображения графиков
def show_first_graphs(T, t, T_reduce, T_stop, tau, P_nom, P_stop, P_reduce, beta, gamma):
    time = np.linspace(0, T, 500)
    t_opt = border_time(tau, T, T_reduce, P_nom, P_stop, P_reduce, beta, gamma)
    stop_losses = [stop_money_losses(beta, tau, P_nom) for t in time]
    reduce_losses = [reduce_money_losses(gamma, t, T_reduce, T, P_nom, P_reduce, P_stop) for t in time]
    #downtime_losses = [reduce_money_losses(gamma, t, T_reduce, T, P_nom, P_reduce, P_stop) for t in time]
    #reduction_losses = [stop_money_losses(beta, tau, P_nom) for t in time]

    plt.figure(figsize=(10, 6))
    plt.axvline(t_opt, color="red", linestyle="--", label=f"Оптимальное время t_опт = {t_opt:.2f}")
    plt.plot(time, stop_losses, label="Потери при остановке")
    plt.plot(time, reduce_losses, label="Потери при снижении мощности")
    plt.xlabel("Время")
    plt.ylabel("Потери")
    plt.title("Графики потерь")
    plt.legend()
    plt.grid()
    plt.show()


def show_second_graphs(T, t, T_reduce, T_stop, tau, P_nom, P_stop, P_reduce, beta, gamma):
    #energy = np.linspace(0, P_nom, 500)
    time = np.linspace(0, T, 500)
    downtime_losses = [downtime_loss(t, T_reduce, tau, P_nom, P_reduce, P_stop) for t in time]
    reduction_losses = [reduction_loss(t, T_reduce, T, P_nom, P_reduce, P_stop) for t in time]
    #downtime_losses = [reduce_power_loss(0.5, P_stop, en, T, T_reduce) for en in energy]
    #reduction_losses = [stop_power_loss(0.5, tau, P_nom, P_stop, T, T_reduce) for en in energy]

    plt.figure(figsize=(10, 6))
    plt.plot(time, downtime_losses, label="Потери за счет простоя", linestyle="--")
    plt.plot(time, reduction_losses, label="Потери за счет снижения мощности")
    plt.xlabel("Время")
    plt.ylabel("Потери энергии")
    plt.title("Графики потерь")
    plt.legend()
    plt.grid()
    plt.show()

def show_third_graphs(T, t, T_reduce, T_stop, tau, P_nom, P_stop, P_reduce, beta, gamma):
    time = np.linspace(0, T, 500)
    stop_power = [stop_reactor_power(t, T_stop, tau, P_nom) for t in time]
    reduce_power = [reduce_reactor_power(t, T_reduce, P_nom, P_reduce) for t in time]
    combined_power = [combined_reactor_power(t, T_stop, T_reduce, tau, P_nom, P_reduce) for t in time]

    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    ax1, ax2, ax3, ax4 = axs.flatten()

    ax1.fill_between(time, stop_power, alpha=0.5, label="Мощность при остановке", color='blue')
    ax1.set_title("График мощности при остановке")
    ax1.set_xlabel("Время")
    ax1.set_ylabel("Мощность")
    ax1.grid()

    ax2.fill_between(time, reduce_power, label="Мощность при снижении", alpha=0.5, color='red')
    ax2.set_title("График мощности при снижении")
    ax2.set_xlabel("Время")
    ax2.set_ylabel("Мощность")
    ax2.grid()

    #axs[2].fill_between(time, combined_power, label="Суммарная мощность", alpha=0.5, color='green')
    ax3.fill_between(time, reduce_power, label="Мощность при снижении", alpha=0.25, color='red')
    ax3.fill_between(time, stop_power, alpha=0.25, label="Мощность при остановке", color='blue')
    #ax3.fill_between(time, combined_power, label="Суммарная мощность", alpha=0.5, color='violet')
    ax3.set_title("График суммарной мощности")
    ax3.set_xlabel("Время")
    ax3.set_ylabel("Мощность")
    ax3.grid()

    # axs[3].fill_between(time, reduce_power, label="Мощность при снижении", alpha=0.5, color='red')
    # axs[3].fill_between(time, stop_power, alpha=0.5, label="Мощность при остановке", color='blue')
    ax4.fill_between(time, combined_power, label="Суммарная мощность", alpha=0.5, color='violet')
    ax4.set_title("График суммарной мощности")
    ax4.set_xlabel("Время")
    ax4.set_ylabel("Мощность")
    ax4.grid()

    plt.tight_layout()
    plt.show()


def show_power_fourth_graphs(T, t, T_reduce, T_stop, tau, P_nom, P_stop, P_reduce, beta, gamma):
    power = np.linspace(0, P_nom, 500)
    stop_losses = [stop_power_loss(0.5, tau, P_nom, P_reduce, T, T_reduce) for w in power]
    reduce_losses = [reduce_power_loss(0.5, w, P_reduce, T, T_reduce) for w in power]

    plt.figure(figsize=(10, 6))
    plt.plot(power, stop_losses, label="Потери мощности при остановке", color="blue")
    plt.plot(power, reduce_losses, label="Потери мощности при снижении", color="red")
    plt.xlabel("Снижение мощности delta_W")
    plt.ylabel("Потери мощности")
    plt.title("Графики потерь мощности")
    plt.legend()
    plt.grid()
    plt.show()



root = tk.Tk()
root.title("Графическое отображение данных")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

entry_fields = {}
param_labels = [
    "T (Общее время)", "t (Время )", "T_reduce (Время снижения)", "T_stop (Время остановки)", "tau (Время простоя)",
    "P_nom (Номинальная мощность)", "P_stop (Мощность при остановке)", "P_reduce (Мощность при снижении)",
    "beta (Коэффициент потерь простоя)", "gamma (Коэффициент потерь снижения мощности)"
]

for i, label in enumerate(param_labels):
    ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky=tk.W)
    entry = ttk.Entry(frame)
    entry.grid(row=i, column=1)
    entry_fields[label] = entry


def set_default_values():
    defaults = {
        "T (Общее время)": 1095,
        "t (Время )": 365,
        "T_reduce (Время снижения)": 912,
        "T_stop (Время остановки)": 300,
        "tau (Время простоя)": 30,
        "P_nom (Номинальная мощность)": 1500,
        "P_stop (Мощность при остановке)": 500,
        "P_reduce (Мощность при снижении)": 300,
        "beta (Коэффициент потерь простоя)": 0.2,
        "gamma (Коэффициент потерь снижения мощности)": 0.1
    }
    for key, value in defaults.items():
        entry_fields[key].delete(0, tk.END)
        entry_fields[key].insert(0, str(value))

def get_parameters():
    try:
        T = validate_input(entry_fields["T (Общее время)"].get(), "T")
        t = validate_input(entry_fields["t (Время )"].get(), "t")
        T_reduce = validate_input(entry_fields["T_reduce (Время снижения)"].get(), "T_reduce")
        T_stop = validate_input(entry_fields["T_stop (Время остановки)"].get(), "T_stop")
        tau = validate_input(entry_fields["tau (Время простоя)"].get(), "tau")
        P_nom = validate_input(entry_fields["P_nom (Номинальная мощность)"].get(), "P_nom")
        P_stop = validate_input(entry_fields["P_stop (Мощность при остановке)"].get(), "P_stop")
        P_reduce = validate_input(entry_fields["P_reduce (Мощность при снижении)"].get(), "P_reduce")
        beta = validate_input(entry_fields["beta (Коэффициент потерь простоя)"].get(), "beta")
        gamma = validate_input(entry_fields["gamma (Коэффициент потерь снижения мощности)"].get(), "gamma")

        return T, t, T_reduce, T_stop, tau, P_nom, P_stop, P_reduce, beta, gamma
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))
        return None

def run_first_group():
    params = get_parameters()
    if params:
        show_first_graphs(*params[:8], params[8], params[9])

def run_second_group():
    params = get_parameters()
    if params:
        show_second_graphs(*params[:8], params[8], params[9])

def run_third_group():
    params = get_parameters()
    if params:
        show_third_graphs(*params[:8], params[8], params[9])


def run_power_loss_graphs():
    params = get_parameters()
    if params:
        show_power_fourth_graphs(*params[:8], params[8], params[9])

button1 = ttk.Button(frame, text="Денежные потери", command=run_first_group)
button1.grid(row=len(param_labels), column=0, padx=5, pady=5)

button2 = ttk.Button(frame, text="Потери энергии (от времени)", command=run_second_group)
button2.grid(row=len(param_labels) + 1, column=0, padx=5, pady=5)

button3 = ttk.Button(frame, text="Потери энергии (от снижения мощности)", command=run_power_loss_graphs)
button3.grid(row=len(param_labels) + 2, column=0, padx=5, pady=5)

button4 = ttk.Button(frame, text="Мощность реактора и потери (от t)", command=run_third_group)
button4.grid(row=len(param_labels) + 3, column=0, padx=5, pady=5)

button_defaults = ttk.Button(frame, text="Установить значения по умолчанию", command=set_default_values)
button_defaults.grid(row=len(param_labels) + 4, column=0, padx=5, pady=10)

root.mainloop()
