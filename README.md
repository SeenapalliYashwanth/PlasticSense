# PlasticSense 🌍

PlasticSense is a web-based system that helps users determine whether a plastic item is reusable, recyclable, or unsafe.

## Features
- Image-based plastic detection (ML placeholder)
- Rule-based safety decision engine
- Explainable output for users

## Tech Stack
- Backend: FastAPI
- Frontend: HTML, CSS, JavaScript
- ML: Image-based classification (extensible to CNN)

## Architecture
Image → ML Detection → Rule Engine → Explanation

## Future Improvements
- Replace placeholder ML with CNN (MobileNetV2)
- Improve accuracy with real dataset
- Deploy full system online

## Design Decisions
- Used rule-based logic for safety-critical decisions to ensure correctness and explainability  
- Used ML only for perception (image classification)  
- Prioritized simplicity and reliability over complex models

## Limitations
- ML model currently uses placeholder logic  
- Limited dataset for training  
- Does not handle mixed plastic materials

## API Endpoints
GET /analyze  
POST /analyze-image  
