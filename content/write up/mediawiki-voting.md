---
author: Simon Klug
title: Using Mediawiki for your society
date: 2020-09-21
tags: MediaWiki, question, voting, society
summary: Knowing the past decisions of a society can be crucial. With MediaWiki and a couple of lines you can showcase these decisions with ease.
---


So a common issue when organizing your society is, that in some assembly you made a decision, but in the future, you forget what you decided on. 

That's why we use [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) to organize our information at the [UniTheater Karlsruhe](https://www.unitheater.de/). And since I am currently a memeber of the board, I thought I would be good idea to be able to have a record of all decisions made in the past. As all memebers can use this internal wiki there are pages for various topics and all meeting minutes are recorded here.

The good thing with MediaWiki is that it is very easy to write your own templates. So I created a template to collect all decisions in an organized manner, which I want to share with you.


## Creating a template
The idea is, whenever a decision is made you just add a template like this: 
{%raw%}

```
{{Decision|Question=Should Max Mustermann be selected best member ever?| Yes=13|No=1|Abs=2}}
```
So you create a new page for your meeting minutes and every time there is a decison with voting, just add this template and you are good to go.
## Creating a Template 
So in the backend of MediaWiki lets go ahead and create a new template for how this works internally.

```
<div style="background-color:#F0F0E7; border: solid 1px #cc9933; padding: 0.5em; padding-left:1em;">
'''Decision:''' {{{Question}}}</br>
({{{Yes}}}/{{{No}}}/{{{Ab}}}) [Yes/No/Abstention]
</div>
{{#subobject:
|Has question={{{Question}}}
|Has decision={{#ifexpr:{{{Yes}}}>{{{No}}}|Yes|No}}
}}
```
So in the first part with the `<div>` we create a "stylish" box with the decision and the votes. If you want you can play with the style to find one that fits for you.   
The second part creates a [subobject](https://www.semantic-mediawiki.org/wiki/Help:Type_Record/Record_vs._subobject) as part of Semantic MediaWiki. We add the question and, with the help of a quick `if`, wether the question was accepted or not. 
## Creating a decision collection
So in the final step, we want to create a page that displays all decisions in a meaningful manner. As we created subobjects for all our decisions we can go ahead and use the [`#ask`-Parser-Function](https://www.semantic-mediawiki.org/wiki/Help:Inline_queries#Parser_function_.23ask) a display all of these objects. With some quick formatting, we now have a nice and linked list of all decisions.

```
{{#ask:[[Has question::+]]
|mainlabel=minutes
|?Has question=Question
|?Has decision=Decision
|format=table 
|headers=plain
|link=subject
}}
```
{%endraw%}