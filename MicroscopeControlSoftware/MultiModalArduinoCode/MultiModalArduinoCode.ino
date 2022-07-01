#include <Adafruit_GFX.h>
//#include <Adafruit_GrayOLED.h>
//#include <Adafruit_SPITFT.h>
//#include <Adafruit_SPITFT_Macros.h>
//#include <gfxfont.h>

#include <Stepper.h>
long z; // number of z steps, defined variable
long sp = 400; // speed of motor

//define variables for serial control
char inputChar = ' ';         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
String intvar;
String ledChar;
char intchar;
char intvar2;

// Set steps per revolution
#define STEPS 100
//  fill_c = matrix.Color333(7, 0, 0);
// Motor pins


int Zpin1 = 10;   // H-bridge, Z-axis motor pin 1
int Zpin2 = 12;   // H-bridge, Z-axis motor pin 2
int Zpin3 = 13;   // H-bridge, Z-axis motor pin 3
int Zpin4 = 11;   // H-bridge, Z-axis motor pin 4
//String zstep;

// Motor pins
Stepper motor3(STEPS, Zpin2, Zpin1, Zpin3, Zpin4);


#include "Adafruit_HT1632.h"

#define HT_DATA 2
#define HT_WR   3
#define HT_CS   4
#define HT_CS2  5

Adafruit_HT1632LEDMatrix matrix = Adafruit_HT1632LEDMatrix(HT_DATA, HT_WR, HT_CS);

String command;
int LED_ON   = 10;
int LED_ON_DF = 15;
int LED_OFF  = 0;
int rr       = 7;// Radius of imaging
int rrs      = 5; // Radius of small circle
int xx       = 8; // x position of the circles (NOTE DONT CHANGE!! semi circles will break)
int yy       = 8;
int rri      = 5; // Inner Radius of Darkfield Imaging
int rro      = 7; // Outer Radius of Darkfield Imaging

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);  // Baud rate for serial communication (originally 9600)
//  delay(2000);
  matrix.begin(ADA_HT1632_COMMON_16NMOS);
//  Serial.println("Hi there");
//  delay(500);
  matrix.fillScreen();
  delay(500);
  motor3.setSpeed(sp);
  pinMode(Zpin1, OUTPUT);
  pinMode(Zpin2, OUTPUT);
  pinMode(Zpin3, OUTPUT);
  pinMode(Zpin4, OUTPUT);

  SemiTEdge();
  delay(100);
  SemiREdge();
  delay(100);
  SemiBEdge();
  delay(100);
  SemiLEdge();
  delay(100);
  QrtTREdge();
  delay(100);
  QrtTLEdge();
  delay(100);
  QrtBREdge();
  delay(100);
  QrtBLEdge();
  delay(100);
  matrix.clearScreen();
  while (!Serial);

}

void loop() {
  // put your main code here, to run repeatedly:
//  if (Serial.available()) {
//    command = Serial.readStringUntil('\n');
//    command.trim();
//    if (command.equals("T")) {
//      topHalf();
//      Serial.println("Order Received for Top Half");
//    }
//  }
  if (Serial.available()) {
//    intvar = Serial.readStringUntil();
//    intvar.toCharArray(intchar, 2);
//    Serial.print(intchar);

    intchar = (char)Serial.read();
//    intchar = String(Serial.read());
//    intvar2 = (char)Serial.read();
//    Serial.print(intvar);
//    Serial.print(intchar);
//    Serial.write('\n');
    
    if (intchar == 'I') 
    {
      inputChar = ' ';
//      while (Serial.available()) {
        // get the new byte:
        // add it to the inputString:
//        ledChar = (char)Serial.read();
        ledChar = Serial.readStringUntil('\n');
//        Serial.print(ledChar);
//        Serial.write('\n');
//        inputChar = (char)Serial.read();
        // if the incoming character is a newline, set a flag
        // so the main loop can do something about it:
//        if (inputChar == '\n') {
//          stringComplete = true;
//        }
//          if (stringComplete) {
        if (ledChar.equals("T")) {
          topHalf();
          Serial.print('1');
        } else if (ledChar.equals("B")) {
          botHalf();
          Serial.print('1');
        } else if (ledChar.equals("L")) {
          lftHalf();
          Serial.print('1');
        } else if (ledChar.equals("R")) {
          rgtHalf();
          Serial.print('1');
        } else if (ledChar.equals("F")) {
          fullCrc();
          Serial.print('1');
        } else if (ledChar.equals("O")) {
          emptySc();
          Serial.print('1');
        } else if (ledChar.equals("E")) {
          outEdge();
          Serial.print('1');
        } else if (ledChar.equals("S")) {
          smallCrc();
          Serial.print('1');
        } else if (ledChar.equals("C")) {
          fill();
          Serial.print('1');
        } else if (ledChar.equals("G")) {
          SemiTEdge();
          Serial.print('1');
        } else if (ledChar.equals("H")) {
          SemiBEdge();
          Serial.print('1');
        } else if (ledChar.equals("J")) {
          SemiREdge();
          Serial.print('1');
        } else if (ledChar.equals("K")) {
          SemiLEdge();
          Serial.print('1');
        } else if (ledChar.equals("W")) {
          QrtTREdge();
          Serial.print('1');
        } else if (ledChar.equals("X")) {
          QrtTLEdge();
          Serial.print('1');
        } else if (ledChar.equals("Y")) {
          QrtBREdge();
          Serial.print('1');
        } else if (ledChar.equals("Z")) {
          QrtBLEdge();
          Serial.print('1');
        }
        else{
          while(Serial.available()){
          char dump1 = Serial.read();
          Serial.print('1');
        }
        
//      }
      
        }
    }
    else if (intchar == 'M') {
      String zstep = Serial.readStringUntil('\n');
      z = zstep.toInt();

       motor3.step(z);
//
      digitalWrite(Zpin1, LOW);
      digitalWrite(Zpin2, LOW);
      digitalWrite(Zpin3, LOW);
      digitalWrite(Zpin4, LOW);
      //digitalWrite(readpin, LOW);
      //Serial.print(zstep + '\n');
      Serial.print('0');

    }
    else{
      while(Serial.available()){
      char dump2 = Serial.read();
      Serial.print('0');
    }
  }
}
}
//
//
void topHalf() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rr,LED_ON);
  matrix.fillCircle(xx,yy-1,rr,LED_ON);
  matrix.fillCircle(xx-1,yy-1,rr,LED_ON);
  matrix.fillCircle(xx-1,yy,rr,LED_ON);
  //fullCrc();
  matrix.fillRect(0, yy-8, 24, yy, LED_OFF);
  matrix.writeScreen();
  }


