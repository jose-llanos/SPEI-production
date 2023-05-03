/*
Nombre: Jose Llanos
Mail: jose.llanos@correounivalle.edu.co

*/
/*analisis
Entradas:
x : entero
Salidas:
Fx : entero
Proceso:Calcular el valor de f(x) dado un valor x.
*/
/*Pseudocodigo
Inicio CalculcarFx(x)
   Fx : entero
    si (x<=0)
        Fx=8*(x*x)-6;
        mostrar (“f(”x") = "Fx)
   si (x>0)
      Fx=3*(x)+5;
        mostrar (“f(”x") = "Fx)
   retornar(Fx)
Fin
Inicio main()
   x : entero
   fx :  entero
   preguntar (x)
   si x<=0 entonces
      fx = 8*(x*x)-6
      mostrar(fx)
   si (x>0)
      fx =3*(x)+5
      mostrar(fx)
Fin
*/
/*Pruebas de escritorio
x     f(x)
10    35
-7    386
0     -6
*/
//Código en C++
#include <iostream>
using namespace std;

int main(){
  int x, fx;
  
  cerr << "Digite el valor de x: ";
  cin >> x;

  if(x<=0){
    fx = 8*(x*x)-6;
    cout << "f(x) = " << fx<<endl;
  }
  if(x>0){
   fx = 3*(x)+5;
   cout << "f(x) = " << fx<<endl;
    }
}
