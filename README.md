openLCA translation files
=========================
This repository contains the resources for the translation of openLCA to other 
languages. These files are also contained in the source code of the openLCA
application. The aim of this project is to provide translators just the files
they need to create or update a translation of openLCA. 

You can download this project as a 
[ZIP-file](https://github.com/GreenDelta/olca-translation-files/archive/master.zip) 
(see the Download ZIP button on the right side) or check it out via Git. The 
translation files are structured in folders which are described in the 
following. If you created a new version of a file, just send us your version of 
this file. If you are familiar with Git, you can also send us pull requests, 
patch files etc. Thank you!


app-messages and bundle-messages
--------------------------------
These folders contain Java property files which store translations as 
key-value-pairs. Both folders contain a file with the key-value-pairs for the
default language (i.e. messages.properties and bundle.properties). The 
translated versions have the same file name but the respective language code 
appended. In principle, these are just text files but encoded in ISO 8859-1 
with Unicode escape characters for characters that cannot be encoded in 
ISO 8859-1.

Fortunately, there is a very nice open source tool available with which it is 
really easy to manage these Java property files: 
[JLokalize](http://jlokalize.sourceforge.net/). Just open the default language
file in the respective folder with JLokalize and you can edit or add 
translations (see the JLokalize documentation). In order to run this tool, you 
need to have [Java](https://www.java.com) installed. 


start-page
----------
This folder contains the translated openLCA start pages. As for the other 
message files there is one file in the default language (start_page.html) and 
the translated files have the same name but the respective language code 
appended. 

The start page is a plain HTML page which you can open in your browser. Don't 
worry about the formatting and missing images this is added in the openLCA 
application. To add a translated start page, copy the start_page.html and use
it as a template. Edit the respective HTML page with an utf-8 enabled text 
editor with HTML syntax highlighting like 
[Notepad++](http://notepad-plus-plus.org/). Be careful to not modify the HTML
tags, CSS, and JavaScript but just edit the text (your editor should help you 
with this). You can always check the result when you open the file in your browser.