void botHalf() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rr,LED_ON);
  matrix.fillCircle(xx,yy-1,rr,LED_ON);
  matrix.fillCircle(xx-1,yy-1,rr,LED_ON);
  matrix.fillCircle(xx-1,yy,rr,LED_ON);
  //fullCrc();
  matrix.fillRect(0, yy, 24, yy, LED_OFF);
  matrix.writeScreen();
  //matrix.writeScreen();
  }

void lftHalf() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rr,LED_ON);
  matrix.fillCircle(xx,yy-1,rr,LED_ON);
  matrix.fillCircle(xx-1,yy-1,rr,LED_ON);
  matrix.fillCircle(xx-1,yy,rr,LED_ON);
  //fullCrc();
  matrix.fillRect(xx-8, 0, xx, 16, LED_OFF);
  matrix.writeScreen();
  }

void rgtHalf() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rr,LED_ON);
  matrix.fillCircle(xx,yy-1,rr,LED_ON);
  matrix.fillCircle(xx-1,yy-1,rr,LED_ON);
  matrix.fillCircle(xx-1,yy,rr,LED_ON);
  //fullCrc();
  matrix.fillRect(xx, 0, xx, 16, LED_OFF);
  matrix.writeScreen();
  }

void outEdge() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rro,LED_ON_DF);
  matrix.fillCircle(xx,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy,rro,LED_ON_DF);

  matrix.fillCircle(xx,yy,rri,LED_OFF);
  matrix.fillCircle(xx,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy,rri,LED_OFF);
  matrix.writeScreen();

}

void SemiTEdge() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rro,LED_ON_DF);
  matrix.fillCircle(xx,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy,rro,LED_ON_DF);

  matrix.fillCircle(xx,yy,rri,LED_OFF);
  matrix.fillCircle(xx,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy,rri,LED_OFF);
  matrix.fillRect(0, yy-8, 24, yy, LED_OFF);

  matrix.writeScreen();

}

void SemiBEdge() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rro,LED_ON_DF);
  matrix.fillCircle(xx,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy,rro,LED_ON_DF);

  matrix.fillCircle(xx,yy,rri,LED_OFF);
  matrix.fillCircle(xx,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy,rri,LED_OFF);
  matrix.fillRect(0, yy, 24, yy, LED_OFF);

  matrix.writeScreen();

}
void SemiLEdge() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rro,LED_ON_DF);
  matrix.fillCircle(xx,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy,rro,LED_ON_DF);

  matrix.fillCircle(xx,yy,rri,LED_OFF);
  matrix.fillCircle(xx,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy,rri,LED_OFF);
  matrix.fillRect(xx-8, 0, xx, 16, LED_OFF);

  matrix.writeScreen();

}

void SemiREdge() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rro,LED_ON_DF);
  matrix.fillCircle(xx,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy,rro,LED_ON_DF);

  matrix.fillCircle(xx,yy,rri,LED_OFF);
  matrix.fillCircle(xx,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy,rri,LED_OFF);
  matrix.fillRect(xx, 0, xx, 16, LED_OFF);

  matrix.writeScreen();

}

void QrtTREdge() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rro,LED_ON_DF);
  matrix.fillCircle(xx,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy,rro,LED_ON_DF);

  matrix.fillCircle(xx,yy,rri,LED_OFF);
  matrix.fillCircle(xx,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy,rri,LED_OFF);
  matrix.fillRect(xx, 0, xx, 16, LED_OFF);
  matrix.fillRect(0, yy-8, 24, yy, LED_OFF);


  matrix.writeScreen();

}

