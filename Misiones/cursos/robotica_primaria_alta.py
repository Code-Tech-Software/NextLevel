"""Robótica · Primaria Alta: Arduino con el kit Rexqualis R3 (una placa compatible con Arduino UNO).

El kit llega una semana después de empezar, así que el primer mundo (dos días de clase) se trabaja sin kit:
actividades desconectadas y Tinkercad Circuits. Todas las prácticas traen su código completo y comentado,
con las conexiones en la descripción, y terminan con un reto para que el alumno modifique el programa.
"""
from Misiones.cursos import mision

TINKERCAD = 'https://www.tinkercad.com/joinclass/UCXTYWZIG'


def practica(nombre, descripcion, codigo, xp=70, monedas=20, **extra):
    return mision(nombre, 'arduino', descripcion, xp, monedas, codigo=codigo, **extra)


def jefe(nombre, descripcion, codigo=None, xp=150, monedas=50, tipo='arduino', **extra):
    return mision(nombre, tipo, descripcion, xp, monedas, jefe=True, codigo=codigo, **extra)


TECLADO_4X4 = r'''
const byte FILAS = 4, COLUMNAS = 4;
char teclas[FILAS][COLUMNAS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};'''

NUMEROS_7SEG = r'''
// Qué segmentos se encienden en cada número (a b c d e f g)
const byte NUMEROS[10][7] = {
  {1,1,1,1,1,1,0},  // 0
  {0,1,1,0,0,0,0},  // 1
  {1,1,0,1,1,0,1},  // 2
  {1,1,1,1,0,0,1},  // 3
  {0,1,1,0,0,1,1},  // 4
  {1,0,1,1,0,1,1},  // 5
  {1,0,1,1,1,1,1},  // 6
  {1,1,1,0,0,0,0},  // 7
  {1,1,1,1,1,1,1},  // 8
  {1,1,1,1,0,1,1}   // 9
};'''

# ========================
# CÓDIGO DE LAS PRÁCTICAS
# ========================
COD_PARPADEO = r'''
// Hola, mundo: el LED que parpadea
// Pin 8 -> resistencia de 220 ohms -> pata larga del LED · pata corta -> GND

const int LED = 8;

void setup() {
  pinMode(LED, OUTPUT);      // el pin 8 será una salida
}

void loop() {
  digitalWrite(LED, HIGH);   // enciende: el pin da 5 V
  delay(500);                // espera medio segundo (500 milisegundos)
  digitalWrite(LED, LOW);    // apaga: el pin da 0 V
  delay(500);
}
'''

COD_SEMAFORO = r'''
// Semáforo: verde en el pin 2, amarillo en el 3 y rojo en el 4
// Cada LED: pin -> resistencia de 220 ohms -> pata larga · pata corta -> GND

const int VERDE = 2;
const int AMARILLO = 3;
const int ROJO = 4;

void setup() {
  pinMode(VERDE, OUTPUT);
  pinMode(AMARILLO, OUTPUT);
  pinMode(ROJO, OUTPUT);
}

void loop() {
  // Siga
  digitalWrite(VERDE, HIGH);
  delay(4000);
  digitalWrite(VERDE, LOW);

  // Precaución: el amarillo parpadea 3 veces
  for (int i = 0; i < 3; i++) {
    digitalWrite(AMARILLO, HIGH);
    delay(400);
    digitalWrite(AMARILLO, LOW);
    delay(400);
  }

  // Alto
  digitalWrite(ROJO, HIGH);
  delay(4000);
  digitalWrite(ROJO, LOW);
}
'''

COD_BOTON = r'''
// Botón mágico: cada vez que lo presionas, el LED cambia (encendido / apagado)
// Botón: una pata al pin 2 y la pata contraria (en diagonal) a GND
// LED: pin 8 -> 220 ohms -> LED -> GND

const int BOTON = 2;
const int LED = 8;

bool encendido = false;
bool antes = HIGH;          // con INPUT_PULLUP, el botón suelto lee HIGH

void setup() {
  pinMode(BOTON, INPUT_PULLUP);   // usa la resistencia que el Arduino trae por dentro
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  bool ahora = digitalRead(BOTON);
  if (antes == HIGH && ahora == LOW) {   // justo en el momento en que lo presionas
    encendido = !encendido;              // ! significa "lo contrario"
    digitalWrite(LED, encendido);
    Serial.println(encendido ? "LED encendido" : "LED apagado");
    delay(50);                           // evita los "rebotes" del botón
  }
  antes = ahora;
}
'''

COD_DIMMER = r'''
// Dimmer: el potenciómetro controla el brillo del LED
// Potenciómetro: patas de los lados a 5V y GND · pata de en medio a A0
// LED: pin 9 (tiene el símbolo ~, sirve para PWM) -> 220 ohms -> LED -> GND

const int POT = A0;
const int LED = 9;

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(POT);                // de 0 a 1023
  int brillo = map(lectura, 0, 1023, 0, 255);   // lo pasamos a la escala de 0 a 255
  analogWrite(LED, brillo);                     // PWM: brillo variable

  Serial.print("Potenciometro: ");
  Serial.print(lectura);
  Serial.print("   Brillo: ");
  Serial.println(brillo);
  delay(100);
}
'''

COD_MELODIA = r'''
// Melodía: "Estrellita, ¿dónde estás?"
// Buzzer pasivo (en Tinkercad se llama Piezo): + al pin 8 · - a GND

const int BUZZER = 8;

// Notas musicales (frecuencia en Hz)
const int NOTA_DO = 262, NOTA_RE = 294, NOTA_MI = 330, NOTA_FA = 349, NOTA_SOL = 392, NOTA_LA = 440;

int melodia[] = { NOTA_DO, NOTA_DO, NOTA_SOL, NOTA_SOL, NOTA_LA, NOTA_LA, NOTA_SOL,
                  NOTA_FA, NOTA_FA, NOTA_MI, NOTA_MI, NOTA_RE, NOTA_RE, NOTA_DO };
int tiempos[] = { 1, 1, 1, 1, 1, 1, 2,
                  1, 1, 1, 1, 1, 1, 2 };   // 1 = negra, 2 = blanca (dura el doble)

void setup() {
  for (int i = 0; i < 14; i++) {
    int duracion = 400 * tiempos[i];
    tone(BUZZER, melodia[i], duracion * 0.9);   // toca la nota
    delay(duracion);                             // espera a que termine
  }
}

void loop() {
  // La canción suena una sola vez. Presiona RESET (o reinicia la simulación) para oírla otra vez.
}
'''

COD_CAJA_FUERTE = r'''
// Jefe: caja fuerte de 3 botones
// Botones (cada uno a GND) en los pines 2, 3 y 4
// LED verde: pin 8 · LED rojo: pin 9 (220 ohms cada uno) · Buzzer pasivo (Piezo): pin 10

const int BOTONES[] = {2, 3, 4};
const int VERDE = 8;
const int ROJO = 9;
const int BUZZER = 10;

const int CLAVE[] = {1, 3, 2, 1};   // la combinación secreta: botón 1, 3, 2 y 1
const int LARGO = 4;

int intento[LARGO];
int presionados = 0;

int leerBoton() {
  for (int i = 0; i < 3; i++) {
    if (digitalRead(BOTONES[i]) == LOW) {          // este botón está presionado
      tone(BUZZER, 600 + i * 200, 80);             // un "bip" diferente para cada botón
      while (digitalRead(BOTONES[i]) == LOW) {}    // espera a que lo sueltes
      delay(50);
      return i + 1;                                // regresa 1, 2 o 3
    }
  }
  return 0;                                        // no hay botón presionado
}

void setup() {
  for (int i = 0; i < 3; i++) pinMode(BOTONES[i], INPUT_PULLUP);
  pinMode(VERDE, OUTPUT);
  pinMode(ROJO, OUTPUT);
  Serial.begin(9600);
  Serial.println("Caja fuerte lista. Escribe la combinacion con los botones.");
}

void loop() {
  int boton = leerBoton();
  if (boton == 0) return;          // nadie presionó: vuelve a empezar el loop

  intento[presionados] = boton;
  presionados++;
  Serial.print("Boton ");
  Serial.println(boton);

  if (presionados == LARGO) {      // ya escribiste los 4: ¡a revisar!
    bool correcta = true;
    for (int i = 0; i < LARGO; i++) {
      if (intento[i] != CLAVE[i]) correcta = false;
    }

    if (correcta) {
      Serial.println("Caja abierta!");
      digitalWrite(VERDE, HIGH);
      tone(BUZZER, 523, 150); delay(180);
      tone(BUZZER, 659, 150); delay(180);
      tone(BUZZER, 784, 300); delay(1500);
      digitalWrite(VERDE, LOW);
    } else {
      Serial.println("Combinacion incorrecta");
      digitalWrite(ROJO, HIGH);
      tone(BUZZER, 150, 700); delay(1500);
      digitalWrite(ROJO, LOW);
    }
    presionados = 0;               // empieza un intento nuevo
  }
}
'''

COD_HOLA_PLACA = r'''
// ¡Hola, placa real! Usa el LED que la placa trae soldado (pin 13) y el monitor serial

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);   // LED_BUILTIN es el LED de la placa (pin 13)
  Serial.begin(9600);
  Serial.println("Hola! Soy tu placa Rexqualis R3 y ya te obedezco.");
}

void loop() {
  // Tres parpadeos rápidos y uno lento
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(150);
    digitalWrite(LED_BUILTIN, LOW);
    delay(150);
  }
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  Serial.println("Sigo vivo :)");
}
'''

COD_SEMAFORO_PEATONAL = r'''
// Semáforo con botón peatonal
// Autos: verde 2 · amarillo 3 · rojo 4   |   Peatón: verde 5 · rojo 6   (cada LED con 220 ohms)
// Botón: pin 7 a GND · Zumbador activo: + al pin 8, - a GND

const int A_VERDE = 2, A_AMARILLO = 3, A_ROJO = 4;
const int P_VERDE = 5, P_ROJO = 6;
const int BOTON = 7;
const int ZUMBADOR = 8;

void setup() {
  for (int pin = 2; pin <= 6; pin++) pinMode(pin, OUTPUT);
  pinMode(ZUMBADOR, OUTPUT);
  pinMode(BOTON, INPUT_PULLUP);
}

void loop() {
  // Normalmente los autos tienen verde y el peatón espera en rojo
  digitalWrite(A_VERDE, HIGH);
  digitalWrite(P_ROJO, HIGH);

  if (digitalRead(BOTON) == LOW) {   // ¡alguien quiere cruzar!
    delay(1000);
    digitalWrite(A_VERDE, LOW);
    digitalWrite(A_AMARILLO, HIGH);
    delay(2000);
    digitalWrite(A_AMARILLO, LOW);
    digitalWrite(A_ROJO, HIGH);

    // Cruce: verde para el peatón con pitidos (para personas que no ven)
    digitalWrite(P_ROJO, LOW);
    digitalWrite(P_VERDE, HIGH);
    for (int i = 0; i < 10; i++) {
      digitalWrite(ZUMBADOR, HIGH);
      delay(100);
      digitalWrite(ZUMBADOR, LOW);
      delay(400);
    }

    // El verde del peatón parpadea: ¡apúrate!
    for (int i = 0; i < 4; i++) {
      digitalWrite(P_VERDE, LOW);
      delay(250);
      digitalWrite(P_VERDE, HIGH);
      delay(250);
    }
    digitalWrite(P_VERDE, LOW);
    digitalWrite(P_ROJO, HIGH);
    delay(1000);
    digitalWrite(A_ROJO, LOW);
  }
}
'''

COD_LUZ_NOCTURNA = r'''
// Luz nocturna automática
// Fotoresistencia: una pata a 5V y la otra a A0 · resistencia de 10K de A0 a GND
// LED: pin 9 -> 220 ohms -> LED -> GND

const int LUZ = A0;
const int LED = 9;
int umbral = 400;   // ajústalo con los números que veas en el monitor serial

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int luz = analogRead(LUZ);   // mucha luz = número grande
  Serial.println(luz);

  if (luz < umbral) {
    digitalWrite(LED, HIGH);   // está oscuro: enciende
  } else {
    digitalWrite(LED, LOW);    // hay luz: apaga
  }
  delay(200);
}
'''

COD_MOCHILA = r'''
// Alarma anti-robo de mochila con el interruptor de inclinación
// Interruptor de inclinación: una pata al pin 2 y la otra a GND
// Zumbador activo: + al pin 8, - a GND · LED rojo: pin 9 -> 220 ohms -> GND

const int INCLINACION = 2;
const int ZUMBADOR = 8;
const int LED = 9;

void setup() {
  pinMode(INCLINACION, INPUT_PULLUP);
  pinMode(ZUMBADOR, OUTPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // De pie, la bolita de adentro cierra el circuito (LOW). Si lo inclinas, se abre (HIGH).
  if (digitalRead(INCLINACION) == HIGH) {
    Serial.println("Alguien movio la mochila!");
    for (int i = 0; i < 6; i++) {
      digitalWrite(ZUMBADOR, HIGH);
      digitalWrite(LED, HIGH);
      delay(250);
      digitalWrite(ZUMBADOR, LOW);
      digitalWrite(LED, LOW);
      delay(250);
    }
  }
}
'''

COD_LAMPARA = r'''
// Jefe: lámpara inteligente de 3 modos (apagada, automática y arcoíris)
// Botón: pin 2 a GND
// LED RGB (cátodo común: la pata más larga a GND): rojo 9 · verde 10 · azul 11 (220 ohms cada uno)
// Fotoresistencia: 5V -> fotoresistencia -> A0 -> 10K -> GND

const int BOTON = 2;
const int ROJO = 9, VERDE = 10, AZUL = 11;
const int LUZ = A0;

int modo = 0;          // 0 = apagada, 1 = automática, 2 = arcoíris
bool antes = HIGH;
int paso = 0;          // avance del arcoíris

void color(int r, int g, int b) {
  analogWrite(ROJO, r);
  analogWrite(VERDE, g);
  analogWrite(AZUL, b);
}

void setup() {
  pinMode(BOTON, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  bool ahora = digitalRead(BOTON);
  if (antes == HIGH && ahora == LOW) {
    modo = (modo + 1) % 3;     // 0 -> 1 -> 2 -> 0 ...
    Serial.print("Modo: ");
    Serial.println(modo);
    delay(50);
  }
  antes = ahora;

  if (modo == 0) {
    color(0, 0, 0);
  } else if (modo == 1) {
    // Automática: entre más oscuro, más brilla (luz blanca)
    int luz = analogRead(LUZ);
    int brillo = map(luz, 0, 1023, 255, 0);
    color(brillo, brillo, brillo);
  } else {
    // Arcoíris: rojo -> verde -> azul -> rojo, poquito a poco
    paso = (paso + 1) % 768;
    if (paso < 256)      color(255 - paso, paso, 0);
    else if (paso < 512) color(0, 511 - paso, paso - 256);
    else                 color(paso - 512, 0, 767 - paso);
    delay(5);
  }
}
'''

COD_PALETA_RGB = r'''
// Paleta de colores con el LED RGB
// LED RGB (cátodo común): pata más larga a GND · rojo 9 · verde 10 · azul 11 (220 ohms cada uno)
// Si tu LED es de ánodo común (pata larga a 5V), usa 255 - valor en cada color.

const int ROJO = 9, VERDE = 10, AZUL = 11;

void color(int r, int g, int b) {
  analogWrite(ROJO, r);
  analogWrite(VERDE, g);
  analogWrite(AZUL, b);
}

void mostrar(const char* nombre, int r, int g, int b) {
  Serial.println(nombre);
  color(r, g, b);
  delay(1500);
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  mostrar("Rojo", 255, 0, 0);
  mostrar("Verde", 0, 255, 0);
  mostrar("Azul", 0, 0, 255);
  mostrar("Amarillo", 255, 255, 0);
  mostrar("Cian", 0, 255, 255);
  mostrar("Magenta", 255, 0, 255);
  mostrar("Naranja", 255, 80, 0);
  mostrar("Morado", 120, 0, 255);
  mostrar("Blanco", 255, 255, 255);
}
'''

