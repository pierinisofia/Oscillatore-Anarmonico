
import argparse
import matplotlib.pyplot as plt
from scipy.integrate import simpson
import numpy as np
import sys

# Costanti fisiche
m = 1.0  
k = 1.0 

def parse_arguments():
    parser = argparse.ArgumentParser(description="Analisi vari oscillatori armonici")
    parser.add_argument('--potenziale', type=str, default='k6', 
                        choices=['k2', 'k4', 'k6', 'mod'], 
                        help='Scegli il potenziale: k2, k4, k6, mod')
    parser.add_argument('--confronta', action='store_true',
                        help="Sovrappone l'oscillatore armonico (k2) per comparare")
    return parser.parse_args()

def funzione_pot(tipo_pot):

    if tipo_pot == 'k2':
        return lambda x: (k * x**2), "Armonico (k2)"
    elif tipo_pot == 'k4':
        return lambda x: (k * x**4), "Anarmonico (k4)"
    elif tipo_pot == 'k6':
        return lambda x: (k * x**6), "Anarmonico Duro (k6)"
    elif tipo_pot == 'mod': 
        return lambda x: (k * np.abs(x)**(1.5)), "Sub-Armonico (mod)"
    else:
        print("Potenziale non riconosciuto.")
        sys.exit(1)

def periodo(x0, V): 
    if x0 == 0:
        return 0.0
    
    epsilon = 0.999999
    xi = np.linspace(0, x0 * epsilon, 1000)
    
    V_x0 = V(x0)
    V_xi = V(xi)
    
    
    fi = 1.0 / np.sqrt(V_x0 - V_xi + 1e-15)
    
    integ = simpson(y=fi, x=xi)
    T = np.sqrt(8 * m) * integ
    return T

def lanci(x_min, x_max, n, V_func):
	
    x_partenza = np.linspace(x_min, x_max, n)
    T_valori = []
    
    for i in x_partenza: 
        t = periodo(i, V_func)
        T_valori.append(t)

    return x_partenza, np.array(T_valori)

def main(): 
    args = parse_arguments()
    
    V_user, label_user = funzione_pot(args.potenziale)
    
    x_valori, y_valori = lanci(0.1, 5.0, 50, V_user)

    plt.figure(figsize=(10, 6))
    plt.plot(x_valori, y_valori, 'o-', color='teal', label=label_user)
    

    if args.confronta and args.potenziale != 'k2':
        print("--- Calcolo confronto Armonico ---")

        V_armonico = lambda x: k * x**2
        

        _, y_armonico = lanci(0.1, 5.0, 50, V_armonico)
        
        plt.plot(x_valori, y_armonico, '--', color='tomato', label='Riferimento Armonico (k2)')

    plt.xlabel('Ampiezza iniziale x0 [m]')
    plt.ylabel('Periodo T [s]')
    plt.title(f'Analisi Periodo: {args.potenziale}')
    plt.grid(True)
    plt.legend()

    plt.show()

if __name__ == "__main__":
    main()
