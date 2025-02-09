# 1. python version
FROM python:3.12.6

RUN echo "Hello"

# 2. set python buffering
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


# 2.1 working directory
WORKDIR /app

# 4. install dependencies
RUN pip install -U pip setuptools wheel
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# 5. local root directory -> docker root directory 
COPY . .


