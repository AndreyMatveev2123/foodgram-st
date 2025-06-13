# build env
FROM node:16
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . ./
RUN npm run build
CMD ["sh", "-c", "cp -r build/* /app/result_build/build/ && tail -f /dev/null"]
