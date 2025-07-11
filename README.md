# Solução Desafio Técnico Doutor-IE

author: [@klausbegnis](https://github.com/klausbegnis) 

## Descrição do problema

## Proposta

## Como utilizar
sudo docker build -t doutor-ie-api .
docker run -d --network doutor_ie_desafio -p 8081:8081 doutor-ie-api
## Conclusões e aprimoramentos

curl -X POST "http://localhost:8081/consulta" \
-H "Content-Type: application/json" \
-d '{"question": "doutor ie test"}'