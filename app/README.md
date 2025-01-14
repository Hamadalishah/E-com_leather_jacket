
## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd Ecom_backend
    ```

2. Build and start the services using Docker Compose:
    ```sh
    docker-compose up --build
    ```

### Environment Variables

Create a `.env` file in the [app](http://_vscodecontentref_/5) directory and add the necessary environment variables.

### Usage

The application will be available at `http://localhost:8004`.

### Project Dependencies

The project uses the following dependencies:

- Python 3.12
- FastAPI
- SQLModel
- Uvicorn
- Python-dotenv
- Python-jose
- Passlib
- Psycopg2
- Httpx
- Pydantic-settings
- Multipart
- Python-multipart

### License

This project is licensed under the MIT License - see the LICENSE file for details.