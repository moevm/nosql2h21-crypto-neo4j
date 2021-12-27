FROM python:3.6

RUN mkdir -p /Users/denis/Downloads/app/
WORKDIR /Users/denis/Downloads/app/

COPY . /Users/denis/Downloads/app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]