# Autonomous Surveillance Rover

## Overview

A full-stack engineering project built for a Master of Computer Applications final year major. It combines:

- ESP32-CAM edge video capture and ultrasonic sensing.
- Django + Channels backend for streaming, threat detection, and remote controls.
- YOLOv8 object detection and face recognition analytics.
- React + Tailwind dashboard for live monitoring and control.

## Repository Structure

```
Autonomous-Surveillance-Rover/
│
├── Frontend/                    <-- React Dashboard Application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
├── Backend/                     <-- Django Web Server & Vision Analytics
│   ├── manage.py
│   ├── Backend/                 <-- Django project config
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   └── urls.py
│   ├── core/                    <-- Server Config & WebSocket Routing
│   │   ├── asgi.py
│   │   └── routing.py
│   ├── surveillance_app/        <-- Streaming, REST APIs, and Signal Handlers
│   │   ├── ai_models/           <-- YOLOv8 & Face Recognition scripts
│   │   ├── consumers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── requirements.txt
│
└── Embedded_Firmware/           <-- C++ Logic for Microcontrollers
    ├── esp32_cam_stream/        <-- Video Wi-Fi Client configuration
    └── motor_navigation/        <-- Sensor tracking & H-Bridge motor driving
```

## Setup Notes

- Install backend dependencies in a Python 3.10+ virtual environment.
- Run `python Backend/manage.py migrate` then `python Backend/manage.py runserver`.
- Install frontend dependencies in `Frontend/` and use `npm start`.
- ESP32 firmware stubs are in `Embedded_Firmware/` and need your Wi-Fi credentials.

## Important

This repository currently contains scaffolded source files for the project, including Django app modules, React dashboard components, and ESP32 firmware stubs.
