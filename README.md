# Student Management Stystem

## Overview

This Student Management System is built using Node.js and follows a **microservice architecture** to keep things simple and flexible. The system is divided into separate independent services, each handling specific tasks. Each service uses the Model-View-Controller (MVC) architectural pattern.

The system has 4 services, namely the Student, Registration, Teacher and Notidication services. Registration Service is tasked with registering or updating students information about the accademic year. Teacher Service is involved in teacher infomration. Student service is where all the infomration is stored about the student. Notification Service sends updates, reminders and announcements to the students.

## Architecture

### System Architecture Diagram

Microservice Architecture for Student Management System
```plaintext

                    +-----------------------+
                    |  Notification Service |
                    |                       |
                    | Sends updates,        |
                    | reminders, and        |
                    | announcements         |
                    +-----------^-----------+
                                |
                                |
    +----------------------+    |    +-----------------------+
    |    Student Service   |<---+--->|  Registration Service |
    | Stores all student   |         | Manages registration  |
    | information          |         | and academic year     |
    |                      |         | updates               |
    |                      |         |                       |
    +-----------^----------+         +-----------------------+
                |                                      
                |
                |_______________
                                |
                    +-----------+-----------+
                    |    Teacher Service    |
                    | Manages teacher       |
                    | information and       |
                    | schedules             |
                    +-----------------------+
```
All services are independent and follow the Model-View-Controller (MVC) architecture. Communication between services is facilitated through well-defined APIs.

### Architectural Patterns

- **MVC (Model-View-Controller)**: Used for Node.js-based services to maintain separation of concerns:

  - **Model**: Handles data and business logic.
  - **View**: Responsible for presenting the output (not directly applicable for backend APIs).
  - **Controller**: Processes incoming requests and delegates logic to the service layer.



## Services Overview

### 1. Registration Service (FastAPI, MVC)

- **Purpose**: Register students for academic year.
- **Technology**:Fast API, Python.
- **Responsibilities**:
  - Student Registration.
  - update the notification service.

### 2. Teacher Service (Node.js, MVC)

- **Purpose**: Teacher registration and assigning to course.
- **Technology**: Node.js, Express, TypeScript.

### 3. Student Service (Node.js, MVC)

- **Purpose**: Register new students.
- **Technology**: Node.js, Express, TypeScript.
- **Responsibilities**:
  - Register new students.
  - link students with course and teacher.

### 4. Notification Service (Node.js, MVC)

- **Purpose**: Notify students of their current status.
- **Technology**: Node.js, Express, TypeScript.

<br />
<br />

## Communication

- **Inter-Service Communication**:

  - Services communicate via REST APIs.
  - Asynchronous messaging (e.g., RabbitMQ or Kafka) is planned for event-driven operations.

- **Data Sharing**:
  - Each service maintains its own database for a decentralized approach.
  - APIs are used to share required data between services.



<br />
<br />

## Scalability and Fault Tolerance

- **Horizontal Scaling**: Each service can be scaled independently.
- **Database Isolation**: Each service uses a dedicated database to ensure autonomy.
- **Resilience**: Services are loosely coupled to prevent cascading failures.

## Security

- **Authentication**: User and driver authentication via secure tokens
- **Data Encryption**: All sensitive data is encrypted in transit and at rest.
- **API Gateway**: Centralized API gateway for secure communication and routing.

<br />
<br />

## Installation and Deployment

### Prerequisites

- Docker (recommended for containerized deployment).

### Steps

1. Clone the repositories for all services.

   ```bash
   git clone <repository_url>
   ```

2. Set up `.env` files for each service with appropriate configurations.

3. Run services:

    ```bash
    docker-compose up
    ```

4. Access APIs via the centralized API Gateway.
    ```bash
    http://localhost:8080/<<service>>
    ```
