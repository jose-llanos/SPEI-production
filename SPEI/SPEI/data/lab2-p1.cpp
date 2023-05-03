/*
Nombre:Jose Miguel Llanos
Mail:jose.llanos@correounivalle.edu.co
*/

/*analisis
Entradas:
nombre : texto
peso : real
altura : real
Salidas:
nombre : texto
IMC : real
categoria : texto
Proceso:Calcular el IMC del paciente y con base en este determinar su categoria.
*/
/*Pseudocodigo
Inicio
   nombre    : cadena
   peso      : real
   altura    : real 
   IMC       : real
   categoria : texto
   // Entradas
   preguntar(nombre)
   preguntar(peso)
   preguntar(altura)
   // Proceso
   IMC = peso/(altura*altura)
   // Salidas
   si IMC<18.5 entonces
      categoria = "Infrapeso"
      mostrar(nombre)
      mostrar(IMC)
      mostrar(categoria)
   si IMC>=18.5 y IMC<25.0 entonces
      categoria = "Normal"
      mostrar(nombre)
      mostrar(IMC)
      mostrar(categoria)
   si IMC>=25.0 entonces
      categoria = "Sobrepeso"
      mostrar(nombre)
      mostrar(IMC)
      mostrar(categoria)    
Fin
*/
/*Pruebas de escritorio
Nombre         Peso  Altura  PACIENTE       IMC      Categoria
Alex Valencia  68.3  1.72    Alex Valencia  23.0868  Normal
María Caicedo  55.1  1.62    María Caicedo  20.9953  Normal
Juan Morales   90.1  1.71    Juan Morales   30.8129  Sobrepeso
*/

//Código en C++
#include <iostream>
using namespace std;

int main() {
   //nombre, categoria : cadena
   string nombre, categoria;
   //peso, altura, IMC : real
   float peso, altura, IMC;
   //preguntar(nombre)
   cerr << "Digite el nombre: ";
   getline(cin, nombre);
   //preguntar(peso)
   cerr << "Digite el peso: ";
   cin >> peso;
   //preguntar(altura)
   cerr << "Digite la altura: ";
   cin >> altura;
   // IMC = peso/(altura*altura)
   IMC = peso / (altura * altura);
   if(IMC < 18.5){
     categoria = "Infrapeso";
     cout << "PACIENTE: " << nombre << endl;
     cout << "IMC: " << IMC << endl;
     cout << "Categoria: " << categoria << endl;
   }
   if(IMC >= 18.5 && IMC < 25.0){
     categoria = "Normal";
     cout << "PACIENTE: " << nombre << endl;
     cout << "IMC: " << IMC << endl;
     cout << "Categoria: " << categoria << endl;
   }
   if(IMC >= 25.0){
     categoria = "Sobrepeso";
     cout << "PACIENTE: " << nombre << endl;
     cout << "IMC: " << IMC << endl;
     cout << "Categoria: " << categoria << endl;
   }
}