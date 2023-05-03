/*
1:Cabecera del archivo

Nombre: Julian Alexander Alvarez Payares
Correo: alvarez.julian@correounivalle.edu.co
Número de laboratorio: 1
*/

/*
2:Análisis del problema

Descripción Funcionalidad:
En un almacén que se dedica a la venta de teléfonos inteligentes se quiere
conocer el IVA, el costo, y la ganancia neta de sus productos. Estos tres
rubros corresponden al 19%, 61%, y 20%, respectivamente, y se calculan sobre
el valor del producto. Usted debe desarrollar un programa que permita calcular
los valores requeridos por el almacén. El programa debe inicialmente solicitar
dos valores, el nombre y el precio del producto. Luego, se muestran cuatro
datos, el nombre, el IVA, el costo, y la ganancia neta. A continuación se
muestra un ejemplo de la entrada de datos:

Entradas:
Samsung Galaxy A31
729900

Salidas:

Producto: Samsung Galaxy A31
IVA: 138681
Costo: 445239
Ganancia Neta: 145980

Proceso: Debo crear 2 variables, una de tipo string y la otra de tipo entero,
para recibir el nombre del producto y el precio del mismo, despues con el valor
del precio debo crear 3 variables de tipo entero para calcular el precio del
iva que es del 19%, despues calcular el costo que es el 61% y por ultimo la
ganancia que es del 20%, ultimamente
muestro los datos.

*/

/*
3: Algoritmo en pseudocódigo

Inicio
  nombreProducto: cadena;
  precioProducto, IVA, costo, gananciaNeta: entero;

  preguntar(nombreProducto)
  preguntar(precio)

  IVA = (precioProducto * 19)/100
  costo = (precioProducto * 61)/100
  gananciaNeta = (precioProducto * 20)/100

  mostrar(nombreProducto)
  mostrar(IVA)
  mostrar(costo)
  mostrar(gananciaNeta)

Fin

*/

/*
4: Pruebas de escritorio

Prueba 1:
nombreProducto = Samsung Galaxy A31
precioProducto = 729900


*/

/*
5: Algoritmo en C++, por ejemplo:
*/

#include <iostream>
#include <string.h>
using namespace std;
// Inicio
int main() {
  // Datos de entradas
  string nombreProducto;
  int precioProducto;
  float IVA, costo, gananciaNeta;
  // Preguntar el nombre del producto
  cerr << "Digite el nombre del producto: ";

  getline(std::cin, nombreProducto);

  // Preguntar el precio del producto.
  cerr << "Digite el precio del producto: ";
  cin >> precioProducto;



  // Proceso

  IVA = (precioProducto * 19)/100;
  costo = (precioProducto * 61)/100;
  gananciaNeta = (precioProducto * 20)/100;

  // Datos de salidas
  cout << "Producto: " << nombreProducto << endl;
  cout << "IVA: " << IVA << endl;
  cout << "Costo: " << costo << endl;
  cout << "Ganancia Neta: " << gananciaNeta << endl;
  
  // Fin
}
