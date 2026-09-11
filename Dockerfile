FROM node:22-alpine AS base
WORKDIR /app
FROM base AS backend
COPY backend/package*.json ./backend/
RUN cd backend && npm install
COPY backend ./backend
WORKDIR /app/backend
CMD ["npm","run","dev"]
FROM base AS frontend
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install
COPY frontend ./frontend
WORKDIR /app/frontend
CMD ["npm","run","dev","--","--host","0.0.0.0"]
