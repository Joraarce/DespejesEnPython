# DespejesEnPython
Despejes en Python
En esta página se va a describir como poner a correr Newton, y algunas de las características más importantes para poner a correrlo.

**¿Qué es Newton?**

La idea es que Newton sea una app educativa para dispositivos móviles para ayudar a estudiantes de secundaria a aprender a realizar despejes matemáticos, hacer conversiones de unidades, aplicar la segunda ley de Newton, y otras habilidades que se requieren para estudiar Física (ojo que no es una calculadora, o un programa que resuelva por sí solo problemas de Física). El nombre de la aplicación está totalmente abierto a discusión por otro más llamativo. La idea es hacer que la app se llegue a encontrar disponible para dispositivos Android y Apple.

Normalmente, las aplicaciones Android se escriben en lenguaje Java y las aplicaciones de Apple se escriben en lenguaje SWIFT, pero Newton está escrito en lenguaje **Python**. La razón principal de que Newton esté escrito en Python se debe a que hace uso de una librería llamada **SimPy**, que entre otras cosas, funciona como un **COMPUTER ALGEBRA SYSTEM (CAS)**. Es decir, permite hacer operaciones y manipulaciones algebraicas, como sumar polinomios, sacar potencias y raíces, funciones trigonométricas, y muchas otras más. Hasta el momento, no tengo conocimientos de que haya librerías con funciones semejantes en Java o en SWIFT, por lo tanto no he podido escribir la aplicación en esos lenguajes.

Newton también hace uso de la librería **Kivy**, (https://kivy.org) con la que se construye las GUI. En teoría, Kivy permite la creación de aplicaciones Android e iOS. La librería **Matplotlib** es necesaria para manejar algunas imágenes y generar figuras con Látex.

**Ejecutar Newton**

Para editar Newton recomiendo usar el editor PyCharm, que se descarga gratuitamente de la siguiente dirección:

https://www.jetbrains.com/es-es/pycharm/download/#section=mac

Al momento de descargar, deben verificar que se escoja la versión COMMUNITY que es gratuita.

Luego de instalar el PyCharm, deben descargar la carpeta de Newton en su computadora en un directorio conocido. El directorio debe tener el archivo main.py y una carpeta llamada Resources que es donde se guardan las imágenes, los archivos de efectos de sonido, e incluso se piensa guardar el archivo .ico que se usa para generar el ícono (que aún está pendiente). Deben abrir con Pycharm el archivo main.py y configurar los ajustes de la siguiente manera:

En Windows y Linux, se debe ingresar al menú File > Settings (En Mac, se debe ir al menú PyCharm > Preferences). A partir de ahí, se debe ir a Project > Python interpreter para agregar las librerías requeridas.

<img width="1440" alt="Screen_Shot_2022-08-27_at_22 17 54-2" src="https://user-images.githubusercontent.com/65260605/189506956-dcf556bf-9ee8-421d-b52a-f7137eb02c56.png">


Se debe hacer click en el botón + buscar el nombre de las librerías requeridas y hacer click en el botón de Install package.

Para el proyecto Newton, en principio será necesario agregar Kivy, Matplotlib, y SymPy.

Luego, para correr el programa deberá hacer click en el botón run.


<img width="1440" alt="Screen_Shot_2022-08-27_at_22 23 45" src="https://user-images.githubusercontent.com/65260605/189506975-dd9881d7-0bae-4fcb-a541-aab6d3a318ca.png">

A la hora de ejecutar, debería salir el menú de inicio:

<img width="1440" alt="Screen_Shot_2022-08-27_at_22 24 51" src="https://user-images.githubusercontent.com/65260605/189506982-082038a5-bfc4-4e48-97f4-d7f04d25acfc.png">


Al hacer click en el botón niveles se puede acceder a las funcionalidades del programa. Note que deberían aparecer efectos de sonido anta algunas entradas.

**Funciones**
| Descripción | Figuras |
|-------------|---------|
| **Infografía (TIPS)**. Este recurso es una infografía donde se hace una descripción sobre el tema a estudiar en una unidad. En un futuro se puede hacer más interactivo. | <img width="408" alt="Screen_Shot_2022-08-27_at_22 37 29" src="https://user-images.githubusercontent.com/65260605/189506989-3e1b61cb-f26f-44da-8e84-c0d0a7f3af6a.png">|
| **Conversiones**. El usuario debe colocar correctamente los factores de conversión para resolver el reto que se le propone. |<img width="394" alt="Screen_Shot_2022-08-27_at_22 41 01" src="https://user-images.githubusercontent.com/65260605/189506993-c85cc7e2-0f86-48b1-9807-61db54c754f4.png">|
| **Despejes**. Al usuario se le presenta una ecuación (por lo general, una ecuación relacionada con la Física) y debe despejar la variable que se le indica. | <img width="391" alt="Screen_Shot_2022-08-27_at_22 42 42" src="https://user-images.githubusercontent.com/65260605/189507006-1fc4b7f9-6e72-47dc-9aa6-ed7e354031cf.png">|
| **Dinámica**. Al usuario se le presenta un DCL, y debe construir correctamente la sumatoria de fuerzas usando los términos matemáticos que se le presenta. | <img width="394" alt="Screen_Shot_2022-08-27_at_22 45 30" src="https://user-images.githubusercontent.com/65260605/189507035-059f918d-5503-4fc1-893d-ea993dafb6a2.png">|

**Dificultades actuales**

El programa tiene efectivamente algunos niveles que deben ser terminados, así como se deben incluir más infografías y otros materiales instructivos.

Por el momento no ha sido posible crear un archivo ejecutable de Newton, solo ha sido posible correrlo desde PyCharm. En teoría, para crear una versión ejecutable es necesario seguir las instrucciones que se encuentran en las siguientes páginas:

https://kivy.org/doc/stable/guide/packaging-ios.html

No he podido hacer la prueba de correr el archivo APK en un dispositivo Android ni tampoco en un simulador, pues parece que es un archivo pesado.

A la hora de intentar crear el ejecutable para iOS, el programa se queja de que no puede cargar la librería Matplotlib. Aparentemente, es necesario incluir un "recipe" tal y como se explica en este enlace:

https://python-for-android.readthedocs.io/en/latest/recipes/

Por el momento, no he tendido éxito con eso.

**Modelo de negocio**

Se ha conversado sobre la posibilidad de que Newton utilice el modelo FREEMIUM. Esto debe discutirse con mayor detalle.
