---
author: Simon Klug
title: Let's make this blog faster 
date: 2021-03-15
tags: tech
summary: The speed of a webpage is essential. Using a static site generator and some manual tweaking one can achieve faster loading with less data. A writeup for better text-based blogs.  
---


This blog has undergone a big facelift.

I finally got rid of any external CSS or JavasScript. This means it does not only load much faster, gets 100 in all categories of [Google Lighthouse](https://developers.google.com/web/tools/lighthouse/) and is safer by not using any JavaScript or common libraries. But in the end, the goal is that readers and myself, the writer can focus on content and content alone.


Before I used the [Elegant Theme](https://github.com/Pelican-Elegant/elegant) for Pelican, which was ok, but overkill for my simple site. So here is a quick write-up of the steps I took and how I updated my site.


## Inspiration

Text and Content first is the pivot point for a blog. Therefore there are no colors so readers can focus on only the content.
The Inspiration for the Design comes from the Blog of [Tom MacWright](https://macwright.com/): A simple navigation on the left, content as the biggest blog in the middle and nothing else. 


## Backend for Static Sites

I do not want to care about style,  I just want to write my posts in Markdown, that's it. 
So I use a static website generator named [Pelican](https://blog.getpelican.com/). It simple to use and it is written in Python, my favorite ecosystem. 

Also writing the [template/theme](https://github.com/hno2/blog/tree/main/theme) with Jinja is awesome and super easy.
There are also a couple of Plugins I use, that generate a Sitemap, Citation & Bibliography from Bibtex and Math with KaTex. 
In the end, I do not have to care about anything except writing content. Awesome!

Using a GitHub Action any commit will automatically generate the HTML and push the output to my webserver via ssh.

## Structure for Speed
Using inline CSS and no javascript means that your browser needs no extra requests to load this page
The main CSS is minimal and therefore text-only pages stay under 10kb.
I set up the theme to add the CSS for code highlighting and for nice math with KaTex only when needed. 


## Server
I use traefik with an Nginx docker container and finetuned the configuration of Nginx. This means adding Security Headers, to prevent different attacks like Cross-Site Scripting. I cannot recommend the [security headers](https://securityheaders.com/?q=simonklug.de&followRedirects=on) tool by Scott Helme enough, to check if your website follows best practices. 

There is only one thing that is bugging me that I have to set the `Content-Security-Policy` header to allow inline CSS (with `style-src: unsafe-inline`). I still have to check out the tradeoff between inline CSS and one extra CSS file loaded. 


HTTPS is a no-brainer now and is supported by [Let's Encrypt.](https://letsencrypt.org/)

## Next Steps
I will work on moving my pictures to inline SVGs whenever possible, I also think about integrating some sort of Comments-Tool (maybe [Utterances](https://utteranc.es/), but ugh to JavaScript...). 


**But in the end it is all about writing more...**