void QrtTLEdge() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rro,LED_ON_DF);
  matrix.fillCircle(xx,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy,rro,LED_ON_DF);

  matrix.fillCircle(xx,yy,rri,LED_OFF);
  matrix.fillCircle(xx,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy,rri,LED_OFF);
  matrix.fillRect(xx-8, 0, xx, 16, LED_OFF);
  matrix.fillRect(0, yy-8, 24, yy, LED_OFF);

  matrix.writeScreen();

}

void QrtBREdge() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rro,LED_ON_DF);
  matrix.fillCircle(xx,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy,rro,LED_ON_DF);

  matrix.fillCircle(xx,yy,rri,LED_OFF);
  matrix.fillCircle(xx,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy,rri,LED_OFF);
  matrix.fillRect(xx, 0, xx, 16, LED_OFF);
  matrix.fillRect(0, yy, 24, yy, LED_OFF);

  matrix.writeScreen();

}

void QrtBLEdge() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rro,LED_ON_DF);
  matrix.fillCircle(xx,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy-1,rro,LED_ON_DF);
  matrix.fillCircle(xx-1,yy,rro,LED_ON_DF);

  matrix.fillCircle(xx,yy,rri,LED_OFF);
  matrix.fillCircle(xx,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy-1,rri,LED_OFF);
  matrix.fillCircle(xx-1,yy,rri,LED_OFF);
  matrix.fillRect(xx-8, 0, xx, 16, LED_OFF);
  matrix.fillRect(0, yy, 24, yy, LED_OFF);

  matrix.writeScreen();

}

void fullCrc() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rro,LED_ON);
  matrix.fillCircle(xx,yy-1,rro,LED_ON);
  matrix.fillCircle(xx-1,yy-1,rro,LED_ON);
  matrix.fillCircle(xx-1,yy,rro,LED_ON);
  //fullCrc();
  matrix.writeScreen();
}

void smallCrc() {
  matrix.clearScreen();
  matrix.fillCircle(xx,yy,rrs,LED_ON);
  matrix.fillCircle(xx,yy-1,rrs,LED_ON);
  matrix.fillCircle(xx-1,yy-1,rrs,LED_ON);
  matrix.fillCircle(xx-1,yy,rrs,LED_ON);
  //fullCrc();
  matrix.writeScreen();
}

void emptySc() {
  matrix.clearScreen();

}


void fill()  {
  matrix.fillScreen();
}


void serialEvent() {
  if (Serial.available()) {
//    intvar = Serial.readStringUntil();
//    intvar.toCharArray(intchar, 2);
//    Serial.print(intchar);

    intchar = (char)Serial.read();
//    intchar = String(Serial.read());
//    intvar2 = (char)Serial.read();
//    Serial.print(intvar);
//    Serial.print(intchar);
//    Serial.write('\n');
    
    if (intchar == 'I') 
    {
      inputChar = ' ';
//      while (Serial.available()) {
        // get the new byte:
        // add it to the inputString:
//        ledChar = (char)Serial.read();
        ledChar = Serial.readStringUntil('\n');
//        Serial.print(ledChar)
        Serial.print(ledChar);
        Serial.write('\n');
//        inputChar = (char)Serial.read();
        // if the incoming character is a newline, set a flag
        // so the main loop can do something about it:
//        if (inputChar == '\n') {
//          stringComplete = true;
//        }
//          if (stringComplete) {
        if (ledChar.equals("T")) {
          topHalf();
          Serial.print('1');
        } else if (ledChar.equals("B")) {
          botHalf();
          Serial.print('1');
        } else if (ledChar.equals("L")) {
          lftHalf();
          Serial.print('1');
        } else if (ledChar.equals("R")) {
          rgtHalf();
          Serial.print('1');
        } else if (ledChar.equals("F")) {
          fullCrc();
          Serial.print('1');
        } else if (ledChar.equals("O")) {
          emptySc();
          Serial.print('1');
        } else if (ledChar.equals("E")) {
          outEdge();
          Serial.print('1');
        } else if (ledChar.equals("S")) {
          smallCrc();
          Serial.print('1');
        } else if (ledChar.equals("C")) {
          fill();
          Serial.print('1');
        }
        else{
          while(Serial.available()){
          char dump1 = Serial.read();
          Serial.print('1');
        }
        
//      }
      
        }
    }
    else if (intchar == 'M') {
      String zstep = Serial.readStringUntil('\n');
      z = zstep.toInt();

       motor3.step(z);
//
      digitalWrite(Zpin1, LOW);
      digitalWrite(Zpin2, LOW);
      digitalWrite(Zpin3, LOW);
      digitalWrite(Zpin4, LOW);
      //digitalWrite(readpin, LOW);
      //Serial.print(zstep + '\n');
      Serial.print('0');

    }
    else{
      while(Serial.available()){
      char dump2 = Serial.read();
      Serial.print('0');
    }
  }
}
}
