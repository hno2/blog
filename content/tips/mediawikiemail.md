---
title: How to add an E-Mail Adress to an existing Mediawiki-user
Tags: tech, tips, mediawiki, email
Date: 2019-11-05 12:15
summary: Easily add an email to an user account via the Media-Wiki maintenance scripts.
---

So I have the problem were I have several Media-Wiki-User without E-Mail. So if anyone of them forgets their password, they cannot reset this. 

Fortunately there is a quick and dirty solution to this. Use one of the maintenance scripts:

    ::bash
    php maintenance/resetUserEmail.php "username" email@adress.com