# Azoe Integration v2.0.0
Un editor/creador de árboles de diálogo para el proyecto AzoeEngine.
Y ahora también un editor de árboles de comportamiento!


**Acciones de teclado**
 - "s": crear un nodo sobre el canvas.
 - "c": crea una conexión entre dos nodos seleccionados. 
 - "shft+c": elimina la conexión entre los nodos seleccionados.
 - "a": crea un punto intermedio entre dos elementos seleccionados adyacentes.
 - "d": con un locutor (en modo diálogo) o un tipo estructural (en modo de comportamiento) y  nodos seleccionados, establece ese locutor o tipo para esos nodos.
 - "suprimir": borra todos los objetos seleccionados. Reemplaza colores en el panel de locutores (modo diálogo).
 - "enter": crea un archivo "output.json" con la estructura del árbol (modo diálogo).
 - "F1": recarga el archivo input.json y borra los nodos en exceso (modo diálogo).
 - "F2": crea un nuevo color para representar un locutor (modo diálogo).
 - "F3": habilita la edición del texto del nodo, o (en modo diálogo) el nombre del locutor seleccionado.
 - "F4": alterna entre el modo de edición de diálogos y el modo de edición de árboles de comportamiento.
 - "F5": levanta la resticción, permitiendo que se añadan nuevos por encima del limite del diálogo.
 - "escape": cierra el programa.

**Acciones con el mouse**
- Click (sobre un objeto): Selecciona. Otros objetos se deseleccionan.
- Click (sobre el canvas): deselecciona todos los objetos.
- Ctrl+click: Selecciona otros objetos manteniendo la selección.
- Ctrl+Click (sobre el canvas) y arrastrar: desplaza a todos los nodos simultáneamente.
- Click (sobre un objeto) y arrastrar: mueve un objeto seleccionado.
- Click (sobre el canvas) y arrastrar: mantener para crear una caja de selección.
- Shift+click y arrastrar: crea una caja de selección sin deseleccionar los demás objetos.
