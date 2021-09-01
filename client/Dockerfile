# base image
FROM node:latest as builder

# set working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY app/package.json /usr/src/app/package.json
RUN npm install
RUN npm install react-scripts@1.1.1 -g

COPY ./app /usr/src/app
# start app
CMD ["npm", "start"]

# production environment
FROM nginx:alpine
RUN rm -rf /etc/nginx/conf.d
COPY conf /etc/nginx
COPY --from=builder /usr/src/app/build /etc/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]