COD_MEZCLADOR = r'''
// Mezclador de colores: 2 potenciómetros y un botón
// Potenciómetro 1 (pata central) -> A0 controla el rojo · Potenciómetro 2 (pata central) -> A1 controla el azul
// Botón: pin 2 a GND enciende / apaga el verde
// LED RGB: rojo 9 · verde 10 · azul 11 (220 ohms cada uno), pata larga a GND

const int ROJO = 9, VERDE = 10, AZUL = 11;
const int BOTON = 2;
bool verde = false;
bool antes = HIGH;

void setup() {
  pinMode(BOTON, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  bool ahora = digitalRead(BOTON);
  if (antes == HIGH && ahora == LOW) {
    verde = !verde;
    delay(50);
  }
  antes = ahora;

  int r = map(analogRead(A0), 0, 1023, 0, 255);
  int b = map(analogRead(A1), 0, 1023, 0, 255);
  int g = verde ? 255 : 0;
  analogWrite(ROJO, r);
  analogWrite(VERDE, g);
  analogWrite(AZUL, b);

  Serial.print("R=");
  Serial.print(r);
  Serial.print("  G=");
  Serial.print(g);
  Serial.print("  B=");
  Serial.println(b);
  delay(100);
}
'''

COD_DADO = r'''
// Dado electrónico con display de 7 segmentos (1 dígito, cátodo común)
// Segmentos a, b, c, d, e, f, g -> pines 2, 3, 4, 5, 6, 7, 8 (cada uno con 220 ohms)
// Pin común del display (el 3 o el 8 del display) -> GND · Botón: pin 10 a GND

const int SEGMENTOS[] = {2, 3, 4, 5, 6, 7, 8};   // a b c d e f g
const int BOTON = 10;
const bool ANODO_COMUN = false;   // si tu display es de ánodo común (común a 5V), cámbialo a true
''' + NUMEROS_7SEG + r'''

void mostrar(int n) {
  for (int i = 0; i < 7; i++) {
    bool encendido = NUMEROS[n][i];
    digitalWrite(SEGMENTOS[i], ANODO_COMUN ? !encendido : encendido);
  }
}

void setup() {
  for (int i = 0; i < 7; i++) pinMode(SEGMENTOS[i], OUTPUT);
  pinMode(BOTON, INPUT_PULLUP);
  randomSeed(analogRead(A5));   // el "ruido" de un pin libre hace los números más aleatorios
  mostrar(0);
}

void loop() {
  if (digitalRead(BOTON) == LOW) {
    // Animación: el dado "rueda" cada vez más lento
    for (int i = 0; i < 12; i++) {
      mostrar(random(1, 7));
      delay(40 + i * 15);
    }
    mostrar(random(1, 7));                    // resultado final: de 1 a 6
    while (digitalRead(BOTON) == LOW) {}      // espera a que sueltes el botón
  }
}
'''

COD_74HC595 = r'''
// 8 LEDs con solo 3 cables gracias al chip 74HC595
// 74HC595: pin 14 (DS) -> Arduino 4 · pin 12 (ST_CP, candado) -> Arduino 5 · pin 11 (SH_CP, reloj) -> Arduino 6
//          pin 16 (VCC) y pin 10 (MR) -> 5V · pin 8 (GND) y pin 13 (OE) -> GND
//          Salidas Q0 (pin 15) y Q1 a Q7 (pines 1 a 7) -> 220 ohms -> LED -> GND

const int DATOS = 4;
const int CANDADO = 5;   // latch
const int RELOJ = 6;     // clock

void enviar(byte patron) {
  digitalWrite(CANDADO, LOW);
  shiftOut(DATOS, RELOJ, MSBFIRST, patron);   // manda los 8 bits, uno por uno
  digitalWrite(CANDADO, HIGH);                // los 8 LEDs cambian al mismo tiempo
}

void setup() {
  pinMode(DATOS, OUTPUT);
  pinMode(CANDADO, OUTPUT);
  pinMode(RELOJ, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // 1) El auto fantástico: una luz que va y viene
  for (int i = 0; i < 8; i++) { enviar(1 << i); delay(80); }
  for (int i = 6; i > 0; i--) { enviar(1 << i); delay(80); }

  // 2) Contador binario de 0 a 255 (míralo también en el monitor serial)
  for (int n = 0; n < 256; n++) {
    enviar(n);
    Serial.print(n);
    Serial.print(" = ");
    Serial.println(n, BIN);
    delay(150);
  }
}
'''

COD_MATRIZ_CARITAS = r'''
// Matriz de LEDs 8x8 con MAX7219: caritas y corazón
// Librería: LedControl (de Eberhard Fahle). Instálala en Herramientas > Administrar bibliotecas.
// Conexiones: VCC -> 5V · GND -> GND · DIN -> 12 · CLK -> 11 · CS -> 10
#include <LedControl.h>

LedControl matriz = LedControl(12, 11, 10, 1);   // DIN, CLK, CS, cuántas matrices

// Cada renglón es un byte: 1 = LED encendido, 0 = apagado
byte feliz[8] = {
  B00111100,
  B01000010,
  B10100101,
  B10000001,
  B10100101,
  B10011001,
  B01000010,
  B00111100
};

byte triste[8] = {
  B00111100,
  B01000010,
  B10100101,
  B10000001,
  B10011001,
  B10100101,
  B01000010,
  B00111100
};

byte corazon[8] = {
  B00000000,
  B01100110,
  B11111111,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000
};

void dibujar(byte figura[8]) {
  for (int fila = 0; fila < 8; fila++) {
    matriz.setRow(0, fila, figura[fila]);
  }
}

void setup() {
  matriz.shutdown(0, false);   // despierta la matriz
  matriz.setIntensity(0, 5);   // brillo de 0 a 15
  matriz.clearDisplay(0);
}

void loop() {
  dibujar(feliz);
  delay(1500);
  dibujar(triste);
  delay(1500);
  dibujar(corazon);
  delay(1500);
}
'''

COD_MATRIZ_ANIMACION = r'''
// Tu propia animación 8x8: el invasor espacial que baila
// Librería LedControl · Conexiones: VCC 5V · GND · DIN 12 · CLK 11 · CS 10
#include <LedControl.h>

LedControl matriz = LedControl(12, 11, 10, 1);

byte cuadro1[8] = {
  B00011000,
  B00111100,
  B01111110,
  B11011011,
  B11111111,
  B00100100,
  B01011010,
  B10100101
};

byte cuadro2[8] = {
  B00011000,
  B00111100,
  B01111110,
  B11011011,
  B11111111,
  B01011010,
  B10000001,
  B01000010
};

void dibujar(byte figura[8]) {
  for (int fila = 0; fila < 8; fila++) matriz.setRow(0, fila, figura[fila]);
}

void setup() {
  matriz.shutdown(0, false);
  matriz.setIntensity(0, 4);
  matriz.clearDisplay(0);
}

void loop() {
  dibujar(cuadro1);
  delay(400);
  dibujar(cuadro2);
  delay(400);
}
'''

COD_CUENTA_REGRESIVA = r'''
// Jefe: semáforo peatonal con cuenta regresiva en el display de 7 segmentos
// Display (cátodo común): a..g -> pines 2..8 (220 ohms cada uno), común -> GND
// LEDs (220 ohms): verde autos 9 · rojo autos 10 · verde peatón 11
// Botón: A0 a GND · Zumbador activo: pin 12

const int SEGMENTOS[] = {2, 3, 4, 5, 6, 7, 8};
const bool ANODO_COMUN = false;
const int AUTO_VERDE = 9, AUTO_ROJO = 10, PEATON = 11;
const int BOTON = A0;
const int ZUMBADOR = 12;
''' + NUMEROS_7SEG + r'''

void mostrar(int n) {
  for (int i = 0; i < 7; i++) {
    bool encendido = NUMEROS[n][i];
    digitalWrite(SEGMENTOS[i], ANODO_COMUN ? !encendido : encendido);
  }
}

void apagarDisplay() {
  for (int i = 0; i < 7; i++) digitalWrite(SEGMENTOS[i], ANODO_COMUN ? HIGH : LOW);
}

void setup() {
  for (int i = 0; i < 7; i++) pinMode(SEGMENTOS[i], OUTPUT);
  pinMode(AUTO_VERDE, OUTPUT);
  pinMode(AUTO_ROJO, OUTPUT);
  pinMode(PEATON, OUTPUT);
  pinMode(ZUMBADOR, OUTPUT);
  pinMode(BOTON, INPUT_PULLUP);   // los pines A0 a A5 también sirven como digitales
  apagarDisplay();
  digitalWrite(AUTO_VERDE, HIGH);
}

void loop() {
  if (digitalRead(BOTON) == LOW) {
    delay(1500);                     // los autos frenan
    digitalWrite(AUTO_VERDE, LOW);
    digitalWrite(AUTO_ROJO, HIGH);
    digitalWrite(PEATON, HIGH);

    for (int n = 9; n >= 0; n--) {   // cuenta regresiva para cruzar
      mostrar(n);
      if (n <= 3) {                  // los últimos segundos: pitido de aviso
        digitalWrite(ZUMBADOR, HIGH);
        delay(150);
        digitalWrite(ZUMBADOR, LOW);
        delay(850);
      } else {
        delay(1000);
      }
    }

    apagarDisplay();
    digitalWrite(PEATON, LOW);
    digitalWrite(AUTO_ROJO, LOW);
    digitalWrite(AUTO_VERDE, HIGH);
  }
}
'''

COD_TERMISTOR = r'''
// Termómetro de colores con el termistor
// 5V -> termistor -> A0 -> resistencia de 10K -> GND
// LED RGB (pata larga a GND): rojo 9 · verde 10 · azul 11 (220 ohms cada uno)

const int SENSOR = A0;
const int ROJO = 9, VERDE = 10, AZUL = 11;

float leerTemperatura() {
  int lectura = analogRead(SENSOR);
  float resistencia = 10000.0 * (1023.0 / lectura - 1.0);   // cuánto mide el termistor ahora
  float kelvin = 1.0 / (1.0 / 298.15 + log(resistencia / 10000.0) / 3950.0);
  return kelvin - 273.15;                                     // de Kelvin a grados Celsius
}

void color(int r, int g, int b) {
  analogWrite(ROJO, r);
  analogWrite(VERDE, g);
  analogWrite(AZUL, b);
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  float temperatura = leerTemperatura();
  Serial.print("Temperatura: ");
  Serial.print(temperatura, 1);
  Serial.println(" C");

  if (temperatura < 24) color(0, 0, 255);        // fresco: azul
  else if (temperatura < 28) color(0, 255, 0);   // agradable: verde
  else color(255, 0, 0);                          // calor: rojo
  delay(500);
}
'''

COD_DHT_LCD = r'''
// Estación del clima: sensor DHT11 + pantalla LCD 16x2
// Librerías: "DHT sensor library" de Adafruit (si te pregunta, instala también "Adafruit Unified Sensor")
//            y LiquidCrystal (ya viene con Arduino)
// DHT11: S -> pin 2 · + -> 5V · - -> GND
// LCD: RS -> 7 · E -> 8 · D4 -> 9 · D5 -> 10 · D6 -> 11 · D7 -> 12
//      VSS y RW -> GND · VDD -> 5V · V0 -> pata central de un potenciómetro (contraste)
//      A -> 220 ohms -> 5V · K -> GND
#include <DHT.h>
#include <LiquidCrystal.h>

DHT dht(2, DHT11);
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {
  dht.begin();
  lcd.begin(16, 2);
  lcd.print("Estacion clima");
  delay(2000);
}

void loop() {
  float humedad = dht.readHumidity();
  float temperatura = dht.readTemperature();

  lcd.clear();
  if (isnan(humedad) || isnan(temperatura)) {
    lcd.print("Error en DHT11");   // revisa los cables del sensor
  } else {
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.print(temperatura, 1);
    lcd.print((char)223);          // el símbolo de grados
    lcd.print("C");
    lcd.setCursor(0, 1);
    lcd.print("Humedad: ");
    lcd.print(humedad, 0);
    lcd.print("%");
  }
  delay(2000);   // el DHT11 solo puede medir cada 2 segundos
}
'''

COD_APLAUSOS = r'''
// Interruptor de aplausos: ¡aplaude y la luz cambia!
// Sensor de sonido: + -> 5V · G -> GND · AO -> A0 · DO -> pin 2
// LED: pin 9 -> 220 ohms -> LED -> GND

const int SONIDO_DIGITAL = 2;
const int SONIDO_ANALOGICO = A0;
const int LED = 9;
bool encendido = false;
unsigned long ultimoAplauso = 0;

void setup() {
  pinMode(SONIDO_DIGITAL, INPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  Serial.println(analogRead(SONIDO_ANALOGICO));   // ábrelo en Herramientas > Serial Plotter

  // millis() cuenta los milisegundos desde que encendió la placa: así ignoramos el eco del aplauso
  if (digitalRead(SONIDO_DIGITAL) == HIGH && millis() - ultimoAplauso > 400) {
    ultimoAplauso = millis();
    encendido = !encendido;
    digitalWrite(LED, encendido);
  }
  delay(5);
}
'''

COD_INUNDACION = r'''
// Alarma de inundación con el sensor de nivel de agua
// Sensor: S -> A0 · + -> pin 7 (lo encendemos solo al medir para que no se oxide) · - -> GND
// LEDs (220 ohms): verde 9 · amarillo 10 · rojo 11 · Zumbador activo: pin 8

const int SENSOR = A0;
const int ENERGIA = 7;
const int ZUMBADOR = 8;
const int VERDE = 9, AMARILLO = 10, ROJO = 11;

int medirAgua() {
  digitalWrite(ENERGIA, HIGH);
  delay(10);
  int nivel = analogRead(SENSOR);
  digitalWrite(ENERGIA, LOW);
  return nivel;
}

void setup() {
  pinMode(ENERGIA, OUTPUT);
  pinMode(ZUMBADOR, OUTPUT);
  pinMode(VERDE, OUTPUT);
  pinMode(AMARILLO, OUTPUT);
  pinMode(ROJO, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int nivel = medirAgua();
  Serial.print("Nivel: ");
  Serial.println(nivel);

  // Ajusta 200 y 450 con lo que marque tu sensor en un vaso con agua
  digitalWrite(VERDE, nivel < 200);
  digitalWrite(AMARILLO, nivel >= 200 && nivel < 450);
  digitalWrite(ROJO, nivel >= 450);
  digitalWrite(ZUMBADOR, nivel >= 450);   // ¡alarma!
  delay(500);
}
'''

COD_MACETA = r'''
// Maceta inteligente: sensor de humedad del suelo + servo bandera + LED
// Sensor: VCC -> pin 7 · GND -> GND · AO -> A0
// Servo SG90: café -> GND · rojo -> 5V · naranja -> pin 9 · LED rojo: pin 12 -> 220 ohms -> GND
#include <Servo.h>

const int SENSOR = A0;
const int ENERGIA = 7;
const int LED = 12;
Servo bandera;

// Calibra tu sensor: anota lo que marca en tierra seca y en tierra recién regada
const int SECO = 1000;
const int MOJADO = 400;

int humedadPorcentaje() {
  digitalWrite(ENERGIA, HIGH);
  delay(10);
  int lectura = analogRead(SENSOR);
  digitalWrite(ENERGIA, LOW);
  Serial.print("Lectura: ");
  Serial.print(lectura);
  return constrain(map(lectura, SECO, MOJADO, 0, 100), 0, 100);   // de 0 % a 100 %
}

void setup() {
  pinMode(ENERGIA, OUTPUT);
  pinMode(LED, OUTPUT);
  bandera.attach(9);
  Serial.begin(9600);
}

void loop() {
  int humedad = humedadPorcentaje();
  Serial.print("   Humedad: ");
  Serial.print(humedad);
  Serial.println("%");

  if (humedad < 30) {
    bandera.write(90);         // sube la bandera: ¡riégame!
    digitalWrite(LED, HIGH);
  } else {
    bandera.write(0);          // bandera abajo: estoy bien
    digitalWrite(LED, LOW);
  }
  delay(1000);
}
'''

