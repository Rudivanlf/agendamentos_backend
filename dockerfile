# 1. Use uma imagem oficial do Python como base
FROM python:3.11-slim

# 2. Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copie o arquivo de dependências primeiro (para otimizar o cache)
COPY requirements.txt .

# 4. Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie o resto do código da sua aplicação para dentro do contêiner
COPY ./app /app/app

# 6. Exponha a porta que o Uvicorn vai usar
EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# 7. Defina o comando para iniciar a aplicação quando o contêiner rodar
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]