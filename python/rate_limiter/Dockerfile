# Python

FROM python:3.11
ADD rate_limiter.py utils.py ./
RUN pip install requests flask
CMD ["python", "./rate_limiter.py"]
