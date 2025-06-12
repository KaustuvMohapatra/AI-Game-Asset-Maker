---

# AI Asset Generator API

This project implements a scalable, asynchronous API for generating images from text prompts using Stable Diffusion. It leverages **FastAPI** for the web server, **Celery** for background task processing, and **Redis** as the message broker and result backend.

## Project Architecture

The system is designed to decouple the client-facing API from the computationally expensive image generation process. This ensures the API remains responsive and can handle multiple requests concurrently.

1.  A **Client** sends a `POST` request with a prompt to the FastAPI server.
2.  The **FastAPI Server** (`main.py`) validates the request, creates a job, and immediately pushes it to the **Redis** message queue. It instantly returns a `job_id` to the client.
3.  A **Celery Worker** (`tasks.py`), running as a separate process, picks up the job from Redis.
4.  The Worker executes the Stable Diffusion pipeline to generate the image, saving the result to a static `output/` directory.
5.  The Client can poll a separate endpoint using the `job_id` to check the status and retrieve the URL of the final image once the job is complete.

```
+--------+      1. POST /v1/generate      +--------------+      2. Enqueue Task      +---------+
| Client | ----------------------------> | FastAPI (main) | ----------------------> |  Redis  |
+--------+      <---------------------------- |              +--------------+      <-----------+      +---------+
            8. GET /v1/jobs/{id}             | (Returns job_id)                        |           |
            (Poll for status)                |                                         | 3. Dequeue Task
                                             |                                         |
                                             v                                         v
                                     +-----------------+      4. Generate Image     +------------------+
                                     | Celery Worker   | --------------------------> | Stable Diffusion |
                                     | (tasks.py)      |      5. Save to Disk       +------------------+
                                     +-----------------+
                                             |
                                             v
                                     +-----------------+
                                     |  output/folder  |
                                     +-----------------+
```

## Core Components

### 1. `main.py` - FastAPI Server

This file acts as the core API server. It provides a RESTful interface for users to initiate image generation tasks and monitor their progress.

-   **`/v1/generate` (POST)**:
    -   Accepts a JSON request (`GenerateRequest`) containing a `prompt`, optional `negative_prompt`, `style_id`, and `seed`.
    -   Enqueues a background task by calling `generate_task.delay(...)`.
    -   Immediately returns a JSON response with the unique `job_id`.
-   **`/v1/jobs/{job_id}` (GET)**:
    -   Allows clients to query the status of a submitted job (`PENDING`, `STARTED`, `SUCCESS`, `FAILURE`).
    -   If the task has succeeded, it returns the URL(s) of the generated image(s).
-   **`/output`**:
    -   Serves the `output/` directory as a static folder, making generated images accessible via HTTP.

### 2. `tasks.py` - Celery Worker

This file defines the background processing logic for the image generation task using Celery. It handles the heavy computation, allowing the main API to remain non-blocking.

-   **Celery App Initialization**: Configures a Celery app named `game_asset_worker` to use Redis as both the message broker and result backend.
-   **`generate_task` Function**:
    -   Decorated with `@celery_app.task` to mark it as a distributed task.
    -   Loads the pre-trained **Stable Diffusion** model from the `diffusers` library.
    -   Generates an image based on the prompt, negative prompt, and seed. If the seed is `-1`, a random one is generated.
    -   Saves the final image to the `output/` directory with a unique filename.
    -   Returns a dictionary containing the relative URL path to the generated image.

### 3. `schemas.py` - Pydantic Data Models

This file defines the data models for API request validation and response formatting using Pydantic, ensuring data consistency and type safety.

-   **`GenerateRequest`**:
    -   Defines the structure for incoming generation requests.
    -   `prompt`: `str` - The main text prompt.
    -   `negative_prompt`: `Optional[str]` - What to exclude from the image.
    -   `style_id`: `int` - An identifier for a specific visual style.
    -   `seed`: `int` - A seed for controlling randomness (defaults to `-1` for random).
-   **`JobStatusResponse`**:
    -   Defines the structure for job status responses.
    -   `job_id`: `str` - The unique identifier for the task.
    -   `status`: `str` - The current state of the job (e.g., "PENDING", "SUCCESS").
    -   `result_urls`: `Optional[List[str]]` - A list of URLs for the generated images upon success.

### 4. `config.py` - Configuration

This file centralizes application configuration, making it easy to manage settings across different environments (e.g., development, production).

-   It retrieves the `REDIS_URL` from environment variables using `os.getenv`.
-   If the `REDIS_URL` environment variable is not set, it provides a default value of `"redis://localhost:6379/0"`, which is convenient for local development.

---

## How to Run

### Prerequisites

-   Python 3.10.6
-   Docker Desktop
-   Git Bash or a similar command-line interface

### Installation and Setup

1.  **Create Project Folder**:
    Create a new directory for the project.
    ```bash
    mkdir ai_asset_generator_api
    cd ai_asset_generator_api
    ```

2.  **Set Up Virtual Environment**:
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Requirements**:
    Create a `requirements.txt` file with the necessary packages and install them.
    *(Note: You would list packages like `fastapi`, `uvicorn`, `celery`, `redis`, `pydantic`, `torch`, `diffusers`, `transformers`, etc., here)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Redis with Docker**:
    Pull the Redis image and run it in a container.
    ```bash
    docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
    ```
    *For future sessions, you can simply start the existing container from the Docker Desktop app.*

5.  **Create Python Files**:
    Create the four described Python files (`main.py`, `tasks.py`, `schemas.py`, `config.py`) in your project folder.

### Running the Application

You will need two separate terminals running in your project directory with the virtual environment activated.

1.  **Terminal 1: Start the Celery Worker**
    ```bash
    celery -A tasks.celery_app worker --loglevel=info --pool=solo
    ```
    *The `--pool=solo` flag is useful for tasks that use GPU resources to prevent parallel execution conflicts on a single GPU.*

2.  **Terminal 2: Start the FastAPI Server**
    ```bash
    uvicorn main:app --reload
    ```
    *The `--reload` flag automatically restarts the server when you make code changes.*

The backend is now ready! You can access the API documentation at `http://127.0.0.1:8000/docs`.
