# Documento de Referencia Maestro: Creación y Progresión de Personajes en D&D 5.5 (Revisión 2024)

Este documento contiene las reglas estructurales y de progresión mecánicas de la edición 2024 de Dungeons & Dragons. Está diseñado para servir como "Base de Conocimiento" para agentes de Inteligencia Artificial que deban procesar, validar o gestionar hojas de personaje en aplicaciones de software.

---

## PARTE 1: CREACIÓN DE PERSONAJE (NIVEL 1)

El proceso de creación sigue un flujo secuencial donde las decisiones se acumulan para calcular los atributos finales del personaje.

### 1. Seleccionar la Clase (Class)
La clase define el armazón mecánico del personaje. A nivel 1, la clase determina:
* **Dado de Golpe (Hit Die):** Define los Puntos de Golpe (HP). Puede ser d6 (magos/hechiceros), d8 (bardos, clérigos, pícaros), d10 (guerreros, paladines, exploradores) o d12 (bárbaros).
* **Puntos de Golpe Base (Nivel 1):** El personaje recibe el valor máximo del dado de golpe + su Modificador de Constitución.
* **Competencias en Salvaciones (Saving Throws):** Cada clase otorga competencia en dos tiradas de salvación específicas.
* **Competencias en Equipo:** Define qué armaduras (Ligeras, Medias, Pesadas, Escudos) y qué armas (Simples, Marciales) puede usar sin penalización.
* **Competencias en Habilidades (Skills):** Otorga un número específico de habilidades a elegir de una lista cerrada (por ejemplo, el Bardo elige 3 habilidades de cualquier tipo, mientras que el Clérigo elige de una lista más restringida relacionada con religión o persuasión).
* **Rasgos de Clase de Nivel 1:** Habilidades específicas (ej. Lanzamiento de Conjuros para clases mágicas, Furia para bárbaros).

### 2. Seleccionar el Trasfondo (Background) - *¡Cambio Crítico en 2024!*
El trasfondo ahora tiene un impacto fundamental en los atributos mecánicos, reemplazando a la raza/especie en este aspecto:
* **Mejora de Puntuación de Característica (ASI):** El trasfondo proporciona 3 características asociadas. El personaje puede elegir distribuir un **+2 a una característica y +1 a otra**, o bien **+1 a las tres características**.
* **Dote de Origen (Origin Feat):** Otorga de forma gratuita una dote específica del catálogo de "Dotes de Origen" (ej. *Iniciado en la Magia*, *Sanador*, *Alerta*).
* **Competencias Fijas:** Otorga competencia en exactamente 2 habilidades específicas y 1 tipo de herramienta.
* **Equipo Inicial Adicional:** Proporciona un pequeño paquete de equipo y oro (50 po).

### 3. Seleccionar la Especie (Species)
Anteriormente llamadas razas. Ya no otorgan bonificadores a las características. Otorgan:
* **Velocidad Base:** Típicamente 30 pies.
* **Tamaño:** Pequeño o Mediano.
* **Rasgos Innatos:** Habilidades como *Visión en la Oscuridad* (Darkvision), linajes feéricos, resistencias a daños (ej. resistencia al fuego para Tiflin), o magia heredada.

### 4. Determinar Puntuaciones de Característica (Ability Scores)
Se definen las 6 puntuaciones base (Fuerza, Destreza, Constitución, Inteligencia, Sabiduría, Carisma).
* **Generación Base:** Se utiliza la Matriz Estándar (15, 14, 13, 12, 10, 8), Compra de Puntos (Point Buy) o Tirada de Dados.
* **Suma del Trasfondo:** A las puntuaciones base se les suman los bonificadores (+2/+1 o +1/+1/+1) obtenidos en el paso 2.
* **Cálculo de Modificadores:** El valor real que se usa en las fórmulas del juego es el modificador.
    * `Fórmula: Modificador = REDONDEAR.MENOS((Puntuación - 10) / 2)`
    * Ejemplo: Una puntuación de 16 da un modificador de +3. Una puntuación de 8 da un modificador de -1.

### 5. Equipo Inicial
El personaje elige cómo equiparse:
* **Paquete Inicial de Clase y Trasfondo:** Toma el equipo predeterminado indicado por su clase y trasfondo.
* **Comprar Equipo (Oro Inicial):** Recibe una cantidad fija de oro (dependiendo de la clase) y compra ítem por ítem.

