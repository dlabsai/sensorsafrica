# Base image
FROM node:18

# Create app directory
WORKDIR /usr/src/app

COPY --chown=node:node package*.json ./

COPY --chown=node:node . .

RUN rm .env

RUN yarn install


# Set NODE_ENV environment variable

USER node

# Start the server using the production build
CMD [ "yarn", "start" ]
