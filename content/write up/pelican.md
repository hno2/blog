---
author: Simon Klug
title: How to automatically deploy a Pelican blog with GitLab CI & Traefik
date: 2019-09-01
slug: ci-deploy-pelican
tags: tech, ci,cd, docker, pelican, blog, website, gitlab, python, traefik, deploy, automation
---
[TOC]

!!! warning
    This tip was written for Traefik 1.X available till End of August last year. Please read the appendix for updating to Traefik 2.X

I always wanted an easy to use blog to write down my thoughts for the world. This is it!
Since this is the first blog post, it will be a quick write-up how to get a pelican blog like this up in running with [GitLab CI/CD-Pipelines](https://about.gitlab.com/product/continuous-integration/). The reason behind this? I do not want to login in every time I update any post.

## Components
* I already have a vServer with the reverse proxy [Traefik](https://traefik.io/) running. Traefik is a lovely piece of software that helps tremendously with managing docker containers that are connected to the web. But any small server will do fine for this purpose.
* I learned to love [GitLab](https://about.gitlab.com/) at work and my university offers it for free for all students. You will need a GitLab Repository of your blog with a GitLab Runner connected (every [gitlab.com](https://gitlab.com) Repository comes with a free runner).

## Getting Started
[Pelican](https://blog.getpelican.com/) is a static site generator powered by python. This  means it will create static html from your markdown files and not much else. So the only thing you actually need on your server side is a domain and some kind of static hosting. 
Since I use traefik I need a docker container providing this static serving. 
There is a nginx dicjer image optimized for static serving. This image is provided [here](https://github.com/flashspys/docker-nginx-static) and is only about 4MB in size.

With traefik you can just run docker compose up with some labels added and have a domain-connected docker image. This is the `docker-compose.yaml` used for this site.

    ::yaml
    version: '3'
    networks:
    frontend:
        external: true
    services:
    yourdomain.de:
        image: flashspys/nginx-static
        container_name: yourdomain.de
        networks:
        - frontend
        ports:
        - 8080:80
        volumes:
        - ./src/:/static
        - ./default.conf:/etc/nginx/conf.d/default.conf
        labels:
        - "traefik.docker.network=frontend"
        - "traefik.enable=true"
        - "traefik.frontend.rule=Host:yourdomain.de, www.yourdomain.de"
        - "traefik.port=80"
        - "traefik.protocol=http"


!!! warning
    If you want to use traefik 2.X you need to update the label `traefik.frontend.rule` to be `` "traefik.http.routers.website.rule=Host(`yourdomain.de`) || Host(`www.yourdomain.de`)"``

What I do here is to connect this container to the right traefik network (`frontend`) and set up the domain-names with `traefik.frontend.rule`. The static content and the nginx config file are mounted as [docker volumes](https://docs.docker.com/storage/volumes/) for me being able to change them on the fly (without having to restart the container). 

Since I want to use fancy urls - without the `.html` at the end - I changed the default nginx config like this.

    server {
        listen       80;
        server_name  localhost;
        root /static;
        index index.html;
    location / {
            try_files $uri $uri/ @htmlext;
        }

        location ~ \.html$ {
            try_files $uri =404;
        }

        location @htmlext {
            rewrite ^(.*)$ $1.html last;
        }
    }
After running `docker-compose up` you have a static file serving server. You can try this by creating a file in the `src/`-folder and browsing to the domain specified.

## From GitLab CI to Server
The next step is to build the static html with pelican running on a GitLab CI pipeline and deploy it to your server via e.g. ssh.

To do so create a new repository and upload the source of your first blog post. I would recommend you start with `pelican-quickstart` and work on from there. 
Once you have your posts committed and pushed to your repository you are ready to add a GitLab CI pipeline. 
I added the following `gitlab-ci.yaml` to my repository.

    ::yaml
    stages: 
      - build
      - deploy
    image: python:3.7-stretch
    # Builds the HTML Code
    build:
        stage: build
        script:
            # Download the theme from GitHub
            - git clone --depth 1 https://github.com/Pelican-Elegant/elegant.git theme/
            # Download the plugins 
            - git clone --recursive --depth 1 https://github.com/getpelican/pelican-plugins.git plugins/
            # Install Requirements
            - pip install -r requirements.txt
            # Build the HTML
            - pelican -s publishconf.py
      artifacts:
        paths:
        - output/
        expire_in: 1 week 

    deploy:
        stage: deploy
        before_script:
          - 'which ssh-agent || ( apt-get update -y && apt-get install openssh-client git -y )'
          - eval $(ssh-agent -s)
          - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add - > /dev/null
          - mkdir -p ~/.ssh
          - chmod 700 ~/.ssh
          - ssh-keyscan yourdomain.com >> ~/.ssh/known_hosts
          - chmod 644 ~/.ssh/known_hosts
        script:
          - scp -r output/* username@yourdomain.com:/var/www/yourdomain.com/src

The first stage `build` installs all requirements and then builds the html with pelican. In the second step the finished files are transferred to the server via `scp`. To use this config you need to change `yourdomain.com`, `username`, filepaths and add your ssh private key (`SSH_PRIVATE_KEY`) to your GitLab CI variables. It is best to generate a new key-pair for this purpose. 
Do not forget to upload your public key to your servers `available_keys`.