### 6. Cálculos Finales Derivados
Con los datos anteriores, se determinan los valores de la hoja:
* **Bono de Competencia (Proficiency Bonus - PB):** +2 a Nivel 1.
* **Iniciativa:** Igual al Modificador de Destreza.
* **Clase de Armadura (CA):**
    * *Sin Armadura:* 10 + Modificador de Destreza.
    * *Armadura Ligera:* Valor Base de la armadura + Modificador de Destreza completo.
    * *Armadura Media:* Valor Base de la armadura + Modificador de Destreza (máximo +2).
    * *Armadura Pesada:* Valor Base de la armadura (Ignora el Modificador de Destreza, incluso si es negativo).
    * *Escudo:* Suma +2 a la CA total.
* **Ataques:** Ataque a Melé usa Fuerza (o Destreza si el arma tiene la propiedad 'Sutil/Finesse'). Ataques a Distancia usan Destreza. Fórmulas:
    * `Bono de Ataque = Modificador de Característica + Bono de Competencia`
    * `Daño = Dado del Arma + Modificador de Característica`
* **Magia (CD y Ataque de Conjuro):**
    * `Tirada de Ataque de Conjuro = Modificador de Característica Lanzadora + Bono de Competencia`
    * `CD de Salvación de Conjuros = 8 + Modificador de Característica Lanzadora + Bono de Competencia`

---

## PARTE 2: PROGRESIÓN Y SUBIDA DE NIVEL (LEVEL UP)

Cuando un personaje gana suficiente experiencia (o por hitos/milestones), sube de nivel. El proceso de subida de nivel implica actualizar los siguientes bloques:

### 1. Aumento de Puntos de Golpe (Obligatorio en cada nivel)
El personaje gana más salud permanente.
* `Nuevos HP Máximos = HP Máximos Anteriores + Tirada del Dado de Golpe (o el Promedio fijo) + Modificador de Constitución`
* *(Nota algorítmica: El promedio fijo del dado es `(Caras / 2) + 1`. Ejemplo para el clérigo o bardo (d8): el promedio es 5. Para un guerrero (d10): 6).*

### 2. Progresión del Bono de Competencia (Automático por Nivel Total)
El Bono de Competencia escala con el *Nivel Total* del personaje (crucial si el personaje es multiclase):
* Niveles 1-4: +2
* Niveles 5-8: +3
* Niveles 9-12: +4
* Niveles 13-16: +5
* Niveles 17-20: +6
*(Cualquier habilidad, salvación, CD de conjuro o ataque donde el personaje sea competente debe recalcularse al alcanzar estos umbrales).*

### 3. Selección de Subclase - *¡Cambio Crítico en 2024!*
**Absolutamente todas las clases eligen su subclase al Nivel 3.**
* Si el personaje sube del Nivel 2 al Nivel 3, se debe desplegar el menú de selección de subclase (ej. Colegio del Glamour para el Bardo o un Dominio específico para el Clérigo).
* La subclase otorga rasgos adicionales de forma inmediata y continuará otorgando rasgos en niveles específicos posteriores detallados por la clase.

### 4. Dotes y Mejoras de Atributos (ASI)
En los niveles **4, 8, 12, 16 y 19** de una clase específica (el guerrero y el pícaro tienen niveles adicionales), el personaje recibe una Dote.
* En las reglas 2024, la "Mejora de Puntuación de Característica" (Ability Score Improvement) es mecánicamente una Dote General.
* El jugador puede elegir subir sus atributos (+2 a uno o +1 a dos) **O** elegir una Dote General (que a menudo incluye un +1 a una característica específica, además de un beneficio mecánico).
* *Lógica de Retroactividad de Constitución:* Si un jugador aumenta su Modificador de Constitución en este paso, la aplicación **debe** recalcular los Puntos de Golpe Máximos sumando retroactivamente +1 HP por cada nivel que tenga el personaje.

### 5. Dotes Épicas (Epic Boons)
En el **Nivel 19**, los personajes obtienen acceso a una categoría especial de dotes llamadas Dotes Épicas (Epic Boons), que representan poderes casi divinos reservados para el final de la progresión.

### 6. Actualización de Lanzamiento de Conjuros
Si el personaje pertenece a una clase lanzadora de conjuros (Bardo, Clérigo, Mago, etc.):
* **Nuevos Espacios de Conjuro:** Se actualiza la cantidad de "Spell Slots" según la tabla de la clase (ej. ganar acceso a conjuros de nivel 2 al llegar a nivel 3 de clase completa).
* **Aprender/Preparar Nuevos Conjuros:** El jugador puede seleccionar nuevos conjuros de la lista de su clase, respetando el nivel de los espacios de conjuro que posee.
* **Sustitución de Conjuros:** Cada vez que el personaje gana un nivel en su clase mágica, tiene derecho a "olvidar" un conjuro que conocía previamente y cambiarlo por otro de la misma lista de clase, siempre que tenga espacios válidos para el nuevo nivel.
