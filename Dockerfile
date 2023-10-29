FROM python:alpine
ENV PYTHONUNBUFFERED 1

EXPOSE 5678 8000
WORKDIR /code
COPY url_shortener poetry.lock pyproject.toml /code/

# Зависимости различных пакетов с сишными биндингами
RUN apk add --no-cache build-base postgresql-dev

# Устанавливаем poetry и зависимости
# Без --no-root обновления кода не будут применяться (так как глобальный модуль будет запускаться)
RUN python -m pip install --upgrade pip && \
  pip install poetry==1.3.2 debugpy && \
  poetry config virtualenvs.create false && \
  poetry install --no-root

# Для отладки ч/з VSCode
# Creates a non-root user and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /code
USER appuser

# fix uvicorn issue: "Debugger warning: It seems that frozen modules are being used, which may"
ENV PYDEVD_DISABLE_FILE_VALIDATION=1

# Запускаем отладчик и uvicorn
CMD python -m debugpy --wait-for-client --listen 0.0.0.0:5678 -m uvicorn url_shortener:app --reload --host 0.0.0.0 --port 8000
