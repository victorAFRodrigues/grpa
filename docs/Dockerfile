# Estágio 1: Build
FROM node:20-alpine AS build

WORKDIR /app

# Instalar dependências
COPY package.json package-lock.json* ./
RUN npm install --frozen-lockfile

# Copiar código e gerar build estático
COPY . .
RUN npm run build

# Estágio 2: Serve com Nginx (Otimizado para produção)
FROM nginx:stable-alpine

# Copiar o build do Docusaurus para o diretório do Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Expor a porta 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
