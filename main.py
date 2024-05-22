import sys
from cliente import cliente
from servidor import servidor

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {'servidor', 'cliente'}:
        print("Uso: python main.py [servidor|cliente]")
        sys.exit(1)

    modo = sys.argv[1]
    if modo == 'servidor':
        servidor()
    else:
        cliente()
