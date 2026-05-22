#! usr/bin/bash

curl -X POST http://localhost:8000/order -H "Content-Type:
  application/json" -d '{"item":"laptop","quantity":1}'