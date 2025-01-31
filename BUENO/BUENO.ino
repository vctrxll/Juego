#include <Servo.h>

Servo servoMotor;


void setup() {
 pinMode(8,INPUT);
 Serial.begin(9600);

 servoMotor.attach(9);
 servoMotor.write(0);
 digitalWrite(8,HIGH);

}

void loop() {


if( digitalRead(8)==LOW){ // Validamos si hay una moneda insertada.
     Serial.println("COIN"); //Imprimimos en el puerto serial la palabra "COIN"  
     delay(1000); //Esperamos un segundo.

     //digitalWrite(8,LOW);
}
digitalWrite(8,HIGH);

if (Serial.available() > 0) { // Verifica si hay datos en el puerto serie
    String mensaje = Serial.readStringUntil("/n"); // Lee hasta encontrar '\n'  
      Serial.println(mensaje);
    // Puedes verificar el contenido del mensaje
    if (mensaje == "darobsequio") {
      servoMotor.write(180);
      delay(1000);
      Serial.println("¡Obsequio concedido!");
      servoMotor.write(-180);
    } else {
      Serial.println("Mensaje desconocido.");
    }
  }

}
