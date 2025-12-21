# here we are using official python runtime as parent image
FROM python:3.12-slim

#setting working directory
WORKDIR /app

# Copy requirements first (for better caching, as the docker images are created in a layered manner we should write the layers first that are less likely to be changes frequently)
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application
COPY . .

EXPOSE 5001

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD [ "python","app.py" ]
