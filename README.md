# Student Management Stystem

## Overview

This Student Management System is built using Nvarious languages and frameworks and follows a **microservice architecture** to keep things simple and flexible. The system is divided into separate independent services, each handling specific tasks.

The system has 4 services, namely the Student, Registration, Authentication and Notidication services. Registration Service is tasked with registering or updating students information about the accademic year. Authentication Service is involved in authenticating users. Student service is where all the infomration is stored about the student. Notification Service sends reminders and announcements to the students.

## Architecture

### System Architecture Diagram

Microservice Architecture for Student Management System

![alt text](<Blank diagram (2)-1.png>)
All services are independent and follow the Model-View-Controller (MVC) architecture. Communication between services is facilitated through well-defined APIs.

### Architectural Patterns

- **MVC (Model-View-Controller)**: Used for Node.js-based services to maintain separation of concerns:

  - **Model**: Handles data and business logic.
  - **View**: Responsible for presenting the output (not directly applicable for backend APIs).
  - **Controller**: Processes incoming requests and delegates logic to the service layer.

## Services Overview

### Service Table

| Service Name           | Description                                | Endpoint                  | Dependencies            |
|------------------------|--------------------------------------------|---------------------------|-------------------------|
| Student Registration    | Manages student information and registration | `/api/students`           | Database Service        |
| Authentication         | Handles user authentication and authorization | `/auhtentication/api/auth`               | User Service            |
| Year Registration     | Registers students to the new year      | `/api/registration/api/registration`            | Student Registration Service |
| Notification Service    | Sends notifications (emails)          | `NONE`      | Student Registration, Course Registration |

### 1. Registration Service (FastAPI, MVC)

- **Purpose**: Register students for academic year.
- **Technology**:Fast API, Python.
- **Responsibilities**:
  - Student Registration.
  - update the notification service.

### 2. Authentication Service (Node.js, MVC)

- **Purpose**: Check that authenticated users access the system.
- **Technology**: Python, Flask.

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

![alt text](<Blank diagram.png>)

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
- **API Gateway**: Centralized API gateway for secure communication and routing.

<br />
<br />

### Docker Compos Table

| **Service Name**         | **Image**                   | **Container Name** | **Build Context**          | **Ports**        | **Depends On**        | **Environment Variables**           |
|--------------------------|-----------------------------|--------------------|---------------------------|------------------|-----------------------|-------------------------------------|
| `rabbitmq`              | `rabbitmq:3-management`    | `rabbitmq`         | N/A                       | `5672:5672`, `15672:15672` | N/A                   | `RABBITMQ_DEFAULT_USER=guest`      |
|                          |                             |                    |                           |                  |                       | `RABBITMQ_DEFAULT_PASS=guest`      |
| `student-service`       | student-service                        | student-service               | `./student-service`       | `8000:8000`     | `rabbitmq`, `nginx`   | `RABBITMQ_HOST=rabbitmq`           |
| `registration-service`  | registration-service                        | registration-service               | `./registration-service`  | `8001:8001`     | `rabbitmq`, `nginx`   | `RABBITMQ_HOST=rabbitmq`           |
| `notification-service`  | notification-service                        | notification-service               | `./notification-service`  | `8002:8002`     | `rabbitmq`            | `RABBITMQ_HOST=rabbitmq`           |
| `authentication-service`| authentication-service                        | authentication-service               | `./authentication-service`| `5002:5002`     | `rabbitmq`, `nginx`   | `RABBITMQ_HOST=rabbitmq`           |
| `nginx`                 | `nginx:latest`             | `nginx`            | N/A                       | `8080:80`       | N/A                   | N/A                                 |

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
    docker-compose up --build
    ```

4. Access APIs via the centralized API Gateway.

    ```bash
    http://localhost:8080/<<service>>
    ```
