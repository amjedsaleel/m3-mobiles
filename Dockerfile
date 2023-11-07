FROM python
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update -y
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY . .
ENTRYPOINT sh entrypoint.sh
