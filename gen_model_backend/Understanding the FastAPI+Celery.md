The folder contains 4 python files :
1. main.py : This FastAPI app queues image generation tasks with Celery and provides endpoints to submit prompts and check job statuses.
2. config.py : This file sets the REDIS_URL variable to the value of the REDIS_URL environment variable, or defaults to "redis://localhost:6379/0" if it's not set.
3. schemas.py : This code defines two Pydantic models:
  GenerateRequest: It represents a request body for image generation with fields for prompt, optional negative_prompt, style_id and seed.
  JobStatusResponse: It represents the response for a job status query, which includes job_id, status, and optional list of result_urls.
4. tasks.py : This file defines a Celery worker that uses the Stable Diffusion model to generate an image from a prompt and saves it to disk.

1. main.py :
The main.py file acts as the core API server for an asynchronous image generation system built using FastAPI and Celery. 
It provides a RESTful interface that allows users to initiate image generation tasks and monitor their progress. 
The application is designed to decouple the web-facing API from the compute-intensive image generation process, ensuring responsiveness and scalability.
One of the main features of the application is the /v1/generate endpoint. 
This endpoint accepts a JSON request containing details such as a prompt, optional negative prompt, style ID, and seed. 
Upon receiving this request, the API enqueues an image generation task using Celery by calling generate_task.delay(...). 
The job is processed in the background by a Celery worker, allowing the API to immediately return a response containing the unique job ID, without waiting for the task to complete.
In addition, the /v1/jobs/{job_id} endpoint allows clients to query the status of their submitted jobs. 
By using the job ID, the API checks the Celery backend for the current state of the task—whether it is pending, running, completed, or failed. 
If the task has succeeded, the endpoint returns the URLs of the generated images stored in the server’s output/ directory. 
This directory is mounted as a static file server at the /output route, making it easy to retrieve generated assets via HTTP.


2. config.py : 
The config.py file serves as a simple configuration module that defines environment-dependent settings for the application—in this case, the Redis connection URL.
It retrieves the REDIS_URL from environment variables using Python’s os.getenv function, providing a default value of "redis://localhost:6379/0" if the variable is not set.
This approach ensures flexibility and portability across different deployment environments. 
For example, in a local development environment, the default Redis URL can be used without any extra setup. 
In a production or cloud environment, the REDIS_URL can be externally defined, allowing the system to seamlessly connect to a remote Redis instance. 
By isolating this configuration logic in its own file, the application follows best practices for clean code organization and environment-specific adaptability.

3. schemas.py
The schemas.py file defines the data models used for request validation and response formatting in the FastAPI application. 
It uses Pydantic’s BaseModel to enforce type checking and structure on the input and output data, ensuring that the API handles data consistently and predictably.
The GenerateRequest model represents the expected structure of a request to generate an image. 
It includes four fields: prompt (the main text input for generation), negative_prompt (an optional field to specify what should be excluded from the image, defaulting to an empty string), style_id (an identifier for the desired visual style), and seed (used to control the randomness of the generation, defaulting to -1 to trigger random seed selection). 
This model ensures that any request sent to the /v1/generate endpoint contains the correct and complete data.
The JobStatusResponse model defines the format of the response returned by the /v1/jobs/{job_id} endpoint. 
It includes the job ID, the current status of the task (e.g., "PENDING", "STARTED", "SUCCESS", etc.), and an optional list of result URLs pointing to the generated images. 
This model provides a standardized way to communicate job progress and results to the client.
By isolating these data models in schemas.py, the application maintains a clean separation of concerns, making the codebase more organized, maintainable, and less error-prone.

4. tasks.py :
The `tasks.py` file defines the background processing logic for the image generation system using **Celery**, a distributed task queue. 
It is responsible for handling the heavy computation involved in generating images from text prompts using a pre-trained **Stable Diffusion** model, allowing the main FastAPI server to remain responsive and non-blocking.
At the top, the file initializes a Celery app named `"game_asset_worker"` and configures it to use **Redis** as both the message broker and the result backend. 
This setup allows Celery to receive task requests from the FastAPI application, execute them asynchronously, and store their results for later retrieval.
The heart of the file is the `generate_task` function, which is marked as a Celery task. This function loads the Stable Diffusion pipeline from Hugging Face’s `diffusers` library and moves it to GPU or CPU based on hardware availability. If the user hasn't provided a specific seed (i.e., seed is negative), the function generates a random one to ensure variability in the outputs. Using the prompt, negative prompt, and the seed, it generates an image using the model. 
The image is then saved in an `output/` directory with a filename that includes the style ID and seed to ensure uniqueness.
Finally, the function returns a dictionary containing a relative URL path to the saved image, which is later used by the API to inform users where they can access their generated images. 

Steps to run :
1. Create the project folder in main drive, e.g., "ai_asset_generator_api"
2. Create and activate a virtual environment in it (python version 3.10.6)
3. Install all requirements from GitBash/command prompt.
4. Install and run Docker app, and start Redis container (for future activations, run Redis container from the Docker app itself)
5. Create the four python files in the project folder.
6. Open the project folder path in terminal, and run : celery -A tasks.celery_app worker --loglevel=info --pool=solo
7. Open another such terminal in project path, and run : uvicorn main:app --reload

The backend is now ready. 
To generate images, queue and poll prompts.                                                   
                                                      

