# Trabalho-MQTT-Last-Will-e-Retain-Flag
Trabalho sobre LWT e Retain Flag  
Com base nos artigos da HiveMQ, o Last Will and Testament (LWT) e o Retained Messages são recursos fundamentais do protocolo MQTT para lidar com a natureza intermitente das redes IoT. Embora ambos envolvam o armazenamento de mensagens no broker, eles servem a propósitos opostos: um lida com a ausência do dispositivo e o outro com o seu último estado conhecido.

### Retained Messages (Mensagens Retidas)
O objetivo é garantir que um novo assinante não precise esperar que um sensor envie dados para conhecer seu estado atual.

Como funciona na prática:

Um sensor de temperatura publica o valor 25°C no tópico sensor/temp com a flag Retain = true.

O Broker armazena essa mensagem e o seu QoS.

Se um Dashboard (cliente) se conectar 10 minutos depois e assinar o tópico sensor/temp, o Broker enviará imediatamente os 25°C para ele, mesmo que o sensor só vá publicar novamente daqui a uma hora.


### Last Will and Testament (LWT)
O objetivo é notificar outros clientes quando um dispositivo se desconecta de forma "não graciosa" (queda de energia, perda de sinal, crash).

Como funciona na prática:

No momento da conexão (CONNECT), o cliente define uma mensagem de "testamento" (ex: tópico sensor/status, mensagem offline, Retain = true).

O Broker armazena essa mensagem, mas não a publica enquanto a conexão estiver ativa.

Se o dispositivo desconectar sem enviar um pacote DISCONNECT (o "adeus" formal), o Broker detecta a queda e publica automaticamente a mensagem offline no tópico especificado.

### Quando usar cada um?
Retain Flag:   
Você quer que o estado atual esteja sempre disponível para novos clientes.   
Status de uma lâmpada (On/Off), última temperatura medida, versão do firmware.   

LWT:  
Você precisa saber se um dispositivo "morreu" ou saiu do ar inesperadamente.  
Monitoramento de presença, alarmes críticos de conectividade, sistemas de saúde (heartbeat).

### Impactos em um sistema IoT Real
Experiência do Usuário (UX): Sem as Retained Messages, as interfaces de usuário (apps/dashboards) ficariam vazias ou com "carregando..." até que o dispositivo enviasse o próximo dado. Isso dá a impressão de que o sistema está lento ou quebrado.

Largura de Banda e Bateria: O LWT economiza recursos porque elimina a necessidade de os dispositivos enviarem mensagens de "estou vivo" (Keep-alive de aplicação) constantemente. O Broker faz o trabalho de monitoramento.

Confiabilidade: O LWT é a única forma confiável de saber se um dispositivo faliu em uma rede instável. Sem ele, você pode estar lendo uma temperatura retida de 2°C de 5 horas atrás, sem saber que o sensor está desconectado.

Gerenciamento de Estado: É importante limpar mensagens retidas enviando uma mensagem vazia com a flag Retain ativada. Se não for bem gerenciado, o sistema pode exibir informações obsoletas de dispositivos que já foram removidos fisicamente da rede.
