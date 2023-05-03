#include <iostream>
using namespace std;

int menu() {
  int opc;
    cerr << "1-Medicamentos POS" << endl;
    cerr << "2-Medicamentos NO POS" << endl;
    cerr << "3-Salir" << endl;
    cerr << "Digite su opción: ";
    cin >> opc;
  return opc;
}

int submenu1() {
  int opc;
  cerr << "10-Acetaminofén - Precio Unitario: $100" << endl;
  cerr << "20-Diclofenaco – Precio unitario: $350" << endl;
  cerr << "30-Ibuprofeno – Precio Unitario: $500" << endl;
  cerr << "Digite su producto: ";
  return opc;
}

int submenu2() {
  int opc;
  cerr << "40-Zidovudina - Precio Unitario: $1000000" << endl;
  cerr << "50-Carmustina - Precio Unitario: $500000" << endl;
  cerr << "Digite su producto: ";
  cin >> opc;
  return opc;
}

int main() {
  string cliente, cedula;
  int totCompra, iva, acetaminofen = 0, diclofenaco = 0, ibuprofeno = 0;
  int totAcetaminofen = 0, totDiclofenaco = 0, totIbuprofeno = 0;
  int zidovudina = 0, carmustina = 0;
  int totZidovudina = 0, totCarmustina = 0;
  int opc = -1, cant;
  cerr << "Digite el nombre: ";
  getline(cin, cliente);
  cerr << "Digite la cédula: ";
  cin >> cedula;
  while(opc != 3) {
    opc = menu();
    if(opc == 1) {
      opc = submenu1();
      cin >> opc;
      if(opc == 10) {
        cerr << "Digite la cantidad Acetaminofén: ";
        cin >> cant;
        acetaminofen += cant;
        totAcetaminofen += (cant * 100);
      }
      if(opc == 20) {
        cerr << "Digite la cantidad Diclofenaco: ";
        cin >> cant;
        diclofenaco += cant;
        totDiclofenaco += (cant * 350);
      }
      if(opc == 30) {
        cerr << "Digite la cantidad Ibuprofeno: ";
        cin >> cant;
        ibuprofeno += cant;
        totIbuprofeno += (cant * 500);
      }
    }
    if(opc == 2) {
      opc = submenu2();
      if(opc == 40) {
        cerr << "Digite la cantidad Zidovudina: ";
        cin >> cant;
        zidovudina += cant;
        totZidovudina += (cant * 1000000);
      }
      if(opc == 50) {
        cerr << "Digite la cantidad Carmustina: ";
        cin >> cant;
        carmustina += cant;
        totCarmustina += (cant * 500000);
      }
    }
  }
  totCompra = totAcetaminofen + totDiclofenaco + totIbuprofeno + totZidovudina + totCarmustina;
  iva = totCompra * 0.19;
  cout << "Nombre Cliente: " << cliente << endl;
  cout << "Cédula: " << cedula << endl;
  cout << "Cantidad Vendida Acetaminofén: " << acetaminofen << endl;
  cout << "Cantidad Vendida Diclofenaco: " << diclofenaco << endl;
  cout << "Cantidad Vendida Ibuprofeno: " << ibuprofeno << endl;
  cout << "Cantidad Vendida Zidovudina: " << zidovudina << endl;
  cout << "Cantidad Vendida Carmustina: " << carmustina << endl;
  cout << "Subtotal: " << totCompra << endl;
  cout << "Iva: " << iva << endl;
  cout << "Total: " << totCompra + iva << endl;
}