# DSL_music 🎶 + 💻

This is a school project (from the subject "Implementation of Computational Methods"). This is basically a parser for a domain specific language (DSL), the
DSL is to create through the language the music you can imagine.

## About this project? 🔍

First of all, what is a DSL? A Domain Specific Language is basically a programming language for solving problems in a specific area, in this project, for music creation.
At least in this field, there are many DSLs with the same purpose, ie: Mutran, Mut, M (in fact, to make this project I relied on the Mut Lexicon and Grammar).


## What exactly does the code do? 🎯

Basically, the code is a basic compiler that allows us to create music (through code) with the DSL language.
The process is divided into four stages.
1. Read a file (with the exception of ".txt") containing the script
2. The program parses the lexemes in the script using ***Regex***
3. If there was no error, we start the syntax analysis, using the ***recursive descence***. 
4. And if everything is ok, then the program reproduce the music that you put in the file

If you want to know more technical aspects, you can read the [pdf](https://drive.google.com/file/d/1QFJCF8eRVqfNWzTA_WRxsCGYkeSiAfOa/view?usp=sharing) 📃 I wrote, 
where I described in more detail the functionality of each step and the logic of the solution.

Also, in that file you can see the grammar diagrams (for the grammar parser), the finite automaton diagram (for the lexical analyzer, the automaton was not programmed 
but was very useful for understand the lexems and through that create the regex expresions) and a video where explain the code and make video that explains the code 
and I test the code.

## How to use it? 🚩

It is easy to use, run the file *"evidencia1.py"*, the program will run. 

First it will ask you for the file to play, type it the filename (with or without the ".txt" extension), *the file must be in the same folder as the script, otherwise the program will never find the file.*

Once the program reads the file, it will start the lexical and grammar analysis, if there is an error in your "code", it will warn you and tell you in which line the error is on. 💬

If everything is fine, the program will play the song that you encoded. 🎵

## Limitations 💢
The code will play the music if you pass it a file with the correct sysntxis (in case of error, the program will warn you), the limitation is that the program just can play with one voice (in other words, only one instrument at the time).

Another limitation is that the amount of lexeme I use, it could limit the possible musical creations (the program has a very short lexicon).

## License 📖
MIT
