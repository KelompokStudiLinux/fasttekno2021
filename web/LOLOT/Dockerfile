FROM node

WORKDIR /app

COPY public /app/public
COPY index.js /app
COPY package.json /app
RUN npm install

RUN useradd -m lolot
COPY flag.txt /home/lolot/flag.txt

EXPOSE 3000
CMD "node" "index.js"