COD_ESTACION = r'''
// Jefe: estación meteorológica completa (cambia de pantalla cada 3 segundos)
// DHT11: S -> 2 · LCD: RS 7, E 8, D4 9, D5 10, D6 11, D7 12 (igual que en la estación del clima)
// Fotoresistencia: 5V -> fotoresistencia -> A0 -> 10K -> GND · Zumbador activo: pin 3
#include <DHT.h>
#include <LiquidCrystal.h>

DHT dht(2, DHT11);
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
const int LUZ = A0;
const int ZUMBADOR = 3;
const float CALOR = 30.0;      // a partir de esta temperatura suena la alarma

int pantalla = 0;
unsigned long ultimoCambio = 0;

void setup() {
  dht.begin();
  lcd.begin(16, 2);
  pinMode(ZUMBADOR, OUTPUT);
  lcd.print("Estacion lista");
}

void loop() {
  if (millis() - ultimoCambio < 3000) return;   // todavía no toca cambiar de pantalla
  ultimoCambio = millis();

  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();
  int luz = map(analogRead(LUZ), 0, 1023, 0, 100);

  lcd.clear();
  if (pantalla == 0) {
    lcd.print("Temperatura");
    lcd.setCursor(0, 1);
    lcd.print(temperatura, 1);
    lcd.print((char)223);
    lcd.print("C");
  } else if (pantalla == 1) {
    lcd.print("Humedad");
    lcd.setCursor(0, 1);
    lcd.print(humedad, 0);
    lcd.print("%");
  } else {
    lcd.print("Luz");
    lcd.setCursor(0, 1);
    lcd.print(luz);
    lcd.print("%  ");
    lcd.print(luz > 50 ? "Dia" : "Noche");
  }
  pantalla = (pantalla + 1) % 3;

  // Alarma de calor
  if (!isnan(temperatura) && temperatura > CALOR) {
    digitalWrite(ZUMBADOR, HIGH);
    delay(200);
    digitalWrite(ZUMBADOR, LOW);
  }
}
'''

COD_BARRERA = r'''
// Barrera de estacionamiento: el sensor ultrasónico ve el auto y el servo levanta la pluma
// Ultrasónico: VCC -> 5V · Trig -> 7 · Echo -> 6 · GND -> GND
// Servo SG90: café GND · rojo 5V · naranja -> 9 · LED rojo 12 y LED verde 13 (220 ohms cada uno)
#include <Servo.h>

const int TRIG = 7, ECHO = 6;
const int ROJO = 12, VERDE = 13;
Servo pluma;

long medirDistancia() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);            // un "grito" de ultrasonido de 10 microsegundos
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long tiempo = pulseIn(ECHO, HIGH, 30000);   // cuánto tarda el eco (máximo 30 ms)
  return tiempo * 0.034 / 2;                  // el sonido viaja 0.034 cm por microsegundo (ida y vuelta)
}

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(ROJO, OUTPUT);
  pinMode(VERDE, OUTPUT);
  pluma.attach(9);
  pluma.write(0);                // pluma abajo
  digitalWrite(ROJO, HIGH);
  Serial.begin(9600);
}

void loop() {
  long distancia = medirDistancia();
  Serial.print(distancia);
  Serial.println(" cm");

  if (distancia > 0 && distancia < 10) {   // ¡llegó un auto!
    digitalWrite(ROJO, LOW);
    digitalWrite(VERDE, HIGH);
    for (int angulo = 0; angulo <= 90; angulo += 2) {   // sube despacito
      pluma.write(angulo);
      delay(15);
    }
    delay(3000);                                        // tiempo para pasar
    for (int angulo = 90; angulo >= 0; angulo -= 2) {   // baja despacito
      pluma.write(angulo);
      delay(15);
    }
    digitalWrite(VERDE, LOW);
    digitalWrite(ROJO, HIGH);
  }
  delay(100);
}
'''

COD_JOYSTICK = r'''
// Joystick: controla un servo, el brillo de un LED y una bocina
// Joystick: GND · +5V · VRx -> A0 · VRy -> A1 · SW -> 2
// Servo: naranja -> 9 · LED: pin 5 -> 220 ohms -> GND · Zumbador activo: pin 8
#include <Servo.h>

Servo servo;
const int EJE_X = A0, EJE_Y = A1, BOTON = 2;
const int LED = 5;
const int ZUMBADOR = 8;

void setup() {
  servo.attach(9);
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  pinMode(ZUMBADOR, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int x = analogRead(EJE_X);   // de 0 a 1023 (en el centro, cerca de 512)
  int y = analogRead(EJE_Y);

  servo.write(map(x, 0, 1023, 0, 180));                // izquierda-derecha mueve el servo
  analogWrite(LED, map(y, 0, 1023, 0, 255));           // arriba-abajo cambia el brillo
  digitalWrite(ZUMBADOR, digitalRead(BOTON) == LOW);   // presiona el joystick: ¡pip!

  Serial.print("X=");
  Serial.print(x);
  Serial.print("  Y=");
  Serial.println(y);
  delay(20);
}
'''

COD_PASO_A_PASO = r'''
// Plato giratorio para fotos 360° con el motor paso a paso
// Placa ULN2003: IN1 -> 8 · IN2 -> 9 · IN3 -> 10 · IN4 -> 11
//                + y - -> 5V y GND del módulo de alimentación · une el GND del módulo con el GND del Arduino
// Botón: pin 2 a GND (inicia una vuelta)
#include <Stepper.h>

const int PASOS_POR_VUELTA = 2048;
Stepper motor(PASOS_POR_VUELTA, 8, 10, 9, 11);   // ¡ojo con el orden: 8, 10, 9, 11!
const int BOTON = 2;

void setup() {
  motor.setSpeed(10);   // vueltas por minuto (este motor aguanta hasta unas 15)
  pinMode(BOTON, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  if (digitalRead(BOTON) == LOW) {
    // 8 paradas de 45°: en cada una puedes tomarle una foto a tu objeto
    for (int parada = 1; parada <= 8; parada++) {
      motor.step(PASOS_POR_VUELTA / 8);
      Serial.print("Foto ");
      Serial.println(parada);
      delay(1500);
    }
    for (int pin = 8; pin <= 11; pin++) digitalWrite(pin, LOW);   // deja descansar al motor
  }
}
'''

COD_VENTILADOR = r'''
// Ventilador con el chip L293D: velocidad y dirección
// L293D: 1 (Enable) -> 5 · 2 (Entrada 1) -> 4 · 7 (Entrada 2) -> 3 · 3 y 6 -> los dos cables del motor
//        4, 5, 12 y 13 -> GND · 16 -> 5V del Arduino · 8 -> 5V del módulo de alimentación (energía del motor)
// Botones a GND: velocidad -> 7 · dirección -> 8 · Une todos los GND.

const int ENABLE = 5, ENTRADA1 = 4, ENTRADA2 = 3;
const int BOTON_VELOCIDAD = 7, BOTON_DIRECCION = 8;

const int VELOCIDADES[] = {0, 150, 200, 255};   // apagado, baja, media, alta
int nivel = 0;
bool haciaAdelante = true;

void aplicar() {
  digitalWrite(ENTRADA1, haciaAdelante ? HIGH : LOW);
  digitalWrite(ENTRADA2, haciaAdelante ? LOW : HIGH);
  analogWrite(ENABLE, VELOCIDADES[nivel]);
  Serial.print("Velocidad: ");
  Serial.print(nivel);
  Serial.println(haciaAdelante ? "  (adelante)" : "  (reversa)");
}

void setup() {
  pinMode(ENABLE, OUTPUT);
  pinMode(ENTRADA1, OUTPUT);
  pinMode(ENTRADA2, OUTPUT);
  pinMode(BOTON_VELOCIDAD, INPUT_PULLUP);
  pinMode(BOTON_DIRECCION, INPUT_PULLUP);
  Serial.begin(9600);
  aplicar();
}

void loop() {
  if (digitalRead(BOTON_VELOCIDAD) == LOW) {
    nivel = (nivel + 1) % 4;
    aplicar();
    while (digitalRead(BOTON_VELOCIDAD) == LOW) {}   // espera a que sueltes
    delay(50);
  }
  if (digitalRead(BOTON_DIRECCION) == LOW) {
    analogWrite(ENABLE, 0);   // frena antes de cambiar de dirección
    delay(300);
    haciaAdelante = !haciaAdelante;
    aplicar();
    while (digitalRead(BOTON_DIRECCION) == LOW) {}
    delay(50);
  }
}
'''

COD_GRUA = r'''
// Jefe: grúa robótica con joystick
// Motor paso a paso (base): ULN2003 IN1 8 · IN2 9 · IN3 10 · IN4 11 · + y - al módulo de alimentación
// Servo (brazo): naranja -> 6 · Joystick: VRx -> A0 · VRy -> A1 · SW -> 2 · LED del gancho: pin 13
#include <Servo.h>
#include <Stepper.h>

Stepper base(2048, 8, 10, 9, 11);
Servo brazo;
const int EJE_X = A0, EJE_Y = A1, BOTON = 2, GANCHO = 13;

int anguloBrazo = 90;
bool ganchoCerrado = false;
bool antes = HIGH;

void setup() {
  base.setSpeed(12);
  brazo.attach(6);
  brazo.write(anguloBrazo);
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(GANCHO, OUTPUT);
}

void loop() {
  int x = analogRead(EJE_X);
  int y = analogRead(EJE_Y);

  // La base gira poquito a poco mientras inclinas el joystick a un lado
  if (x > 700) base.step(16);
  if (x < 300) base.step(-16);

  // El brazo sube o baja de 2 en 2 grados
  if (y > 700 && anguloBrazo < 170) anguloBrazo += 2;
  if (y < 300 && anguloBrazo > 10) anguloBrazo -= 2;
  brazo.write(anguloBrazo);

  // El botón del joystick abre y cierra el gancho
  bool ahora = digitalRead(BOTON);
  if (antes == HIGH && ahora == LOW) {
    ganchoCerrado = !ganchoCerrado;
    digitalWrite(GANCHO, ganchoCerrado);
  }
  antes = ahora;
  delay(15);
}
'''

COD_TECLADO = r'''
// Teclado matricial 4x4: ¿qué tecla presioné?
// Librería: Keypad (de Mark Stanley y Alexander Brevig)
// Cables del teclado, de izquierda a derecha viéndolo de frente: 9, 8, 7, 6, 5, 4, 3, 2
// Zumbador activo: pin 10
#include <Keypad.h>
''' + TECLADO_4X4 + r'''
byte pinesFilas[FILAS] = {9, 8, 7, 6};
byte pinesColumnas[COLUMNAS] = {5, 4, 3, 2};
Keypad teclado = Keypad(makeKeymap(teclas), pinesFilas, pinesColumnas, FILAS, COLUMNAS);

const int ZUMBADOR = 10;

void setup() {
  pinMode(ZUMBADOR, OUTPUT);
  Serial.begin(9600);
  Serial.println("Presiona una tecla...");
}

void loop() {
  char tecla = teclado.getKey();
  if (tecla) {
    Serial.print("Tecla: ");
    Serial.println(tecla);
    digitalWrite(ZUMBADOR, HIGH);
    delay(60);
    digitalWrite(ZUMBADOR, LOW);
  }
}
'''

COD_CERRADURA = r'''
// Cerradura con contraseña: teclado 4x4 + servo
// Teclado: cables a 9, 8, 7, 6, 5, 4, 3, 2 (igual que antes) · Servo: naranja -> 11
// LED verde 12 · LED rojo 13 (220 ohms cada uno) · Zumbador activo 10
// Escribe la clave y presiona # para abrir. * borra lo que llevas.
#include <Keypad.h>
#include <Servo.h>
''' + TECLADO_4X4 + r'''
byte pinesFilas[FILAS] = {9, 8, 7, 6};
byte pinesColumnas[COLUMNAS] = {5, 4, 3, 2};
Keypad teclado = Keypad(makeKeymap(teclas), pinesFilas, pinesColumnas, FILAS, COLUMNAS);

Servo cerrojo;
const int VERDE = 12, ROJO = 13, ZUMBADOR = 10;
const String CLAVE = "2580";   // cámbiala por tu clave secreta
String escrito = "";

void pitido(int ms) {
  digitalWrite(ZUMBADOR, HIGH);
  delay(ms);
  digitalWrite(ZUMBADOR, LOW);
}

void setup() {
  cerrojo.attach(11);
  cerrojo.write(0);              // cerrado
  pinMode(VERDE, OUTPUT);
  pinMode(ROJO, OUTPUT);
  pinMode(ZUMBADOR, OUTPUT);
  digitalWrite(ROJO, HIGH);
  Serial.begin(9600);
}

void loop() {
  char tecla = teclado.getKey();
  if (!tecla) return;
  pitido(40);

  if (tecla == '*') {
    escrito = "";
    Serial.println("Borrado");
  } else if (tecla == '#') {
    if (escrito == CLAVE) {
      Serial.println("Acceso concedido!");
      digitalWrite(ROJO, LOW);
      digitalWrite(VERDE, HIGH);
      cerrojo.write(90);         // abre
      delay(5000);
      cerrojo.write(0);          // vuelve a cerrar
      digitalWrite(VERDE, LOW);
      digitalWrite(ROJO, HIGH);
    } else {
      Serial.println("Clave incorrecta");
      for (int i = 0; i < 3; i++) {
        pitido(150);
        delay(100);
      }
    }
    escrito = "";
  } else {
    escrito += tecla;
    Serial.println(escrito);     // en una cerradura de verdad mostraríamos asteriscos
  }
}
'''

COD_IR_CODIGOS = r'''
// Control remoto: descubre el código de cada botón
// Librería: IRremote (de shirriff, z3t0 y ArminJo), versión 4 o más nueva
// Receptor infrarrojo: S (señal) -> 11 · + (centro) -> 5V · - -> GND
#include <IRremote.hpp>

const int RECEPTOR = 11;

void setup() {
  Serial.begin(9600);
  IrReceiver.begin(RECEPTOR, ENABLE_LED_FEEDBACK);   // el LED 13 parpadea cuando recibe algo
  Serial.println("Apunta el control al receptor y presiona botones...");
}

void loop() {
  if (IrReceiver.decode()) {
    // Si dejas el botón presionado llegan "repeticiones": las ignoramos
    if (!(IrReceiver.decodedIRData.flags & IRDATA_FLAGS_IS_REPEAT)) {
      Serial.print("Codigo del boton: 0x");
      Serial.println(IrReceiver.decodedIRData.command, HEX);
    }
    IrReceiver.resume();   // listo para el siguiente botón
  }
}
'''

COD_IR_LUCES = r'''
// Control remoto: enciende las luces de la pirámide
// Receptor IR: S -> 11 · + -> 5V · - -> GND · LEDs (220 ohms): rojo 4 · verde 5 · azul 6
// Botones del control: 1, 2 y 3 encienden / apagan cada LED · 0 apaga todo
#include <IRremote.hpp>

const int RECEPTOR = 11;
const int LEDS[] = {4, 5, 6};

// Si tu control da otros códigos (los viste en la práctica anterior), cámbialos aquí
const uint16_t BOTON_0 = 0x16, BOTON_1 = 0x0C, BOTON_2 = 0x18, BOTON_3 = 0x5E;
bool encendido[] = {false, false, false};

void cambiar(int i) {
  encendido[i] = !encendido[i];
  digitalWrite(LEDS[i], encendido[i]);
}

void setup() {
  for (int i = 0; i < 3; i++) pinMode(LEDS[i], OUTPUT);
  IrReceiver.begin(RECEPTOR, ENABLE_LED_FEEDBACK);
}

void loop() {
  if (!IrReceiver.decode()) return;
  bool repetido = IrReceiver.decodedIRData.flags & IRDATA_FLAGS_IS_REPEAT;
  uint16_t codigo = IrReceiver.decodedIRData.command;
  IrReceiver.resume();
  if (repetido) return;

  if (codigo == BOTON_1) cambiar(0);
  else if (codigo == BOTON_2) cambiar(1);
  else if (codigo == BOTON_3) cambiar(2);
  else if (codigo == BOTON_0) {
    for (int i = 0; i < 3; i++) {
      encendido[i] = false;
      digitalWrite(LEDS[i], LOW);
    }
  }
}
'''

