const int ledVermelhoCarro = 13;
const int ledAmareloCarro   = 12;
const int ledVerdeCarro     = 11;
const int ledVermelhoPed    = 10;
const int ledVerdePed       = 9;

void setup() {
  Serial.begin(9600);
  pinMode(ledVermelhoCarro, OUTPUT);
  pinMode(ledAmareloCarro, OUTPUT);
  pinMode(ledVerdeCarro, OUTPUT);
  pinMode(ledVermelhoPed, OUTPUT);
  pinMode(ledVerdePed, OUTPUT);

  irParaEstadoPadrao();
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();
    
    if (comando == 'P') {
      executarCiclo(10000); // 10 segundos fechado (Pedestre)
    } 
    else if (comando == 'N') {
      executarCiclo(15000); // 15 segundos fechado (Normal)
    }
  }
}

// === FUNÇÃO CORRIGIDA COM X COMPLETAMENTE ===
void executarCiclo(unsigned long tempoFechado) {
  // 1. Amarelo de atenção padrão (3 segundos)
  digitalWrite(ledVerdeCarro, LOW);
  digitalWrite(ledAmareloCarro, HIGH);
  delay(3000); 
  
  // 2. Fecha para carros e abre para pedestres
  digitalWrite(ledAmareloCarro, LOW);
  digitalWrite(ledVermelhoCarro, HIGH);
  digitalWrite(ledVermelhoPed, LOW);
  digitalWrite(ledVerdePed, HIGH); 
  
  // Espera o tempo dinâmico mandado pelo Python
  delay(tempoFechado);
  
  // 3. Reseta e volta o fluxo dos carros
  irParaEstadoPadrao();
}

void irParaEstadoPadrao() {
  digitalWrite(ledVerdePed, LOW);
  digitalWrite(ledVermelhoPed, HIGH);
  digitalWrite(ledVermelhoCarro, LOW);
  digitalWrite(ledVerdeCarro, HIGH);
}