FROM python
COPY . /src
WORKDIR /src

RUN pip install -r requirements.txt
CMD ["python", "postr/app.py"]