COD_PIR = r'''
// Alarma de intrusos con el sensor de movimiento PIR HC-SR501
// PIR: VCC -> 5V · OUT -> 2 · GND -> GND   (al encenderlo, tarda 1 minuto en calibrarse)
// LED rojo: pin 12 -> 220 ohms -> GND · Zumbador activo: pin 8

const int PIR = 2;
const int LED = 12;
const int ZUMBADOR = 8;
int intrusos = 0;
bool habiaMovimiento = false;

void setup() {
  pinMode(PIR, INPUT);
  pinMode(LED, OUTPUT);
  pinMode(ZUMBADOR, OUTPUT);
  Serial.begin(9600);
  Serial.println("Calibrando... no te muevas frente al sensor (60 segundos)");
  delay(60000);
  Serial.println("Alarma activada!");
}

void loop() {
  bool movimiento = digitalRead(PIR) == HIGH;
  if (movimiento && !habiaMovimiento) {   // empezó un movimiento nuevo
    intrusos++;
    Serial.print("Movimiento detectado! Total: ");
    Serial.println(intrusos);
  }
  habiaMovimiento = movimiento;

  digitalWrite(LED, movimiento);
  if (movimiento) {               // sirena intermitente
    digitalWrite(ZUMBADOR, HIGH);
    delay(150);
    digitalWrite(ZUMBADOR, LOW);
    delay(150);
  }
}
'''

COD_RFID_LEER = r'''
// RFID: lee el número secreto (UID) de tu tarjeta o llavero
// Librería: MFRC522 (de GithubCommunity)
// RC522: SDA -> 10 · SCK -> 13 · MOSI -> 11 · MISO -> 12 · RST -> 9 · GND -> GND · 3.3V -> 3.3V  (¡NUNCA a 5V!)
#include <SPI.h>
#include <MFRC522.h>

MFRC522 lector(10, 9);   // SDA, RST

void setup() {
  Serial.begin(9600);
  SPI.begin();
  lector.PCD_Init();
  Serial.println("Acerca una tarjeta o un llavero al lector...");
}

void loop() {
  if (!lector.PICC_IsNewCardPresent() || !lector.PICC_ReadCardSerial()) return;

  Serial.print("UID: ");
  for (byte i = 0; i < lector.uid.size; i++) {
    Serial.print("0x");
    if (lector.uid.uidByte[i] < 0x10) Serial.print("0");
    Serial.print(lector.uid.uidByte[i], HEX);
    if (i < lector.uid.size - 1) Serial.print(", ");
  }
  Serial.println();
  lector.PICC_HaltA();   // terminamos con esta tarjeta
}
'''

COD_RFID_ACCESO = r'''
// RFID: acceso autorizado
// RC522 conectado como en la práctica anterior (¡a 3.3V!) · Servo: naranja -> 6
// LED verde 4 · LED rojo 5 (220 ohms cada uno) · Zumbador activo 8
#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

MFRC522 lector(10, 9);
Servo puerta;
const int VERDE = 4, ROJO = 5, ZUMBADOR = 8;

// Pega aquí el UID de TU tarjeta (lo copiaste en la práctica anterior)
byte autorizada[4] = {0xDE, 0xAD, 0xBE, 0xEF};

bool esAutorizada() {
  if (lector.uid.size != 4) return false;
  for (byte i = 0; i < 4; i++) {
    if (lector.uid.uidByte[i] != autorizada[i]) return false;
  }
  return true;
}

void setup() {
  SPI.begin();
  lector.PCD_Init();
  puerta.attach(6);
  puerta.write(0);
  pinMode(VERDE, OUTPUT);
  pinMode(ROJO, OUTPUT);
  pinMode(ZUMBADOR, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (!lector.PICC_IsNewCardPresent() || !lector.PICC_ReadCardSerial()) return;

  if (esAutorizada()) {
    Serial.println("Bienvenido");
    digitalWrite(VERDE, HIGH);
    digitalWrite(ZUMBADOR, HIGH);
    delay(100);
    digitalWrite(ZUMBADOR, LOW);
    puerta.write(90);            // abre
    delay(4000);
    puerta.write(0);             // cierra
    digitalWrite(VERDE, LOW);
  } else {
    Serial.println("Tarjeta desconocida");
    digitalWrite(ROJO, HIGH);
    digitalWrite(ZUMBADOR, HIGH);
    delay(800);
    digitalWrite(ZUMBADOR, LOW);
    digitalWrite(ROJO, LOW);
  }
  lector.PICC_HaltA();
}
'''

COD_BOVEDA = r'''
// Jefe: bóveda de doble seguridad (tarjeta RFID + clave en el teclado)
// RC522 (¡a 3.3V!): SDA 10 · SCK 13 · MOSI 11 · MISO 12 · RST 9
// Teclado 4x4: filas -> 2, 3, 4, 5 · columnas -> 6, 7, 8, A0 (cables del teclado de izquierda a derecha)
// Servo: naranja -> A1 · Zumbador activo -> A2 · LED verde -> A3 · LED rojo -> A4 (220 ohms)
#include <SPI.h>
#include <MFRC522.h>
#include <Keypad.h>
#include <Servo.h>

MFRC522 lector(10, 9);
Servo cerrojo;
''' + TECLADO_4X4 + r'''
byte pinesFilas[FILAS] = {2, 3, 4, 5};
byte pinesColumnas[COLUMNAS] = {6, 7, 8, A0};
Keypad teclado = Keypad(makeKeymap(teclas), pinesFilas, pinesColumnas, FILAS, COLUMNAS);

const int ZUMBADOR = A2, VERDE = A3, ROJO = A4;
byte autorizada[4] = {0xDE, 0xAD, 0xBE, 0xEF};   // el UID de tu tarjeta
const String CLAVE = "1793";                      // tu clave secreta

bool tarjetaOk = false;          // ¿ya pasó el paso 1?
unsigned long horaTarjeta = 0;
String escrito = "";

void pitido(int ms) {
  digitalWrite(ZUMBADOR, HIGH);
  delay(ms);
  digitalWrite(ZUMBADOR, LOW);
}

bool esAutorizada() {
  if (lector.uid.size != 4) return false;
  for (byte i = 0; i < 4; i++) {
    if (lector.uid.uidByte[i] != autorizada[i]) return false;
  }
  return true;
}

void reiniciar() {
  tarjetaOk = false;
  escrito = "";
  digitalWrite(VERDE, LOW);
  Serial.println("Paso 1: acerca tu tarjeta");
}

void setup() {
  SPI.begin();
  lector.PCD_Init();
  cerrojo.attach(A1);
  cerrojo.write(0);
  pinMode(ZUMBADOR, OUTPUT);
  pinMode(VERDE, OUTPUT);
  pinMode(ROJO, OUTPUT);
  Serial.begin(9600);
  reiniciar();
}

void loop() {
  // Paso 1: la tarjeta
  if (!tarjetaOk) {
    if (!lector.PICC_IsNewCardPresent() || !lector.PICC_ReadCardSerial()) return;
    if (esAutorizada()) {
      tarjetaOk = true;
      horaTarjeta = millis();
      digitalWrite(VERDE, HIGH);   // verde fijo: tarjeta aceptada
      pitido(100);
      Serial.println("Paso 2: escribe la clave y presiona #");
    } else {
      digitalWrite(ROJO, HIGH);
      pitido(700);
      digitalWrite(ROJO, LOW);
    }
    lector.PICC_HaltA();
    return;
  }

  // Tienes 15 segundos para escribir la clave
  if (millis() - horaTarjeta > 15000) {
    Serial.println("Tiempo agotado");
    pitido(700);
    reiniciar();
    return;
  }

  // Paso 2: la clave
  char tecla = teclado.getKey();
  if (!tecla) return;
  pitido(30);
  if (tecla == '#') {
    if (escrito == CLAVE) {
      Serial.println("Boveda abierta!");
      cerrojo.write(90);
      for (int i = 0; i < 3; i++) {
        pitido(80);
        delay(80);
      }
      delay(5000);
      cerrojo.write(0);
    } else {
      Serial.println("Clave incorrecta");
      digitalWrite(ROJO, HIGH);
      pitido(1000);
      digitalWrite(ROJO, LOW);
    }
    reiniciar();
  } else if (tecla == '*') {
    escrito = "";
  } else {
    escrito += tecla;
  }
}
'''

COD_RELOJ = r'''
// Reloj de verdad: módulo RTC + pantalla LCD
// Librerías: RTClib (de Adafruit) y LiquidCrystal
// RTC: VCC -> 5V · GND -> GND · SDA -> A4 · SCL -> A5   (con su pila de botón puesta)
// LCD: RS 7 · E 8 · D4 9 · D5 10 · D6 11 · D7 12 (igual que en la estación del clima)
#include <Wire.h>
#include <RTClib.h>
#include <LiquidCrystal.h>

RTC_DS1307 rtc;    // si tu módulo dice DS3231, cámbialo por RTC_DS3231
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
const char* DIAS[] = {"Dom", "Lun", "Mar", "Mie", "Jue", "Vie", "Sab"};

void dosDigitos(int n) {
  if (n < 10) lcd.print('0');
  lcd.print(n);
}

void setup() {
  lcd.begin(16, 2);
  if (!rtc.begin()) {
    lcd.print("No veo el RTC");
    while (true) {}
  }
  // SOLO LA PRIMERA VEZ: quita las // de la siguiente línea y sube el programa (toma la hora de tu compu).
  // Después vuelve a ponerlas y súbelo otra vez; si no, el reloj regresa a esa hora cada vez que se reinicia.
  // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
}

void loop() {
  DateTime ahora = rtc.now();
  lcd.setCursor(0, 0);
  lcd.print(DIAS[ahora.dayOfTheWeek()]);
  lcd.print(" ");
  dosDigitos(ahora.day());
  lcd.print("/");
  dosDigitos(ahora.month());
  lcd.print("/");
  lcd.print(ahora.year());

  lcd.setCursor(4, 1);
  dosDigitos(ahora.hour());
  lcd.print(":");
  dosDigitos(ahora.minute());
  lcd.print(":");
  dosDigitos(ahora.second());
  delay(250);
}
'''

COD_DESPERTADOR = r'''
// Despertador: el reloj RTC + LCD de la práctica anterior, más un buzzer pasivo y un botón
// Buzzer pasivo: + -> 6 · - -> GND · Botón para apagar la alarma: pin 2 a GND
#include <Wire.h>
#include <RTClib.h>
#include <LiquidCrystal.h>

RTC_DS1307 rtc;    // o RTC_DS3231, igual que en el reloj
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
const int BUZZER = 6, BOTON = 2;

const int ALARMA_HORA = 7;      // ¡cámbiala! (formato de 24 horas)
const int ALARMA_MINUTO = 30;
int ultimoDiaQueSono = -1;

void dosDigitos(int n) {
  if (n < 10) lcd.print('0');
  lcd.print(n);
}

void sonarAlarma() {
  lcd.setCursor(0, 1);
  lcd.print("   ARRIBA!      ");
  unsigned long inicio = millis();
  // Suena hasta que presiones el botón (o máximo 1 minuto)
  while (digitalRead(BOTON) == HIGH && millis() - inicio < 60000) {
    tone(BUZZER, 880, 150);
    delay(200);
    tone(BUZZER, 1175, 150);
    delay(400);
  }
  noTone(BUZZER);
  lcd.clear();
}

void setup() {
  lcd.begin(16, 2);
  pinMode(BOTON, INPUT_PULLUP);
  rtc.begin();
}

void loop() {
  DateTime ahora = rtc.now();
  lcd.setCursor(0, 0);
  lcd.print("Hora   ");
  dosDigitos(ahora.hour());
  lcd.print(":");
  dosDigitos(ahora.minute());
  lcd.print(":");
  dosDigitos(ahora.second());

  lcd.setCursor(0, 1);
  lcd.print("Alarma ");
  dosDigitos(ALARMA_HORA);
  lcd.print(":");
  dosDigitos(ALARMA_MINUTO);

  if (ahora.hour() == ALARMA_HORA && ahora.minute() == ALARMA_MINUTO && ahora.day() != ultimoDiaQueSono) {
    ultimoDiaQueSono = ahora.day();   // así solo suena una vez al día
    sonarAlarma();
  }
  delay(250);
}
'''

COD_CRONOMETRO = r'''
// Cronómetro con millis(): mide tiempos en décimas de segundo
// LCD como en las prácticas anteriores · Botón iniciar/pausar -> 2 · Botón reiniciar -> 3 (a GND)
#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
const int INICIAR = 2, REINICIAR = 3;

bool corriendo = false;
unsigned long inicio = 0;      // cuándo empezó a correr
unsigned long acumulado = 0;   // el tiempo que llevaba antes de pausar
bool antes = HIGH;

void setup() {
  lcd.begin(16, 2);
  pinMode(INICIAR, INPUT_PULLUP);
  pinMode(REINICIAR, INPUT_PULLUP);
  lcd.print("Cronometro");
}

void loop() {
  bool ahora = digitalRead(INICIAR);
  if (antes == HIGH && ahora == LOW) {
    if (corriendo) acumulado += millis() - inicio;   // pausa: guarda lo que llevaba
    else inicio = millis();                          // arranca
    corriendo = !corriendo;
    delay(50);
  }
  antes = ahora;

  if (digitalRead(REINICIAR) == LOW && !corriendo) acumulado = 0;

  unsigned long total = acumulado + (corriendo ? millis() - inicio : 0);
  unsigned long segundos = total / 1000;
  int decimas = (total % 1000) / 100;

  lcd.setCursor(0, 1);
  lcd.print(segundos / 60);        // minutos
  lcd.print(":");
  if (segundos % 60 < 10) lcd.print("0");
  lcd.print(segundos % 60);
  lcd.print(".");
  lcd.print(decimas);
  lcd.print(corriendo ? "  >    " : "  ||   ");
}
'''

COD_REFLEJOS = r'''
// Juego de reflejos: presiona el botón en cuanto se encienda el LED
// LED: pin 8 -> 220 ohms -> GND · Botón: pin 2 a GND · Buzzer pasivo: pin 9

const int LED = 8, BOTON = 2, BUZZER = 9;
unsigned long record = 99999;

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(BOTON, INPUT_PULLUP);
  Serial.begin(9600);
  randomSeed(analogRead(A5));
  Serial.println("Juego de reflejos! Presiona el boton para empezar.");
}

void loop() {
  while (digitalRead(BOTON) == HIGH) {}   // espera a que presiones para empezar
  while (digitalRead(BOTON) == LOW) {}    // y a que lo sueltes
  Serial.println("Preparate...");

  unsigned long espera = random(2000, 6000);   // espera sorpresa de 2 a 6 segundos
  unsigned long inicioEspera = millis();
  while (millis() - inicioEspera < espera) {
    if (digitalRead(BOTON) == LOW) {           // ¡presionaste antes de tiempo!
      Serial.println("Muy pronto! Espera a que se encienda la luz.");
      tone(BUZZER, 150, 500);
      delay(1000);
      return;
    }
  }

  digitalWrite(LED, HIGH);
  tone(BUZZER, 1000, 100);
  unsigned long salida = millis();
  while (digitalRead(BOTON) == HIGH) {}        // espera tu reacción
  unsigned long reaccion = millis() - salida;
  digitalWrite(LED, LOW);

  Serial.print("Tu tiempo: ");
  Serial.print(reaccion);
  Serial.println(" ms");
  if (reaccion < record) {
    record = reaccion;
    Serial.println("NUEVO RECORD!");
    tone(BUZZER, 1319, 300);
  }
  Serial.println("Presiona el boton para jugar otra vez.");
  delay(500);
}
'''

