// serial_test.ino
char dataString[50] = {0};
int a =0;  

void setup() {
  Serial.begin(9600);  // Starting serial communication
}

void loop() {
  if(a<10) {
    a++;                          
    sprintf(dataString,"%02X",a); // convert a value to hex  
    Serial.println(dataString);   // send the data 
    delay(1000); 
  }
}
