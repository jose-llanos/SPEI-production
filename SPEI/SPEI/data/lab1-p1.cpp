/*
1:Cabecera del archivo

Nombre: Julian Alexander Alvarez Payares
Correo: alvarez.julian@correounivalle.edu.co
*/

/*
2:Análisis del problema

Descripción Funcionalidad:
En una cinemateca se lleva el registro de las películas que se exhiben.
De cada película se solicitan cinco valores, estos son: el título, el
país de origen, el género, la duración (en minutos) y el año de estreno.
Usted debe desarrollar un programa que permita registrar la información
de las películas. A continuación se muestra un ejemplo de la entrada de
datos.

Entradas:
La escafandra y la mariposa
Francia
Drama
112
2007

Salidas:
DATOS DE LA PELÍCULA
TÍTULO: La escafandra y la mariposa
PAÍS DE ORIGEN: Francia
GÉNERO: Drama
DURACIÓN: 112 minutos
AÑO DE ESTRENO: 2007

Proceso: Debo crear 5 variables de tipo string,
el nombre de cada variable es nombrePelicula, paisOrigen, genero, duración y
fechaEstreno, respectivamente. Despues, debo agregar unos cout para imprimir el
mensaje en pantalla como es requerido.
*/

/*
3: Algoritmo en pseudocódigo

Inicio
  nombrePelicula, paisOrigen, genero: cadena
  duración y fechaEstreno: entero
  preguntar(nombrePelicula)
  preguntar(paisOrigen)
  preguntar(genero)
  preguntar(duración)
  preguntar(fechaEstreno)
  mostrar(nombrePelicula)
  mostrar(paisOrigen)
  mostrar(genero)
  mostrar(duración)
  mostrar(fechaEstreno)
Fin

*/

/*
4: Pruebas de escritorio

Prueba 1:
nombrePelicula = La escafandra y la mariposa
paisOrigen = Francia
genero = Drama
duración = 112
fechaEstreno = 2007
*/

//5: Algoritmo en C++, por ejemplo:
#include <iostream>
#include <string.h>
using namespace std;
// Inicio
int main() {
  // Datos de entradas
  string nombrePelicula, paisOrigen, genero,duracion, fechaEstreno;
  // Preguntar el título de la película
  cerr << "Digite el título de la película: ";
  //cin >> nombrePelicula;
  getline(std::cin, nombrePelicula);

  // Preguntar el país de origen
  cerr << "Digite el país de origen: ";
  cin >> paisOrigen;
  // Preguntar el género
  cerr << "Digite el género: ";
  cin >> genero;
  // Preguntar la duración
  cerr << "Digite la duración en minutos: ";
  cin >> duracion;
  // Preguntar el año de estreno
  cerr << "Digite el año de estreno: ";
  cin >> fechaEstreno;

  // Proceso

  // Datos de salidas
  cout << "DATOS DE LA PELÍCULA" << endl;
  cout << "TÍTULO: " << nombrePelicula << endl;
  cout << "PAÍS DE ORIGEN: " << paisOrigen << endl;
  cout << "GÉNERO: " << genero << endl;
  cout << "DURACIÓN: " << duracion << " minutos"<<endl;
  cout << "AÑO DE ESTRENO: " << fechaEstreno << endl;
// Fin
}