COD_SIMON = r'''
// Simón dice electrónico: repite la secuencia de luces (¡cada ronda es más larga!)
// LEDs (220 ohms): rojo 2 · verde 3 · azul 4 · Botones a GND: rojo 5 · verde 6 · azul 7 · Buzzer pasivo: 8

const int LEDS[] = {2, 3, 4};
const int BOTONES[] = {5, 6, 7};
const int TONOS[] = {262, 330, 392};
const int BUZZER = 8;

int secuencia[50];
int largo = 0;

void encender(int i, int ms) {
  digitalWrite(LEDS[i], HIGH);
  tone(BUZZER, TONOS[i], ms);
  delay(ms);
  digitalWrite(LEDS[i], LOW);
  delay(150);
}

int esperarBoton() {
  while (true) {
    for (int i = 0; i < 3; i++) {
      if (digitalRead(BOTONES[i]) == LOW) {
        encender(i, 250);
        while (digitalRead(BOTONES[i]) == LOW) {}
        return i;
      }
    }
  }
}

void perder() {
  Serial.print("Perdiste! Llegaste a la ronda ");
  Serial.println(largo);
  for (int n = 0; n < 3; n++) {
    for (int i = 0; i < 3; i++) digitalWrite(LEDS[i], HIGH);
    tone(BUZZER, 150, 300);
    delay(350);
    for (int i = 0; i < 3; i++) digitalWrite(LEDS[i], LOW);
    delay(200);
  }
  largo = 0;
  delay(1000);
}

void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(LEDS[i], OUTPUT);
    pinMode(BOTONES[i], INPUT_PULLUP);
  }
  Serial.begin(9600);
  randomSeed(analogRead(A5));
}

void loop() {
  secuencia[largo] = random(0, 3);   // agrega un color nuevo a la secuencia
  largo++;
  Serial.print("Ronda ");
  Serial.println(largo);

  for (int i = 0; i < largo; i++) encender(secuencia[i], 400);   // Simón muestra la secuencia

  for (int i = 0; i < largo; i++) {                             // ahora te toca a ti
    if (esperarBoton() != secuencia[i]) {
      perder();
      return;
    }
  }
  delay(800);                        // ¡bien! siguiente ronda
  if (largo == 50) largo = 0;        // ¡completaste el juego entero!
}
'''

COD_BURBUJA = r'''
// Nivel de burbuja: el acelerómetro GY-521 mueve un punto en la matriz 8x8
// GY-521: VCC -> 5V · GND -> GND · SCL -> A5 · SDA -> A4
// Matriz MAX7219 (librería LedControl): DIN 12 · CLK 11 · CS 10
#include <Wire.h>
#include <LedControl.h>

const int MPU = 0x68;   // la "dirección" del GY-521 en el bus I2C
LedControl matriz = LedControl(12, 11, 10, 1);

void setup() {
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);     // registro de energía del sensor
  Wire.write(0);        // ¡despierta!
  Wire.endTransmission(true);

  matriz.shutdown(0, false);
  matriz.setIntensity(0, 5);
  matriz.clearDisplay(0);
  Serial.begin(9600);
}

void loop() {
  // Pide la aceleración en X y en Y (2 bytes cada una)
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 4, true);
  int16_t ax = Wire.read() << 8;   // primero el byte alto...
  ax |= Wire.read();               // ...y luego el bajo
  int16_t ay = Wire.read() << 8;
  ay |= Wire.read();

  // Plano = 0 · muy inclinado = cerca de ±16384. Lo convertimos a una posición de 0 a 7.
  int columna = constrain(map(ax, -8000, 8000, 0, 7), 0, 7);
  int fila = constrain(map(ay, -8000, 8000, 0, 7), 0, 7);

  matriz.clearDisplay(0);
  matriz.setLed(0, fila, columna, true);

  Serial.print("X=");
  Serial.print(ax);
  Serial.print("  Y=");
  Serial.println(ay);
  delay(50);
}
'''

COD_ENCODER = r'''
// Perilla mágica: el codificador rotatorio mueve un servo de 10 en 10 grados
// Codificador: CLK -> 2 · DT -> 3 · SW -> 4 · + -> 5V · GND -> GND
// Servo: naranja -> 9
#include <Servo.h>

const int CLK = 2, DT = 3, SW = 4;
Servo servo;
int posicion = 9;            // de 0 a 18 (por 10 = grados)
int ultimoCLK;

void setup() {
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT_PULLUP);
  servo.attach(9);
  servo.write(posicion * 10);
  ultimoCLK = digitalRead(CLK);
  Serial.begin(9600);
}

void loop() {
  int actualCLK = digitalRead(CLK);
  if (actualCLK != ultimoCLK && actualCLK == LOW) {   // la perilla dio un "clic"
    if (digitalRead(DT) != actualCLK) posicion++;      // hacia un lado
    else posicion--;                                   // hacia el otro
    posicion = constrain(posicion, 0, 18);
    servo.write(posicion * 10);
    Serial.print("Angulo: ");
    Serial.println(posicion * 10);
  }
  ultimoCLK = actualCLK;

  if (digitalRead(SW) == LOW) {                        // presiona la perilla: al centro
    posicion = 9;
    servo.write(90);
    Serial.println("Al centro");
    delay(300);
  }
}
'''

COD_TEMPORIZADOR = r'''
// Jefe: temporizador de cocina (gira la perilla para elegir minutos y presiónala para empezar)
// Codificador: CLK 2 · DT 3 · SW 4 · LCD: RS 7, E 8, D4 9, D5 10, D6 11, D7 12 · Buzzer pasivo: 6
#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
const int CLK = 2, DT = 3, SW = 4, BUZZER = 6;

int minutos = 5;
int ultimoCLK;
bool contando = false;
unsigned long fin = 0;

void mostrarTiempo(unsigned long segundos) {
  lcd.setCursor(0, 1);
  if (segundos / 60 < 10) lcd.print("0");
  lcd.print(segundos / 60);
  lcd.print(":");
  if (segundos % 60 < 10) lcd.print("0");
  lcd.print(segundos % 60);
  lcd.print("        ");
}

void pantallaElegir() {
  lcd.clear();
  lcd.print("Elige minutos");
  mostrarTiempo(minutos * 60UL);
}

void esperarSoltar() {
  while (digitalRead(SW) == LOW) {}
  delay(50);
}

void setup() {
  lcd.begin(16, 2);
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT_PULLUP);
  ultimoCLK = digitalRead(CLK);
  pantallaElegir();
}

void loop() {
  if (!contando) {
    // Elegir los minutos con la perilla
    int actualCLK = digitalRead(CLK);
    if (actualCLK != ultimoCLK && actualCLK == LOW) {
      minutos += (digitalRead(DT) != actualCLK) ? 1 : -1;
      minutos = constrain(minutos, 1, 60);
      mostrarTiempo(minutos * 60UL);
    }
    ultimoCLK = actualCLK;

    if (digitalRead(SW) == LOW) {   // ¡a contar!
      esperarSoltar();
      contando = true;
      fin = millis() + minutos * 60000UL;
      lcd.clear();
      lcd.print("Contando...");
    }
    return;
  }

  long restante = (long)(fin - millis()) / 1000;
  if (restante > 0) {
    mostrarTiempo(restante);
  } else {
    lcd.clear();
    lcd.print("Tiempo!");
    for (int i = 0; i < 5; i++) {
      tone(BUZZER, 988, 200);
      delay(250);
      tone(BUZZER, 1319, 400);
      delay(600);
    }
    contando = false;
    pantallaElegir();
  }

  if (contando && digitalRead(SW) == LOW) {   // presionar mientras cuenta: cancelar
    esperarSoltar();
    contando = false;
    lcd.clear();
    lcd.print("Cancelado");
    delay(800);
    pantallaElegir();
  }
}
'''

COD_PLANTILLA = r'''
// Plantilla para tu proyecto final: LEER -> DECIDIR -> ACTUAR
// 1) Escribe aquí qué hace tu invento:
//    Ejemplo: "Si la tierra de la maceta está seca, enciende un LED y suena una melodía"
// 2) Anota tus conexiones:
//    Sensor ........ -> pin ....
//    Actuador ...... -> pin ....

// ----- Pines -----
const int SENSOR = A0;
const int ACTUADOR = 9;

// ----- Valores que puedes ajustar -----
int umbral = 500;

void setup() {
  pinMode(ACTUADOR, OUTPUT);
  Serial.begin(9600);
  Serial.println("Mi invento esta listo");
}

// Paso 1: LEER el mundo con un sensor
int leerSensor() {
  return analogRead(SENSOR);
}

// Paso 2: DECIDIR qué hacer con ese dato
bool hayQueActuar(int valor) {
  return valor > umbral;
}

// Paso 3: ACTUAR (luz, sonido, movimiento...)
void actuar(bool encender) {
  digitalWrite(ACTUADOR, encender ? HIGH : LOW);
}

void loop() {
  int valor = leerSensor();
  Serial.println(valor);          // revisa tus datos en el monitor serial
  actuar(hayQueActuar(valor));
  delay(100);
}
'''


# ========================
# MINIJUEGO (solo uno: el kit es el protagonista)
# ========================
JUEGOS = {
    'clasifica_kit': {
        'nombre': 'Detective del kit: ¿sensor, actuador o pantalla?', 'icono': '🧰', 'plantilla': 'clasifica',
        'en_arcade': True, 'descripcion': '¿La pieza siente, se mueve o hace ruido, o muestra información?',
        'configuracion': {'tema': 'personalizado', 'rondas': 14, 'tiempo': 10, 'categorias': [
            {'nombre': 'Sensores y entradas', 'emoji': '🎛️', 'tarjetas': [
                'Sensor ultrasónico', 'Sensor de movimiento PIR', 'Fotoresistencia', 'Termistor', 'DHT11',
                'Sensor de sonido', 'Sensor de humedad del suelo', 'Sensor de nivel de agua', 'Sensor de gas MQ-2',
                'Interruptor de inclinación', 'GY-521 (acelerómetro)', 'Receptor infrarrojo', 'Joystick',
                'Lector RFID RC522', 'Potenciómetro', 'Teclado 4x4']},
            {'nombre': 'Actuadores', 'emoji': '⚙️', 'tarjetas': [
                'Servomotor SG90', 'Motor paso a paso', 'Zumbador activo', 'Buzzer pasivo', 'LED', 'LED RGB',
                'Motor de 3 V', 'Relé']},
            {'nombre': 'Pantallas', 'emoji': '📟', 'tarjetas': [
                'Pantalla LCD 1602', 'Display de 7 segmentos', 'Matriz de LEDs MAX7219', 'Display de 4 dígitos']},
        ]},
    },
}


