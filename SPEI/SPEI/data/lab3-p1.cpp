#include <iostream>
using namespace std;

int subsidioTransporte(int s) {
  return s * 0.2;
}

int bonificacionServicios(int s) {
  return s * 0.1;
}

int funcionSalud(int s) {
  return s * 0.04;
}

int pension(int s) {
  return s * 0.04;
}

int retefuente(int s) {
  return s * 0.05;
}

int main() {
  int cant, salario, totSalario = 0, strans = 0, bserv = 0, salud = 0, pens = 0, retef = 0;
  cerr << "Digite la cantidad de empleados: ";
  cin >> cant;
  for(int i=1; i <= cant; i++) {
    cerr << "Digite el salario del empleado " << i << ": ";
    cin >> salario;
    strans += subsidioTransporte(salario);
    bserv += bonificacionServicios(salario);
    salud += funcionSalud(salario);
    pens += pension(salario);
    retef += retefuente(salario);
    totSalario += salario;
  }
  cout << "Cantidad de empleados a pagar: " << cant << endl;
  cout << "Total a Pagar: " << (totSalario + strans + bserv)  << endl;
  cout << "Total Descuentos: " << (salud + pens + retef)  << endl;
  cout << "Neto a Pagar: " << (totSalario + strans + bserv - salud - pens - retef) << endl;
}