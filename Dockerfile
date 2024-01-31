FROM python:3.9-slim-bullseye

WORKDIR /app

RUN apt update && apt install -y curl 

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    mv kubectl /usr/local/bin/ && \
    chmod +x /usr/local/bin/kubectl

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3",  "./clean-finalizers.py", "argocd" ]