# ========================
# MUNDOS
# ========================
MUNDOS = [
    # ---------- Sin kit: dos días de simulador y actividades desconectadas ----------
    {'nombre': 'Simulador Tinkercad: Base de Entrenamiento', 'tema': 'espacio',
     'descripcion': 'Tu kit viene en camino. Mientras llega, entrena como los astronautas: primero en papel y en el '
                    'simulador, para que el día que lo abras ya sepas exactamente qué hacer.',
     'niveles': [
         {'nombre': 'Día 1: planos del ingeniero', 'cofre': 25, 'misiones': [
             mision('El circuito humano', 'presencial',
                    '⚡ Sin kit y sin computadora.\n\n'
                    '1. Formen un círculo tomados de las manos: dos compañeros son la pila (+ y −), uno es el LED y uno es el interruptor.\n'
                    '2. Pasen un "apretón de mano" (la corriente) desde el + de la pila. El LED levanta los brazos solo si el '
                    'apretón da la vuelta completa y regresa al −.\n'
                    '3. Cuando el interruptor suelta las manos, ¿qué pasa? ¿Y si la corriente se salta al LED (corto circuito)?\n\n'
                    'Con esto entenderás por qué un circuito necesita estar CERRADO.', xp=50, monedas=15),
             mision('Electricidad y componentes', 'cuestionario', 'Lo básico que todo inventor necesita saber antes de conectar.',
                    xp=60, monedas=15, preguntas=[
                        ('¿Cuál es la pata positiva (ánodo) de un LED?', 'La pata más larga',
                         ['La pata más corta', 'Las dos son iguales', 'La que está doblada']),
                        ('¿Para qué ponemos una resistencia junto al LED?', 'Para limitar la corriente y que no se queme',
                         ['Para que brille de colores', 'Para que gaste más pila', 'Para que suene']),
                        ('Si la electricidad fuera agua en una manguera, el voltaje sería…', 'La presión que empuja el agua',
                         ['El color del agua', 'El tamaño de la cubeta', 'La temperatura del agua']),
                        ('Un circuito funciona solo cuando está…', 'Cerrado: la corriente puede dar toda la vuelta',
                         ['Abierto', 'Mojado', 'Desconectado de la pila']),
                        ('Un corto circuito ocurre cuando…', 'La corriente va de + a − sin pasar por nada que la frene',
                         ['El cable es muy largo', 'Usamos un LED rojo', 'Apagamos el circuito']),
                        ('En una protoboard, los 5 agujeros de una misma tira corta están…', 'Conectados entre sí',
                         ['Separados', 'Pegados con pegamento', 'Conectados a internet']),
                        ('¿Qué es Arduino?', 'Una placa con un microcontrolador que podemos programar',
                         ['Un videojuego', 'Una batería', 'Un tipo de LED']),
                        ('digitalWrite(8, HIGH) hace que el pin 8…', 'Dé 5 V (encendido)', ['Dé 0 V', 'Lea un sensor', 'Se borre']),
                    ]),
             mision('Planos en papel: dibuja tu circuito', 'evidencia',
                    'Los ingenieros dibujan antes de construir. En tu cuaderno, dibuja con símbolos eléctricos un circuito con:\n\n'
                    '• Una pila\n• Un botón (interruptor)\n• Una resistencia\n• Un LED (marca cuál es su pata + )\n\n'
                    'Usa regla y marca hacia dónde viaja la corriente con flechas. Sube una foto de tu plano.', xp=60, monedas=15),
             mision('Tinkercad: tu primer circuito (sin Arduino)', 'link',
                    'Entra a tu clase de Tinkercad, crea un diseño nuevo de Circuitos y arma:\n\n'
                    '• Un portapilas de 2 pilas AA (3 V) + un botón + una resistencia de 100 Ω + un LED.\n\n'
                    'Inicia la simulación y presiona el botón. Después experimenta:\n'
                    '1. Voltea el LED: ¿enciende?\n2. Cambia la pila por una de 9 V y quita la resistencia: ¿qué te avisa Tinkercad?\n\n'
                    'Sube una captura de tu circuito funcionando.', xp=60, monedas=15, link=TINKERCAD),
             practica('Hola, mundo: el LED que parpadea',
                      'El primer programa de todo inventor. 🌍\n\n'
                      '🔌 Conexiones (en Tinkercad): pin 8 → resistencia 220 Ω → pata larga del LED; pata corta → GND.\n\n'
                      '💻 Cambia el editor de bloques a "Texto", copia el código y presiona "Iniciar simulación".\n\n'
                      '🧠 delay(500) espera medio segundo. ¿Qué pasa si pones 100? ¿Y 2000?\n\n'
                      '🏆 Reto: haz que el LED diga SOS en código Morse: 3 cortos, 3 largos, 3 cortos.',
                      COD_PARPADEO, xp=60, monedas=15, link=TINKERCAD),
         ]},
         {'nombre': 'Día 2: simulador en acción', 'cofre': 30, 'misiones': [
             practica('Semáforo', 'Programa el semáforo de la esquina de tu escuela. 🚦\n\n'
                      '🔌 Conexiones: LED verde → pin 2 · amarillo → pin 3 · rojo → pin 4. Cada uno con su resistencia de 220 Ω a GND.\n\n'
                      '🧠 El ciclo for repite el parpadeo del amarillo 3 veces sin escribirlo 3 veces.\n\n'
                      '🏆 Reto: agrega un segundo semáforo para la calle de enfrente (cuando uno está en verde, el otro está en rojo).',
                      COD_SEMAFORO, link=TINKERCAD),
             practica('Botón mágico: enciende y apaga', 'Un botón que funciona como el apagador de tu cuarto. 💡\n\n'
                      '🔌 Conexiones: botón → una pata al pin 2 y la pata contraria (en diagonal) a GND · LED → pin 8 con 220 Ω.\n\n'
                      '🧠 INPUT_PULLUP usa una resistencia escondida dentro del Arduino: el botón suelto lee HIGH y presionado lee LOW.\n'
                      'Abre el Monitor serie para ver los mensajes.\n\n'
                      '🏆 Reto: cuenta cuántas veces se presionó el botón y muéstralo en el monitor serie.',
                      COD_BOTON, link=TINKERCAD),
             practica('Dimmer con potenciómetro', 'Controla el brillo de un LED como una perilla de luz. 🎚️\n\n'
                      '🔌 Conexiones: potenciómetro → patas de los lados a 5V y GND, pata central a A0 · LED → pin 9 (tiene ~) con 220 Ω.\n\n'
                      '🧠 analogRead da números de 0 a 1023 y analogWrite usa de 0 a 255: la función map() hace la conversión.\n\n'
                      '🏆 Reto: si el potenciómetro pasa de 900, que el LED parpadee como alerta.',
                      COD_DIMMER, link=TINKERCAD),
             practica('Melodía con buzzer', 'Tu Arduino también es músico. 🎵\n\n'
                      '🔌 Conexiones: Piezo (buzzer) → + al pin 8 y − a GND.\n\n'
                      '🧠 tone(pin, frecuencia, duración) toca una nota. Entre más alta la frecuencia, más aguda la nota.\n\n'
                      '🏆 Reto: programa otra canción que te sepas (por ejemplo, "Las mañanitas" o "Cumpleaños feliz").',
                      COD_MELODIA, link=TINKERCAD),
             jefe('Jefe: El Guardián del Simulador',
                  '🔐 El Guardián solo deja pasar a quien construya una caja fuerte de 3 botones.\n\n'
                  '🔌 Conexiones: botones en los pines 2, 3 y 4 (cada uno a GND) · LED verde → 8 · LED rojo → 9 · Piezo → 10.\n\n'
                  '🧠 La combinación secreta está guardada en un arreglo: CLAVE[] = {1, 3, 2, 1}. Cada botón presionado se '
                  'guarda en intento[] y al llegar a 4 se comparan uno por uno.\n\n'
                  '🏆 Reto: cambia la clave por una de 6 botones y agrega un tercer LED que parpadee mientras escribes.',
                  COD_CAJA_FUERTE, link=TINKERCAD),
         ]},
     ]},

    # ---------- Llega el kit ----------
    {'nombre': 'Estación Polar del Kit', 'tema': 'hielo',
     'descripcion': '¡Llegó el kit! Conoce cada pieza, aprende a cuidarla y pasa del simulador a los circuitos de verdad.',
     'niveles': [
         {'nombre': '¡Llegó el kit!', 'cofre': 25, 'misiones': [
             mision('Inventario del explorador', 'presencial',
                    '🧰 Abre tu kit con cuidado y revisa que esté todo con la lista.\n\n'
                    '1. Separa las piezas en grupos: sensores, motores, pantallas, componentes pequeños y cables.\n'
                    '2. Guarda las resistencias por valor (puedes usar bolsitas con etiqueta).\n'
                    '3. Escribe tu nombre en la caja.\n\n'
                    '⚠️ Reglas del inventor:\n• Desconecta el USB antes de mover cables.\n'
                    '• Nunca conectes 5V directo a GND.\n• Los motores toman energía del módulo de alimentación, no de un pin.\n'
                    '• El lector RFID usa 3.3 V, nunca 5 V.', xp=40, monedas=10),
             mision('Detective del kit: ¿sensor, actuador o pantalla?', 'juego',
                    'Clasifica las piezas de tu kit: ¿sienten algo, hacen algo o muestran información?', juego='clasifica_kit'),
             practica('¡Hola, placa real!', 'Tu primera vez subiendo un programa a la placa de verdad. 🎉\n\n'
                      '1. Conecta la placa con el cable USB.\n2. En Arduino IDE elige Herramientas → Placa → "Arduino Uno" y el Puerto (COM) que aparezca.\n'
                      '3. Copia el código y presiona la flecha → (Subir).\n4. Abre el Monitor serie (lupa de arriba a la derecha) a 9600.\n\n'
                      '💡 Si la computadora no encuentra la placa, avísale a tu profe: algunas placas compatibles necesitan el driver CH340.\n\n'
                      '🏆 Reto: cambia el mensaje por tu nombre y haz que el LED parpadee tantas veces como tu edad.',
                      COD_HOLA_PLACA, xp=50, monedas=15),
             mision('El código de colores de las resistencias', 'evidencia',
                    '🌈 Las resistencias no traen el número escrito: lo dicen con bandas de colores.\n\n'
                    'Negro 0 · Café 1 · Rojo 2 · Naranja 3 · Amarillo 4 · Verde 5 · Azul 6 · Violeta 7 · Gris 8 · Blanco 9\n'
                    'Las dos primeras bandas son números y la tercera dice cuántos ceros agregar.\n'
                    'Ejemplo: rojo-rojo-café = 2, 2 y un cero = 220 Ω.\n\n'
                    'Encuentra en tu kit una de 220 Ω, una de 1 kΩ y una de 10 kΩ, pégalas en una hoja con su valor y sube la foto.',
                    xp=60, monedas=15),
             mision('El kit al derecho y al revés', 'cuestionario', '¿Ya conoces tu kit? Demuéstralo.', xp=60, monedas=15, preguntas=[
                 ('¿Cuáles son los colores de una resistencia de 220 Ω?', 'Rojo, rojo, café',
                  ['Café, negro, naranja', 'Café, negro, rojo', 'Naranja, naranja, café']),
                 ('¿Cuáles son los colores de una resistencia de 10 kΩ?', 'Café, negro, naranja',
                  ['Rojo, rojo, café', 'Café, negro, rojo', 'Amarillo, violeta, rojo']),
                 ('¿A qué voltaje se conecta el lector RFID RC522?', '3.3 V', ['5 V', '9 V', '12 V']),
                 ('Antes de cambiar cables en tu circuito debes…', 'Desconectar el cable USB',
                  ['Mojar la placa', 'Subir el volumen', 'Nada']),
                 ('Los motores deben tomar energía de…', 'El módulo de alimentación, no directo de un pin',
                  ['Un pin digital directamente', 'El cargador del celular', 'Una pila de reloj']),
                 ('Los pines A0 a A5 sirven para leer señales…', 'Analógicas, de 0 a 1023',
                  ['Solo de internet', 'Solo de colores', 'Solo de 0 y 1']),
                 ('Los pines con ~ (3, 5, 6, 9, 10 y 11) pueden…', 'Hacer PWM: brillo o velocidad variable',
                  ['Medir temperatura', 'Conectarse a wifi', 'Dar 12 V']),
                 ('¿Cuál de estos es un sensor?', 'El sensor ultrasónico', ['El servomotor', 'El zumbador', 'La pantalla LCD']),
             ]),
         ]},
         {'nombre': 'Primeros circuitos reales', 'cofre': 30, 'misiones': [
             practica('Semáforo con botón peatonal', 'El semáforo de Tinkercad, ahora de verdad… ¡y con botón para peatones! 🚶\n\n'
                      '🔌 Conexiones:\n• Autos: verde → 2 · amarillo → 3 · rojo → 4\n• Peatón: verde → 5 · rojo → 6\n'
                      '• Cada LED con 220 Ω a GND · Botón → pin 7 y GND · Zumbador activo → + al pin 8, − a GND\n\n'
                      '🧠 Los pitidos ayudan a las personas que no pueden ver el semáforo.\n\n'
                      '🏆 Reto: que el semáforo no haga caso al botón si alguien lo presionó hace menos de 10 segundos.',
                      COD_SEMAFORO_PEATONAL),
             practica('Luz nocturna automática', 'Una lámpara que se enciende sola cuando oscurece. 🌙\n\n'
                      '🔌 Conexiones: fotoresistencia → una pata a 5V y la otra a A0 · resistencia de 10 kΩ de A0 a GND · LED → pin 9 con 220 Ω.\n\n'
                      '🧠 Abre el monitor serie, tapa la fotoresistencia con tu mano y anota los números con luz y sin luz. '
                      'Ajusta el umbral con esos números.\n\n'
                      '🏆 Reto: en vez de encender o apagar, que el LED brille más entre más oscuro esté (usa map y analogWrite).',
                      COD_LUZ_NOCTURNA),
             practica('Alarma anti-robo de mochila', '¿Alguien movió tu mochila? ¡Ahora lo sabrás! 🎒\n\n'
                      '🔌 Conexiones: interruptor de inclinación → una pata al pin 2 y la otra a GND · zumbador activo → pin 8 · LED rojo → pin 9 con 220 Ω.\n\n'
                      '🧠 Dentro del interruptor hay una bolita metálica: de pie cierra el circuito y al inclinarlo lo abre. '
                      'Si tu alarma suena al revés, cambia HIGH por LOW en el if.\n\n'
                      '🏆 Reto: agrega un botón para "armar" y "desarmar" la alarma.',
                      COD_MOCHILA),
         ]},
         {'nombre': 'El iglú del jefe', 'cofre': 40, 'misiones': [
             jefe('Jefe: El Yeti de la Oscuridad',
                  '🥶 El Yeti apagó todas las luces del polo. Construye una lámpara inteligente con 3 modos que se cambian con un botón:\n'
                  '0 = apagada · 1 = automática (brilla más entre más oscuro esté) · 2 = arcoíris.\n\n'
                  '🔌 Conexiones: botón → pin 2 y GND · LED RGB → rojo 9, verde 10, azul 11 (220 Ω cada uno), pata larga a GND · '
                  'fotoresistencia → 5V y A0, con 10 kΩ de A0 a GND.\n\n'
                  '🧠 La operación % (módulo) hace que el modo regrese a 0 después del 2.\n\n'
                  '🏆 Reto: agrega un cuarto modo "fiesta" que cambie de color al azar cada 200 ms.',
                  COD_LAMPARA),
         ]},
     ]},

    # ---------- Luces y pantallas ----------
    {'nombre': 'Ciudad de las Mil Luces', 'tema': 'ciudad',
     'descripcion': 'Colores, números y dibujos hechos de luz: LED RGB, display de 7 segmentos, el chip 74HC595 y la matriz de 8×8.',
     'niveles': [
         {'nombre': 'Colores y números', 'cofre': 25, 'misiones': [
             practica('Paleta de colores RGB', 'Un solo LED que puede ser de casi cualquier color. 🎨\n\n'
                      '🔌 Conexiones: LED RGB → pata más larga a GND · rojo → 9 · verde → 10 · azul → 11 (220 Ω cada uno).\n\n'
                      '🧠 Mezclando rojo, verde y azul con distinta fuerza (0 a 255) se forman los demás colores.\n\n'
                      '🏆 Reto: inventa 3 colores nuevos con su nombre (por ejemplo, "verde limón") y agrégalos a la lista.',
                      COD_PALETA_RGB),
             practica('Mezclador de colores', 'Tú eliges el color con dos perillas y un botón. 🎛️\n\n'
                      '🔌 Conexiones: potenciómetro 1 → centro a A0 · potenciómetro 2 → centro a A1 (patas de los lados a 5V y GND) · '
                      'botón → pin 2 y GND · LED RGB → 9, 10 y 11 con 220 Ω.\n\n'
                      '🏆 Reto: que el monitor serie diga el nombre del color cuando reconozca uno (por ejemplo, rojo + azul = "Morado").',
                      COD_MEZCLADOR),
             practica('Dado electrónico', 'Un dado que nunca se pierde debajo del sillón. 🎲\n\n'
                      '🔌 Conexiones: display de 7 segmentos (1 dígito) → segmentos a, b, c, d, e, f, g a los pines 2 a 8 (220 Ω cada uno) · '
                      'pin común a GND · botón → pin 10 y GND.\n\n'
                      '📍 Pines del display (de frente, con el punto abajo a la derecha): abajo, de izquierda a derecha: e, d, común, c, punto · '
                      'arriba, de derecha a izquierda: b, a, común, f, g.\n\n'
                      '🧠 La tabla NUMEROS dice qué segmentos se encienden para dibujar cada número.\n\n'
                      '🏆 Reto: agrega un buzzer pasivo que haga "tic" cada vez que el dado cambia de número.',
                      COD_DADO),
         ]},
         {'nombre': 'Más luces con menos cables', 'cofre': 30, 'misiones': [
             practica('74HC595: 8 LEDs con 3 cables', 'Un chip que convierte 3 cables en 8 salidas. 🧩\n\n'
                      '🔌 Conexiones del 74HC595 (con la muesca a la izquierda, el pin 1 es el de abajo a la izquierda; '
                      'se cuentan hacia la derecha hasta el 8 y regresan por arriba del 9 al 16):\n'
                      '• pin 14 → Arduino 4 · pin 12 → Arduino 5 · pin 11 → Arduino 6\n'
                      '• pin 16 y pin 10 → 5V · pin 8 y pin 13 → GND\n'
                      '• Salidas: pin 15 y pines 1 a 7 → 220 Ω → LED → GND\n\n'
                      '🧠 shiftOut manda los 8 bits uno tras otro. Mira el monitor serie: ¡es el número en binario!\n\n'
                      '🏆 Reto: haz una barra que se llene de izquierda a derecha y se vacíe.',
                      COD_74HC595, xp=80),
             mision('Binario y registros', 'cuestionario', 'El idioma secreto de las computadoras: ceros y unos.', xp=60, monedas=15,
                    preguntas=[
                        ('¿Cuántos valores puede tener un bit?', 'Dos: 0 y 1', ['Diez', 'Uno', 'Infinitos']),
                        ('8 bits juntos forman un…', 'Byte', ['Kilo', 'Pixel', 'Volt']),
                        ('¿Qué número es 00000101 en binario?', '5', ['101', '2', '11']),
                        ('Con 8 LEDs (8 bits), ¿hasta qué número puedes contar?', '255', ['8', '100', '1023']),
                        ('El chip 74HC595 sirve para…', 'Controlar 8 salidas con solo 3 pines del Arduino',
                         ['Medir la temperatura', 'Guardar música', 'Dar más voltaje']),
                        ('El pin "candado" (latch) del 74HC595 hace que…', 'Los 8 LEDs cambien al mismo tiempo',
                         ['Los LEDs se apaguen para siempre', 'El chip se caliente', 'El Arduino se reinicie']),
                        ('analogWrite(9, 255) hace que el LED brille…', 'Al máximo', ['Al mínimo', 'A la mitad', 'Rojo']),
                        ('Un display de 7 segmentos de cátodo común conecta su pin común a…', 'GND', ['5V', 'A0', 'El pin 13']),
                    ]),
             practica('Matriz 8×8: caritas', 'Dibuja con luz en una matriz de 64 LEDs. 😀\n\n'
                      '📚 Instala la librería "LedControl" (Herramientas → Administrar bibliotecas).\n\n'
                      '🔌 Conexiones del módulo MAX7219: VCC → 5V · GND → GND · DIN → 12 · CLK → 11 · CS → 10.\n\n'
                      '🧠 Cada renglón del dibujo es un byte: B00111100 enciende los 4 LEDs del centro.\n\n'
                      '🏆 Reto: agrega una carita sorprendida y una que guiña el ojo.',
                      COD_MATRIZ_CARITAS),
             practica('Matriz 8×8: tu propia animación', 'Haz tu propio personaje animado, como en los videojuegos clásicos. 👾\n\n'
                      '🔌 Mismas conexiones que en la práctica de las caritas.\n\n'
                      '✏️ Antes de programar: dibuja una cuadrícula de 8×8 en tu cuaderno, pinta tu personaje y escribe cada renglón con 1 y 0.\n\n'
                      '🏆 Reto: crea una animación de al menos 3 cuadros (un personaje que camina, un corazón que late, una flecha que se mueve…) '
                      'y sube una foto de tu cuadrícula junto a la matriz.',
                      COD_MATRIZ_ANIMACION, xp=80),
         ]},
         {'nombre': 'La torre del jefe', 'cofre': 40, 'misiones': [
             jefe('Jefe: El Apagón de la Ciudad Neón',
                  '🌃 ¡Se fue la luz y los peatones no pueden cruzar! Construye un semáforo peatonal con cuenta regresiva de 9 a 0.\n\n'
                  '🔌 Conexiones: display de 7 segmentos → a..g a los pines 2..8 (220 Ω), común a GND · '
                  'LEDs con 220 Ω: verde autos 9 · rojo autos 10 · verde peatón 11 · botón → A0 y GND · zumbador activo → 12.\n\n'
                  '🧠 Los pines analógicos (A0 a A5) también funcionan como pines digitales.\n\n'
                  '🏆 Reto: que el amarillo de los autos parpadee antes del rojo y que la cuenta sea de 15 segundos '
                  '(pista: muestra solo las unidades o haz parpadear el punto).',
                  COD_CUENTA_REGRESIVA),
         ]},
     ]},

    # ---------- Sensores del ambiente ----------
    {'nombre': 'Océano de los Sensores', 'tema': 'oceano',
     'descripcion': 'Temperatura, humedad, sonido y agua: aprende a medir el mundo y a convertir números en decisiones.',
     'niveles': [
         {'nombre': 'Sentidos electrónicos', 'cofre': 25, 'misiones': [
             practica('Termómetro de colores', 'Mide la temperatura con un termistor y muéstrala con colores. 🌡️\n\n'
                      '🔌 Conexiones: 5V → termistor → A0 → resistencia de 10 kΩ → GND · LED RGB → 9, 10 y 11 con 220 Ω.\n\n'
                      '🧠 El termistor cambia su resistencia con el calor; la fórmula la convierte en grados Celsius.\n'
                      'Prueba: toma el termistor entre tus dedos. ¿Cuánto sube?\n\n'
                      '🏆 Reto: muestra la temperatura en grados Fahrenheit también (°F = °C × 1.8 + 32).',
                      COD_TERMISTOR),
             practica('Estación del clima: DHT11 + LCD', 'Temperatura y humedad del salón en una pantalla. ⛅\n\n'
                      '📚 Instala "DHT sensor library" de Adafruit (acepta instalar también "Adafruit Unified Sensor").\n\n'
                      '🔌 Conexiones:\n• DHT11: S → 2 · + → 5V · − → GND\n'
                      '• LCD: RS → 7 · E → 8 · D4 → 9 · D5 → 10 · D6 → 11 · D7 → 12\n'
                      '• LCD: VSS y RW → GND · VDD → 5V · V0 → pata central de un potenciómetro · A → 220 Ω → 5V · K → GND\n\n'
                      '💡 Si la pantalla se ve vacía o con cuadritos, gira el potenciómetro (contraste).\n\n'
                      '🏆 Reto: si la humedad pasa de 70 %, que la pantalla diga "Lleva paraguas".',
                      COD_DHT_LCD, xp=90, monedas=25),
             practica('Interruptor de aplausos', '👏👏 ¡Enciende la luz con un aplauso!\n\n'
                      '🔌 Conexiones: sensor de sonido → + a 5V · G a GND · AO a A0 · DO al pin 2 · LED → pin 9 con 220 Ω.\n\n'
                      '🔧 Gira el tornillito azul del sensor hasta que su LED se apague en silencio y parpadee al aplaudir. '
                      'Si funciona al revés, cambia HIGH por LOW.\n\n'
                      '🧠 Abre Herramientas → Serial Plotter: ¡verás tu aplauso como una montaña en la gráfica!\n\n'
                      '🏆 Reto: que la luz solo cambie con DOS aplausos seguidos.',
                      COD_APLAUSOS),
         ]},
         {'nombre': 'Agua y tierra', 'cofre': 30, 'misiones': [
             practica('Alarma de inundación', 'Avisa antes de que se inunde el cuarto de máquinas. 🌊\n\n'
                      '🔌 Conexiones: sensor de nivel de agua → S a A0 · + al pin 7 · − a GND · '
                      'LEDs con 220 Ω: verde 9 · amarillo 10 · rojo 11 · zumbador activo → 8.\n\n'
                      '⚠️ Mete al agua solo la parte con rayitas del sensor. Nunca mojes la placa ni los cables.\n\n'
                      '🧠 Encendemos el sensor solo al medir (pin 7) para que sus pistas no se oxiden.\n\n'
                      '🏆 Reto: calibra los números 200 y 450 con un vaso de agua y escribe en el comentario los valores que encontraste.',
                      COD_INUNDACION),
             practica('Maceta inteligente', 'Una maceta que levanta su bandera cuando tiene sed. 🌱\n\n'
                      '🔌 Conexiones: sensor de humedad del suelo → VCC al pin 7 · GND · AO a A0 · '
                      'servo SG90 → café a GND, rojo a 5V, naranja al pin 9 · LED rojo → pin 12 con 220 Ω.\n\n'
                      '🔧 Calibra: anota lo que marca el monitor serie con tierra seca y con tierra mojada, y cambia SECO y MOJADO.\n\n'
                      '🏆 Reto: agrega un buzzer pasivo que toque una melodía corta cuando la planta ya fue regada.',
                      COD_MACETA, xp=80),
             mision('Sensores bajo la lupa', 'cuestionario', '¿Ya piensas como ingeniero de sensores?', xp=60, monedas=15, preguntas=[
                 ('analogRead() regresa un número entre…', '0 y 1023', ['0 y 1', '0 y 255', '1 y 100']),
                 ('El DHT11 mide…', 'La temperatura y la humedad del aire', ['La distancia', 'La luz', 'El sonido']),
                 ('El sensor ultrasónico calcula la distancia con…', 'El tiempo que tarda en regresar el eco',
                  ['Una cámara', 'Un imán', 'El color del objeto']),
                 ('Un termistor cambia su…', 'Resistencia cuando cambia la temperatura',
                  ['Color con la luz', 'Forma con el sonido', 'Peso con el agua']),
                 ('Con mucha luz, una fotoresistencia tiene…', 'Menos resistencia',
                  ['Más resistencia', 'Siempre la misma resistencia', 'Agua']),
                 ('¿Para qué sirve el Serial Plotter?', 'Para ver los datos de un sensor como gráfica',
                  ['Para dibujar en Paint', 'Para borrar el programa', 'Para cargar la batería']),
                 ('¿Por qué encendemos el sensor de agua solo al medir?', 'Para que sus pistas no se oxiden tan rápido',
                  ['Para que mida más agua', 'Para gastar más energía', 'Para que suene']),
                 ('Si un sensor marca números distintos en cada lugar, debemos…', 'Calibrarlo: medir y ajustar los umbrales',
                  ['Tirarlo', 'Ignorar los números', 'Cambiar de placa']),
             ]),
         ]},
         {'nombre': 'La fosa del Kraken', 'cofre': 40, 'misiones': [
             jefe('Jefe: El Kraken del Clima',
                  '🐙 El Kraken desordenó el clima. Construye una estación meteorológica que muestre, una tras otra, '
                  'la temperatura, la humedad y la luz, y que suene una alarma si hace mucho calor.\n\n'
                  '🔌 Conexiones: DHT11 → 2 · LCD igual que en la estación del clima (7 a 12) · '
                  'fotoresistencia → 5V y A0 con 10 kΩ a GND · zumbador activo → 3.\n\n'
                  '🧠 Usamos millis() en vez de delay() para que el Arduino nunca se quede "congelado" esperando.\n\n'
                  '🏆 Reto: agrega una cuarta pantalla con la temperatura más alta del día.',
                  COD_ESTACION, xp=160),
         ]},
     ]},

    # ---------- Motores ----------
    {'nombre': 'Fragua de los Motores', 'tema': 'volcan',
     'descripcion': 'Servos, motores paso a paso y motores de corriente directa: ¡es hora de que tus inventos se muevan!',
     'niveles': [
         {'nombre': 'Servos con sentido', 'cofre': 25, 'misiones': [
             practica('Barrera de estacionamiento', 'La pluma se levanta sola cuando llega un auto. 🚗\n\n'
                      '🔌 Conexiones: sensor ultrasónico → VCC 5V · Trig 7 · Echo 6 · GND · '
                      'servo SG90 → café GND, rojo 5V, naranja 9 · LED rojo → 12 · LED verde → 13 (220 Ω).\n\n'
                      '🧠 El sensor grita con ultrasonido y mide cuánto tarda el eco. El for mueve el servo de 2 en 2 grados para que suba despacito.\n\n'
                      '💡 Si la placa se reinicia cuando se mueve el servo, aliméntalo con el módulo de alimentación.\n\n'
                      '🏆 Reto: cuenta cuántos autos han entrado y muéstralo en el monitor serie.',
                      COD_BARRERA, xp=80),
             practica('Joystick: control total', 'Un joystick como el de los videojuegos para controlar tu invento. 🕹️\n\n'
                      '🔌 Conexiones: joystick → GND · +5V · VRx a A0 · VRy a A1 · SW al pin 2 · '
                      'servo → naranja al 9 · LED → pin 5 con 220 Ω · zumbador activo → 8.\n\n'
                      '🧠 Cada eje del joystick es un potenciómetro: en el centro marca cerca de 512.\n\n'
                      '🏆 Reto: que el servo regrese solito al centro (90°) cuando sueltas el joystick.',
                      COD_JOYSTICK),
         ]},
         {'nombre': 'Motores que giran', 'cofre': 30, 'misiones': [
             practica('Plato giratorio 360°', 'Un plato que gira en paradas exactas para tomar fotos de tus inventos. 📸\n\n'
                      '🔌 Conexiones: placa ULN2003 → IN1 8 · IN2 9 · IN3 10 · IN4 11 · + y − al módulo de alimentación (5V) · '
                      'une el GND del módulo con el GND del Arduino · conecta el motor a la placa ULN2003 · botón → pin 2 y GND.\n\n'
                      '🧠 Este motor da 2048 pasos por vuelta: 2048 / 8 = 256 pasos son 45°.\n\n'
                      '🏆 Reto: que gire una vuelta completa hacia un lado y luego regrese (usa un número negativo en step).',
                      COD_PASO_A_PASO, xp=80),
             practica('Ventilador con L293D', 'Un ventilador con 3 velocidades y reversa. 🌀\n\n'
                      '🔌 Conexiones del chip L293D (muesca hacia arriba; los pines se cuentan desde la muesca, bajando por la izquierda):\n'
                      '• 1 → Arduino 5 · 2 → Arduino 4 · 7 → Arduino 3\n• 3 y 6 → los dos cables del motor de 3 V\n'
                      '• 4, 5, 12 y 13 → GND · 16 → 5V del Arduino · 8 → 5V del módulo de alimentación\n'
                      '• Botón de velocidad → pin 7 · botón de dirección → pin 8 (ambos a GND) · une todos los GND\n\n'
                      '🧠 El L293D es un "puente H": cambiando qué entrada está en HIGH, el motor gira hacia un lado o hacia el otro.\n\n'
                      '🏆 Reto: agrega un potenciómetro para elegir cualquier velocidad, no solo 3.',
                      COD_VENTILADOR, xp=90, monedas=25),
             mision('Engranes de cartón', 'presencial',
                    '⚙️ Sin kit: mecánica con las manos.\n\n'
                    '1. Recorta dos engranes de cartón: uno grande (24 dientes) y uno chico (12 dientes).\n'
                    '2. Clávalos con tachuelas sobre un cartón para que sus dientes encajen.\n'
                    '3. Gira el chico una vuelta: ¿cuánto gira el grande? ¿Hacia qué lado?\n\n'
                    '🧠 Así funcionan las cajas de engranes: el motor paso a paso trae una adentro para ganar fuerza.\n'
                    'Explícale a tu profe qué descubriste.', xp=50, monedas=15),
         ]},
         {'nombre': 'El taller del gólem', 'cofre': 40, 'misiones': [
             jefe('Jefe: El Gólem de Engranes',
                  '🏗️ Construye una grúa robótica: la base gira con el motor paso a paso, el brazo sube y baja con el servo '
                  'y el botón del joystick abre y cierra el gancho.\n\n'
                  '🔌 Conexiones: ULN2003 → 8, 9, 10, 11 (energía del módulo de alimentación) · servo → naranja al 6 · '
                  'joystick → VRx A0 · VRy A1 · SW 2 · LED del gancho → 13.\n\n'
                  '✂️ Arma la estructura de la grúa con cartón, palitos o tapas. El motor paso a paso es la base y el servo, el brazo.\n\n'
                  '🏆 Reto: agrega un zumbador que pite mientras la base gira, como las grúas de verdad.',
                  COD_GRUA, xp=170, monedas=55),
         ]},
     ]},

    # ---------- Seguridad y comunicación ----------
    {'nombre': 'Pirámide de los Secretos', 'tema': 'desierto',
     'descripcion': 'Teclados, controles remotos, tarjetas RFID y sensores de movimiento: protege los tesoros de la pirámide.',
     'niveles': [
         {'nombre': 'Códigos y controles', 'cofre': 25, 'misiones': [
             practica('Teclado 4×4: ¿qué tecla presioné?', 'El teclado de los cajeros y las alarmas. 🔢\n\n'
                      '📚 Instala la librería "Keypad" (de Mark Stanley y Alexander Brevig).\n\n'
                      '🔌 Conexiones: los 8 cables del teclado, de izquierda a derecha, a los pines 9, 8, 7, 6, 5, 4, 3, 2 · zumbador activo → 10.\n\n'
                      '🧠 Son 16 teclas con solo 8 cables: 4 filas y 4 columnas. El Arduino revisa cuál fila y cuál columna se tocan.\n\n'
                      '🏆 Reto: que cada tecla haga un pitido de duración diferente.',
                      COD_TECLADO, xp=60, monedas=15),
             practica('Cerradura con contraseña', 'Una cerradura de verdad: escribe la clave y el servo abre. 🔐\n\n'
                      '🔌 Conexiones: teclado igual que antes (9 a 2) · servo → naranja al 11 · LED verde → 12 · LED rojo → 13 (220 Ω) · zumbador activo → 10.\n\n'
                      '🧠 Las teclas se van juntando en el texto "escrito". # revisa la clave y * la borra.\n\n'
                      '🏆 Reto: después de 3 intentos fallidos, que la cerradura se bloquee 30 segundos.',
                      COD_CERRADURA, xp=80),
             practica('Control remoto: descubre los códigos', 'Cada botón del control manda un código invisible. 📡\n\n'
                      '📚 Instala la librería "IRremote" (versión 4 o más nueva).\n\n'
                      '🔌 Conexiones del receptor infrarrojo: S → 11 · + (centro) → 5V · − → GND.\n\n'
                      '🧠 Apunta el control y presiona botones: anota en tu cuaderno el código de cada uno (lo vas a necesitar).\n'
                      '📱 Truco: mira el foco del control con la cámara de un celular mientras presionas: ¡verás la luz infrarroja!\n\n'
                      '🏆 Reto: escribe en el comentario los códigos de los botones 0 al 9.',
                      COD_IR_CODIGOS, xp=60, monedas=15),
             practica('Control remoto: luces de la pirámide', 'Enciende y apaga luces desde lejos. 🔦\n\n'
                      '🔌 Conexiones: receptor IR → S al 11 · LEDs con 220 Ω: rojo → 4 · verde → 5 · azul → 6.\n\n'
                      '🧠 Si tu control dio otros códigos en la práctica anterior, cámbialos en BOTON_0 a BOTON_3.\n\n'
                      '🏆 Reto: que los botones + y − suban y bajen el brillo de los LEDs (usa analogWrite).',
                      COD_IR_LUCES),
         ]},
         {'nombre': 'Guardianes de la cámara', 'cofre': 30, 'misiones': [
             practica('Alarma de intrusos con PIR', 'Un sensor que detecta el calor de las personas en movimiento. 🚨\n\n'
                      '🔌 Conexiones: PIR HC-SR501 → VCC 5V · OUT 2 · GND · LED rojo → 12 con 220 Ω · zumbador activo → 8.\n\n'
                      '🧠 Al encenderlo tarda 1 minuto en calibrarse. Sus dos perillas ajustan la sensibilidad y cuánto dura la señal.\n\n'
                      '🏆 Reto: que la alarma solo funcione cuando está oscuro (agrega la fotoresistencia).',
                      COD_PIR),
             practica('RFID: tarjetas mágicas', 'Lee el número secreto de tu tarjeta o llavero. 💳\n\n'
                      '📚 Instala la librería "MFRC522".\n\n'
                      '🔌 Conexiones del lector RC522: SDA → 10 · SCK → 13 · MOSI → 11 · MISO → 12 · RST → 9 · GND → GND · '
                      '3.3V → 3.3V  ⚠️ ¡NUNCA a 5V!\n\n'
                      '🧠 Cada tarjeta tiene un número único (UID). Cópialo del monitor serie: lo necesitas en la siguiente práctica.\n\n'
                      '🏆 Reto: escribe el UID de tu tarjeta y el de tu llavero en el comentario.',
                      COD_RFID_LEER, xp=60, monedas=15),
             practica('RFID: acceso autorizado', 'Solo TU tarjeta abre la puerta. 🚪\n\n'
                      '🔌 Conexiones: RC522 igual que antes (¡3.3 V!) · servo → naranja al 6 · LED verde → 4 · LED rojo → 5 (220 Ω) · zumbador activo → 8.\n\n'
                      '🧠 Cambia {0xDE, 0xAD, 0xBE, 0xEF} por el UID de tu tarjeta. La función esAutorizada() lo compara byte por byte.\n\n'
                      '🏆 Reto: autoriza dos tarjetas (la tuya y la de un compañero) y que el monitor diga el nombre de quién entró.',
                      COD_RFID_ACCESO, xp=80),
             mision('Seguridad electrónica', 'cuestionario', '¿Podrías diseñar la seguridad de un banco?', xp=60, monedas=15, preguntas=[
                 ('RFID significa identificación por…', 'Radiofrecuencia', ['Rayos X', 'Huella digital', 'Contraseña']),
                 ('El sensor PIR detecta…', 'El calor (infrarrojo) de un cuerpo en movimiento',
                  ['El color de la ropa', 'El ruido', 'La humedad']),
                 ('La luz del control remoto es infrarroja. Nuestros ojos…', 'No la ven, pero la cámara de un celular sí',
                  ['La ven roja', 'La ven azul', 'La escuchan']),
                 ('Un teclado 4×4 tiene 16 teclas pero solo 8 cables porque…', 'Se organiza en 4 filas y 4 columnas',
                  ['Tiene wifi', 'Solo funcionan 8 teclas', 'Usa pilas']),
                 ('Una buena clave para tu bóveda es…', 'Difícil de adivinar y secreta',
                  ['1234', 'Tu cumpleaños pegado en la caja', '0000']),
                 ('En el UID de una tarjeta, «0xA3» es un número escrito en…', 'Hexadecimal', ['Romano', 'Morse', 'Braille']),
                 ('Un sistema de doble seguridad pide…', 'Dos pruebas distintas, como tarjeta y clave',
                  ['Dos tarjetas iguales', 'Gritar dos veces', 'Nada']),
                 ('Al encender el PIR hay que esperar cerca de un minuto porque…', 'Se está calibrando',
                  ['Se descarga de internet', 'Está dormido para siempre', 'Debe llegar a 100 °C']),
             ]),
         ]},
         {'nombre': 'La cámara del faraón', 'cofre': 40, 'misiones': [
             jefe('Jefe: La Esfinge del Desierto',
                  '🗝️ La Esfinge solo abre la bóveda con DOBLE seguridad: primero tu tarjeta RFID y después la clave en el teclado '
                  '(tienes 15 segundos).\n\n'
                  '🔌 Conexiones:\n• RC522 (¡3.3 V!): SDA 10 · SCK 13 · MOSI 11 · MISO 12 · RST 9\n'
                  '• Teclado: filas → 2, 3, 4, 5 · columnas → 6, 7, 8, A0\n'
                  '• Servo → naranja a A1 · zumbador activo → A2 · LED verde → A3 · LED rojo → A4 (220 Ω)\n\n'
                  '🧠 El programa tiene dos "estados": esperando tarjeta y esperando clave. La variable tarjetaOk dice en cuál está.\n\n'
                  '🏆 Reto: agrega un tercer paso: que también haya que presionar un botón escondido.',
                  COD_BOVEDA, xp=180, monedas=60),
         ]},
     ]},

    # ---------- Tiempo y juegos ----------
    {'nombre': 'Taller del Tiempo y los Juegos', 'tema': 'dulces',
     'descripcion': 'Relojes, alarmas, cronómetros y videojuegos de verdad hechos con tus propias manos.',
     'niveles': [
         {'nombre': 'El tiempo en tus manos', 'cofre': 25, 'misiones': [
             practica('Reloj de verdad con RTC', 'Un reloj que no se atrasa aunque desconectes la placa. 🕰️\n\n'
                      '📚 Instala la librería "RTClib" (de Adafruit).\n\n'
                      '🔌 Conexiones: RTC → VCC 5V · GND · SDA a A4 · SCL a A5 (con su pila de botón) · LCD igual que antes (7 a 12).\n\n'
                      '⚠️ La primera vez quita las // de la línea rtc.adjust, sube el programa, y luego vuelve a ponerlas y súbelo otra vez.\n'
                      'Si tu módulo dice DS3231, cambia RTC_DS1307 por RTC_DS3231. Si tiene pines CLK, DAT y RST, avísale a tu profe.\n\n'
                      '🏆 Reto: que el reloj muestre la hora en formato de 12 horas con a.m. y p.m.',
                      COD_RELOJ, xp=80),
             practica('Despertador', '¡A levantarse! Tu propio despertador con melodía. ⏰\n\n'
                      '🔌 Conexiones: el circuito del reloj + buzzer pasivo → + al 6, − a GND + botón → pin 2 y GND.\n\n'
                      '🧠 Para probarlo, pon la alarma 2 minutos después de la hora actual.\n\n'
                      '🏆 Reto: agrega un botón de "5 minutos más" que vuelva a sonar después de 5 minutos.',
                      COD_DESPERTADOR, xp=80),
             practica('Cronómetro con millis()', 'Mide en décimas de segundo quién arma más rápido un circuito. ⏱️\n\n'
                      '🔌 Conexiones: LCD igual que antes · botón iniciar/pausar → pin 2 · botón reiniciar → pin 3 (ambos a GND).\n\n'
                      '🧠 millis() cuenta los milisegundos desde que se encendió la placa. Restando dos momentos sabemos cuánto tiempo pasó.\n\n'
                      '🏆 Reto: agrega un botón de "vuelta" que guarde el tiempo de cada vuelta en el monitor serie.',
                      COD_CRONOMETRO),
         ]},
         {'nombre': 'Arcade de verdad', 'cofre': 30, 'misiones': [
             practica('Juego de reflejos', '¿Quién del salón tiene los reflejos más rápidos? ⚡\n\n'
                      '🔌 Conexiones: LED → pin 8 con 220 Ω · botón → pin 2 y GND · buzzer pasivo → 9.\n\n'
                      '🧠 random(2000, 6000) elige una espera sorpresa para que nadie pueda adivinar. ¡Y detecta a los tramposos!\n\n'
                      '🏆 Reto: hazlo para 2 jugadores con 2 botones: gana quien presione primero.',
                      COD_REFLEJOS),
             practica('Simón dice electrónico', 'El clásico juego de memoria de luces y sonidos. 🔴🟢🔵\n\n'
                      '🔌 Conexiones: LEDs con 220 Ω: rojo 2 · verde 3 · azul 4 · botones (a GND): rojo 5 · verde 6 · azul 7 · buzzer pasivo → 8.\n\n'
                      '🧠 La secuencia se guarda en un arreglo y crece una ronda a la vez.\n\n'
                      '🏆 Reto: agrega un cuarto color y que el juego vaya más rápido cada 5 rondas.',
                      COD_SIMON, xp=90, monedas=25),
             practica('Nivel de burbuja digital', 'Inclina la protoboard y mira cómo rueda la "burbuja" de luz. 🫧\n\n'
                      '🔌 Conexiones: GY-521 → VCC 5V · GND · SCL a A5 · SDA a A4 · matriz MAX7219 → DIN 12 · CLK 11 · CS 10.\n\n'
                      '🧠 El GY-521 tiene un acelerómetro: siente hacia dónde jala la gravedad. Lo leemos directo por I2C con la librería Wire.\n\n'
                      '🏆 Reto: que la burbuja sea de 2×2 LEDs y que suene un pitido cuando esté perfectamente al centro.',
                      COD_BURBUJA, xp=90, monedas=25),
             practica('Perilla mágica: codificador rotatorio', 'Una perilla que gira sin fin, como la de los estéreos. 🎚️\n\n'
                      '🔌 Conexiones: codificador → CLK 2 · DT 3 · SW 4 · + a 5V · GND · servo → naranja al 9.\n\n'
                      '🧠 Al girar, CLK y DT cambian en distinto orden según la dirección: así el Arduino sabe hacia dónde giraste.\n\n'
                      '🏆 Reto: que la perilla controle cuántos LEDs se encienden en la barra del 74HC595.',
                      COD_ENCODER),
         ]},
         {'nombre': 'La cocina del jefe', 'cofre': 40, 'misiones': [
             jefe('Jefe: El Glotón de los Segundos',
                  '🍪 El Glotón se come los segundos y nadie sabe cuándo salen las galletas. Construye un temporizador de cocina: '
                  'gira la perilla para elegir los minutos, presiónala para empezar y ¡suena al terminar!\n\n'
                  '🔌 Conexiones: codificador → CLK 2 · DT 3 · SW 4 · LCD → 7 a 12 · buzzer pasivo → 6.\n\n'
                  '🧠 Guardamos la hora en que debe terminar (fin) y cada vuelta del loop calculamos cuánto falta.\n\n'
                  '🏆 Reto: agrega un LED RGB que pase de verde a amarillo a rojo conforme se acaba el tiempo.',
                  COD_TEMPORIZADOR, xp=170, monedas=55),
         ]},
     ]},

    # ---------- Proyecto final ----------
    {'nombre': 'Selva de los Inventores', 'tema': 'bosque',
     'descripcion': 'La gran final: inventa algo que resuelva un problema real, constrúyelo con tu kit y preséntalo en la '
                    'Feria de Inventos.',
     'niveles': [
         {'nombre': 'Idea y plan', 'cofre': 30, 'misiones': [
             mision('Lluvia de ideas: un problema real', 'presencial',
                    '💡 En equipo, busquen un problema de su escuela o de su casa que un invento con Arduino podría resolver.\n\n'
                    'Ejemplos: plantas que se olvidan de regar, la puerta del salón que se queda abierta, el ruido en la biblioteca, '
                    'saber si el bebedero tiene agua…\n\n'
                    '1. Escriban 5 ideas.\n2. Voten la mejor.\n3. Cuéntenle a su profe: ¿qué problema resuelve y quién lo va a usar?',
                    xp=50, monedas=15),
             mision('Plano del invento', 'evidencia',
                    '📐 Antes de construir, planea como ingeniero. En una hoja dibuja:\n\n'
                    '• La lista de piezas del kit que vas a usar (al menos 3).\n'
                    '• El dibujo de las conexiones (qué va a qué pin).\n'
                    '• El diagrama de flujo de tu programa: LEER → DECIDIR → ACTUAR.\n\n'
                    'Sube una foto de tu plano.', xp=80, monedas=20),
             mision('Prototipo de cartón', 'presencial',
                    '📦 Construye la "carcasa" de tu invento con cartón, cajas o material reciclado: '
                    'dónde va la placa, por dónde salen los sensores y cómo se ve por fuera.\n\n'
                    'Un buen diseño también se ve bonito y es fácil de usar.', xp=60, monedas=15),
         ]},
         {'nombre': 'Construcción', 'cofre': 40, 'misiones': [
             practica('Proyecto final: el código base', 'Esta plantilla organiza tu programa en 3 pasos: LEER → DECIDIR → ACTUAR. 🧭\n\n'
                      '1. Copia la plantilla y escribe arriba qué hace tu invento y sus conexiones.\n'
                      '2. Cambia leerSensor() por el sensor de tu proyecto (puedes copiar partes de prácticas anteriores).\n'
                      '3. Cambia hayQueActuar() por tu regla de decisión.\n4. Cambia actuar() por lo que debe hacer tu invento.\n\n'
                      '🏆 Sube una foto de tu invento funcionando y explica en el comentario qué cambiaste de la plantilla.',
                      COD_PLANTILLA, xp=120, monedas=35),
             mision('Bitácora de pruebas', 'evidencia',
                    '🧪 Los inventores prueban, fallan y mejoran. Lleva una bitácora con al menos 3 pruebas:\n\n'
                    '• ¿Qué probaste?\n• ¿Qué pasó?\n• ¿Qué bug encontraste y cómo lo arreglaste?\n\n'
                    'Sube una foto de tu bitácora.', xp=80, monedas=20),
             mision('Gran examen del inventor', 'cuestionario', 'Todo lo que aprendiste en el año, en 8 preguntas.', xp=80, monedas=25,
                    preguntas=[
                        ('¿Qué hace INPUT_PULLUP?', 'Activa una resistencia interna: el botón suelto lee HIGH y presionado LOW',
                         ['Apaga el pin', 'Da 12 V al botón', 'Borra el programa']),
                        ('map(valor, 0, 1023, 0, 255) sirve para…', 'Convertir un rango de números a otro',
                         ['Dibujar un mapa', 'Medir distancias', 'Guardar archivos']),
                        ('¿Qué ventaja tiene millis() sobre delay()?', 'El Arduino puede seguir haciendo otras cosas mientras mide el tiempo',
                         ['Ninguna', 'Hace que el Arduino se apague', 'Solo funciona de noche']),
                        ('Un servo SG90 se mueve entre…', '0 y 180 grados', ['0 y 1023 grados', 'Gira sin parar', '0 y 10 grados']),
                        ('Para cambiar la dirección de giro de un motor de corriente directa usamos…', 'Un puente H como el L293D',
                         ['Una fotoresistencia', 'Un LED', 'El monitor serie']),
                        ('Un motor paso a paso es ideal cuando necesitas…', 'Girar ángulos exactos',
                         ['Hacer ruido', 'Medir la luz', 'Ver la hora']),
                        ('Una pantalla LCD 1602 muestra…', '2 renglones de 16 caracteres', ['16 renglones de 2', 'Videos', 'Fotos a color']),
                        ('Los inventos con sensores siguen el ciclo…', 'Leer (sensor) → decidir (código) → actuar (actuador)',
                         ['Actuar → apagar → dormir', 'Decidir → borrar → repetir', 'Leer → olvidar → esperar']),
                    ]),
         ]},
         {'nombre': 'La gran feria', 'cofre': 60, 'misiones': [
             jefe('Jefe final: La Feria de Inventos',
                  '🏆 ¡El gran día! Presenta tu invento en la Feria de Inventos (pregúntale a tu profe si pueden invitar a sus familias).\n\n'
                  'Tu presentación debe tener:\n1. El problema que resuelve tu invento.\n2. Una demostración en vivo.\n'
                  '3. La explicación de una parte de tu código.\n4. Qué fue lo más difícil y cómo lo resolviste.\n\n'
                  'Tu profe evalúa: ¿funciona?, ¿usa al menos 3 piezas del kit?, ¿lo sabes explicar?, ¿es creativo?',
                  tipo='presencial', xp=250, monedas=100),
         ]},
     ]},
]

CURSO = {
    'nombre': 'Robótica · Primaria Alta (kit Arduino Rexqualis R3)',
    'juegos': JUEGOS,
    'mundos': MUNDOS,
}
