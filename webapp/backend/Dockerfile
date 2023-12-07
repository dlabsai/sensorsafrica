# Base image
FROM node:18

# Create app directory
WORKDIR /usr/src/app

COPY --chown=node:node package*.json ./

COPY --chown=node:node . .

RUN rm .env

RUN yarn install

# Run the build command which creates the production bundle
RUN yarn run build

# Set NODE_ENV environment variable
ENV NODE_ENV production

USER node

EXPOSE 4000

# Start the server using the production build
CMD [ "node", "dist/main.js" ]
