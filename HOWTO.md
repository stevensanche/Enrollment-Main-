# HOWTO analyze course enrollment

The primary objective of this project is to introduce a fundamental 
loop idiom, the _accumulator pattern_, together with some ways of 
representing tabular data.  We will consider both _lists_ and 
_dictionaries_ as representations of tabular data.  We will use 
dictionaries (type `dict`)  in a version of the accumulator 
pattern, to keep counts of elements in a list.  We will also 
use a dictionary to expand abbreviated codes from a list. 


We will take data in the form of text files in the _comma separated 
values_ (CSV) format, which can be exported from many popular 
spreadsheet applications including Microsoft Excel and Google Sheets.
The data represents individual student enrollments in a computer 
science course (but stripped of individually identifiable 
information, for privacy).   As is often the case, the records 
contain some abbreviated codes (in this case, for academic major and 
class standing) which is not very meaningful by itself.  We will use 
additional data files to translate to make these codes more 
meaningful and useful.

## The raw data

The `data` directory contains input data for this project.  
The primary input data is `roster_selected.csv`, taken from the roster 
of a recent course offering.  Originally it had several columns,
including student names and emails, but we have removed columns that
could be used to identify individual students.  The order has also 
been scrambled to anonymize it.  The remaining data 
looks like this: 

```csv
Class,Major
FR,DSCI
JR,CIS
JR,GSS
SO,CIS
JR,CIS
SO,CS
SO,CIS
SO,DSCI
SO,CIS
JR,DSCI
SO,CIS
SO,CIS
JR,CS
JR,EXPL
SR,CINE
SO,GEOG
```

Although this is just a text file, we will refer to it as a _table_ 
with two columns.  The first column is class standing (e.g., "SO" 
for "sophomore").  The second is column is major, represented by 
abbreviations like "DSCI" for "data science" and "cine" for "cinema 
studies".  We think of each line as a row of the table.  The first 
row contains headers, or names of the columns. 

A second file, `programs.csv`, is taken from a list of programs 
including majors at the same university.  It looks like this: 

```csv
Code,Student Type,Type,Program Name,School,Degree(s),Status,Active Term,Inactive Term,End Term,Campus,Note
ABAO,graduate,majors,Applied Behavior Analysis,ED,M.S.,active,202201,,,,Online
ACTG,undergraduate,majors,Accounting,BUS,"B.A., B.S.",active,,,,,
ACTG,graduate,majors,Accounting,BUS,"Ph.D., M.Actg.",active,,,,,
ADBR,graduate,majors,Advertising and Brand Responsibility,SOJC,"M.A., M.S.",active,201701,,,,
ADPD,undergraduate,minors,Audio Production,SOMD,,active,201701,,,,
ADSL,graduate,specializations,Advanced Strategy and Leadership,BUS,,active,201701,,,,
AFR,undergraduate,minors,African Studies,CAS,,active,,,,,
ALAW,graduate,majors,American Law,LAW,LL.M.,active,201401,,,,
AMAN,undergraduate,majors,Arts Management,DSGN,"B.A., B.S.",inactive,,202201,202804,,
AMGT,graduate,majors,Arts Management,DSGN,"M.A., M.S.",inactive,,202201,202804,,
PCIS,undergraduate,pre-majors,Pre-Computer & Information Science,CAS,,inactive,,202001,202604,,
```

As in the other CSV file, the first line of this file is column 
headings.  As is typical of real-world data, it contains many 
columns and many rows that are not relevant to us.  For example, we 
will not be concerned with the fact that the Accounting program 
offers Ph.D. and Masters degrees, and we will not encounter Audio 
Production (ADPD) as it is a code for a minor concentration rather 
than a major.  Records for the same code may appear multiple times 
when undergraduate and graduate degrees or majors and minors are 
offered in the same discipline. 

Our results will combine information from `programs.csv` with 
information from `roster_selected.csv`. 

## Desired output

The output should summarize enrollment numbers by major.  It will 
look like this: 

```commandline
  40 Computer and Information Science
  36 Computer Science
  20 Data Science
  14 Exploring
  11 Business Administration
   8 Mathematics and Computer Science
   8 Physics
   7 Mathematics
    ... 
   1 Journalism
   1 Art and Technology
   1 Multidisciplinary Science
   1 Chemistry
```

## Do we really want to use plain Python? 

There are several ways we could tackle this problem.  An expert user 
of a spreadsheet application like Excel or Google Sheets could do it 
entirely within a spreadsheet app.  Someone expert in the use of the 
R language for statistical computation might choose that.  A data 
scientist might use the Python Pandas package and/or the Anaconda 
distribution for scientific computing in Python.  Each of these 
choices might be appropriate in some contexts.  For example, if nice 
graphic displays were important, the Anaconda distribution might be 
preferable to the version of Python that we will use.

However, the task at hand does not _require_ Anaconda or Pandas. The 
standard distribution of Python is adequate.  Building it in Python 
provides some flexibility compared to working entirely in a 
spreadsheet, and is likely to be less work if we want to use the 
same analysis on different data sets (whereas it can be difficult to 
disentangle data from its analysis in a spreadsheet).  So our 
approach is not the _only_ reasonable approach, it is one reasonable 
approach for someone who is not already committed to R, Pandas, or 
Anaconda. 

## Steps

We know we will need to do the following, in some order: 

- Read data from CSV files, either to process line by line or to keep 
  in some data structure.
- Associate codes from the "Major" column in `roster_selected.csv` with
  corresponding codes from the "Code" column in `programs.csv`
  to find program names corresponding to each major code.  
  For example, if we see `SO,ESCI` in roster file, we will want to find
  the code "ESCI" from a record in the programs file to find that
  "ESCI" stands for "Environmental Science".  
- Count the number of rows containing each major.
- Sort the data so that we can print the majors with the largest 
  counts first. 

We will surely want to write functions for at least some of these 
tasks, and we may want to break them down farther into smaller 
functions.  As usual, it is not immediately obvious which functions 
we will need to develop, or in what order. 

## Data structure selection

The _data structures_ most appropriate for a set of data depend on 
how we plan to use them, that is, the operations we plan to perform 
in our _algorithms_.  Conversely, different algorithms may be 
preferable depending on which data structures we choose.  We must 
choose them together.  How? 

A good approach is to start by sketching an algorithmic approach in 
an abstract form.  "Abstract" means that they can be implemented in 
different ways, i.e., that we postpone commitment to some 
particulars. For example, we can sketch the algorithm in 
[_pseudocode_](https://en.wikipedia.org/wiki/Pseudocode)
rather than Python.  Pseudocode is not a programming 
language per se, nor is it narrative text in a natural language like 
English. 
Pseudocode is a sort of 
hybrid in which we write down steps, loops, etc., in roughly the 
form of a program, but designed for human reading. Critically, when 
we do not wish to make a commitment to some detail (like the exact 
form of a data structure), we write them with just enough detail to 
explain what they must accomplish, without specifying how it will be 
done.  

Wikipedia describes pseudocode this way: 

> A programmer who needs to implement a specific algorithm,
> especially an unfamiliar one, will often start with a pseudocode
> description, and then "translate" that description into the target
> programming language and modify it to interact correctly with the
> rest of the program. Programmers may also start a project by
> sketching out the code in pseudocode on paper before writing it in
> its actual language, as a top-down structuring approach, with a 
> process of steps to be followed as a refinement. 

Two parts of our list of "things we will need to do" stand out as 
likely requiring consideration that could impact the choices made 
for all the other steps: 

- Associate codes from the "Major" column in `roster_selected.csv` with
  corresponding codes from the "Code" column in `programs.csv`
  to find program names and schools corresponding to each major code.  

- Count the number of rows containing each major.

### An admission

This HOWTO will walk you through an approach that works and that 
does not require too much magic (i.e., code that I am not ready to 
explain yet).  It is not the first approach I tried.  

You may get 
the impression that a programmer makes a bunch of good choices, and 
things just work the first time.  In fact, even very good 
programmers with decades of experience make lots of preliminary 
decisions that turn out to be wrong choices.  They may be "wrong" in 
the sense that they just don't work at all, but more often they are 
"wrong" in the sense that they make the program more complex than it 
needs to be.  That was certainly the case with this project.  If you 
wonder "how did the author know to make that choice?", the real 
answer is "by trying several other things first, slowly whittling 
away unnecessary complexity."  

Collections and loop design are hard enough already, so I'm hiding 
all the other things I tried before settling on this approach. 


### Looking up major codes

The first task, finding program names associated 
with codes, is conceptually straightforward:  We are given a _key_ 
that appears in one column of the table, and we want one or more 
_values_ from other columns of the table.  Since they key will be a 
string, a straightforward and efficient way to handle this task will 
be to keep the table as a Python `dict` structure. 

There is one complication, however:  A `dict` must have unique keys. 
The `programs.csv` file, on the contrary, may have more than one row 
with the same major code, like this: 

```csv
ENV,undergraduate,majors,Environmental Studies,CAS,"B.A., B.S.",active,,,,,
ENV,undergraduate,minors,Environmental Studies,CAS,,active,,,,,
ENV,graduate,majors,Environmental Studies,CAS,"M.A., M.S.",active,,,,,
```

Does it matter? The columns we will use are the full name of the 
major (e.g., "Environmental Studies") and the school (e.g., "CAS").  
We might expect that these would always be the same for a single 
major code.  Looking through the file, this appears to be the case. 
We can use any row with a given major code, such as the first or 
last such row we encounter.

We will write pseudocode assuming that looking up a major code is as 
simple and efficient as looking in a dict.  We will need a function 
to create the dict, but we may not need a separate function for the 
lookup. 

We will want to build a structure that is conceptually a table with 
two columns, keys and values.  Major codes like "DSCI" will be the 
"key" column, and program names like "Data Science" will be the 
values. Conceptually it will look like this:

| Code | Program Name |
|------|--------------|
| ENV  | Environmental Studies |
| DSCI | Data Science   |
| CS   | Computer Science |
| BADM | Badminton |
| GSS | General Social Science |

Because we will want to quickly find the values by key, we will 
represent this table as a `dict`: 

```python
{'ENV': 'Environmental Studies', 'DSCI': 'Data Science', 
 'CS': 'Computer Science', 'BADM': 'Badminton', 'GSS': 'General Social Science' }
```

Considering the form of the input data, which has many additional 
fields, we will probably want to read just selected fields of each 
line into the dict structure. 

### Individual Majors

The information we need from the roster is just the major code for 
each student.  For example, we might have 

| Major  |
|--------|
| CS     |
| DSCI   |
| GSS    |
| CS     |
| DSCI   |
| BADM   |

We can represent this single-column table very simply as a list

```python
['CS', 'DSCI', 'GSS', 'CS', 'DSCI', 'BADM']
```

### Summarizing by Major

The entries are not unique (e.g., "CS" appears more than once), but 
we cannot just ignore duplicates.  Instead, we will want to count 
occurrences of each value to produce a table like this:

| Major  | Count |
|--------|-------|
| DSCI   | 2     |
| CS     | 2     |
| BADM   | 1     |
| GSS    | 1     |

It would be straightforward to represent this table as a `dict`:

```python
{ 'DSCI': 2, 'CS': 2, 'BADM': 1, 'GSS': 1 }
```

There are at least two ways we could do this.

### Approach 1:  Sort and summarize

Counting rows with the same major code would be fairly easy if we 
first sorted the table by major code, thereby grouping rows with the 
same major code.  

| Major |
|-------|
| CS    |
| CS    |
| DSCI  |
| DSCI  |
| BADM  |
| GSS   |

We could write a loop that keeps a count for each contiguous group 
of like elements.  We could build either a list or a dict to hold 
the (major code, count) pairs.

### Approach 2:  Summarize in a dict

Another approach is to build a dict in which the _key_ 
elements are major codes and the _value_ elements are counts.  We 
would not have to sort the list of major codes, because we can 
access the elements of the dict in any order.  

As we loop through each element of the list of majors, we can
look in a table of 
counts for an entry for the current major code. If there is no entry 
for that major code, we can create one and initialize its value to 1.
If there is already a count for that major code, we can add 1 to it. 

Either of these approaches seems fine.  We'll choose approach 2, 
summarizing into a `dict`, but you may wish to try the other 
approach as well. 

With these decisions, we can sketch our overall application in 
pseudocode: 

```pseudocode
Read roster CSV file into a single list with major codes. 
Count elements in list of major codes, keeping a summary in a dict 
that maps major code to count. 
Sort the (major code, count) elements from the dict, giving a list 
from largest count to smallest. 
Read program CSV file into a dict that maps program codes (the same 
as major codes) into program names. 
For each (major code, count) pair,  
    look up major code to get program name
    print count and program name
```

We could combine some steps, for example summarizing majors into 
counts while we read the CSV file.  Let's not.  Breaking it down 
into smaller steps gives us a better chance of writing functions 
that we can reuse for other purposes.  For example, the function 
that reads major codes from the CSV file could also work to read 
class standings.  We wouldn't have to change anything else in the 
program to get a ranked list of class standings of students in a class.

## Order of development

We'll start with a skeleton consisting 
of just the file header, an import of the `doctests` module, and the 
boilerplate for invoking the tests. 

```python
"""Enrollment analysis:  Summary report of majors enrolled in a class.
CS 210 project, Fall 2022.
Author:  Your name here
Credits: TBD
"""
import doctest


def main():
    doctest.testmod()

if __name__ == "__main__":
    main()
```

As in prior projects, we want to choose a development order that 
allows us to build and test one function at a time.  Most of our 
tasks involve doing something with tables (which may be lists or 
dictionaries), so it makes sense to start with a function that reads
a CSV file into a table. 

### Read one column from a CSV file

Our pseudocode sketch calls for reading just the major codes from 
`roster-selected.csv` into a list.  Rather than specialize our 
function to reading major codes from this particular CSV file, we'll 
make a more generally useful function for reading one selected 
column from any CSV file that starts with column headers: 

```python
def read_csv_column(path: str, field: str) -> list[str]:
    """Read one column from a CSV file with headers into a list of strings."""
```

Is this testable?  It can be, but it requires a little extra work.  
Testing it on the real `roster_selected.csv` file would require a 
very long doctest comment, which would moreover fail if we tried it 
with a different roster file.  Instead, I have created a much 
shorter test input called `test_roster.csv`, just for use in doctests: 

```
Note,Class,Major
From CAS,FR,DSCI
From CAS,JR,CIS
From Business,JR,BADM
From Business,JR,BIC
From CAS,SO,CIS
From CAS,JR,GSS
```

I have purposely added a "Note" column that is not in the real 
roster file, because I want to be sure the function relies only on 
the column headers and not on the layout of the CSV file.  With this,
I  can write a short but useful test case: 

```python
def read_csv_column(path: str, field: str) -> list[str]:
    """Read one column from a CSV file with headers into a list of strings.

    >>> read_csv_column("data/test_roster.csv", "Major")
    ['DSCI', 'CIS', 'BADM', 'BIC', 'CIS', 'GSS']
    """
```

We can use the 
[CSV module](https://docs.python.org/3/library/csv.html) for reading.
Just after 

```import doctest``` 

add

```import csv``` 

to import the CSV  module. As our CSV files start with a row 
containing column headers, 
you can use a `DictReader` object. The `DictReader` class is described
in the CSV module documentation.
It treats the header row of the CSV file specially, letting us use
column headings as keys to get the fields we want from a row.  

The CSV module documentation 
provides an example of reading and printing the names of Monty 
Python cast members with a `DictReader`.  You can use that as a 
starting point, opening the value of `path` instead of `names.csv`, 
and building a list instead of printing names. 

### Count element values

The next line of our pseudocode sketch says we need to use the list 
produced by `read_csv_column` to produce a table of counts, 
represented as a `dict` in which the keys are major codes like "CIS" 
and the values are integers.  Here is the function header, with a 
test case: 

```python
def counts(column: list[str]) -> dict[str, int]:
    """Returns a dict with counts of elements in column.

    >>> counts(["dog", "cat", "cat", "rabbit", "dog"])
    {'dog': 2, 'cat': 2, 'rabbit': 1}
    """
```

To implement this function, you will need to loop through the 
elements of `column` while building up the `dict` object.  Before 
the loop, you will need to initialize the value of the variable that 
will hold the `dict`.   You 
can use a Python `for` loop to inspect each element of `column`.  

Within the body of the loop, you must consider two cases for the 
major code in each element: 

- This is the first occurrence of that major code.  You will need to 
  set the count for that code to 1. 

- There is already a count of 1 or more for that major code.  You 
  will need to increase it by 1. 

Don't forget to return the `dict` _after_ the loop. 

### Start integrating

When your `read_csv_column` and `counts` functions are working, you 
will already be able to make a simplified version of the main 
program that prints major counts, although so far you will be 
printing codes rather than program names, and they will not be in 
the desired order.  

```python
def main():
    doctest.testmod()
    majors = read_csv_column("data/roster_selected.csv", "Major")
    counts_by_major = counts(majors)
    key_val_pairs = counts_by_major.items()
    for key_val in key_val_pairs:
        code, count = key_val
        print(count, code)
```

This code works, but we can make it shorter.  The call on
`counts_by_major.items()` can be combined 
with the `for` loop over those (key, value) pairs.  The
extraction of `code` and `count` from a (key, value) pair
can also be combined in the same statement with the `for` loop header:

```python
    for code, count in counts_by_major.items():
        print(count, code)
```

Is this better or worse?  I like it better because we have not only 
made the code a little shorter, but also eliminated a few variables 
like `key_val_pairs`.  I find it more readable, but that is partly 
because I am familiar with this pattern for `for` loops in Python.  The 
balance between making code shorter and keeping each step clear may 
vary somewhat from programmer to programmer.  It will also change 
over time as you gain experience.  Stick with what you find readable 
and understandable. 

### Converting major codes to program names

To get from 

```commandline
36 CS
14 EXPL
2 CINE
```

to 

```commandline
36 Computer Science
14 Exploring
2 Cinema Studies
```

we will need to use the `programs.csv` file.  Instead of reading one 
column, we will need to read two:  One ("Code") to use as the key of 
a `dict`, and another ("Program Name") to use as the value 
associated with a key.  The header of our function will look like this: 

```python
def read_csv_dict(path: str, key_field: str, value_field: str) -> dict[str, dict]:
    """Read a CSV with column headers into a dict with selected
    key and value fields.

    >>> read_csv_dict("data/test_programs.csv", key_field="Code", value_field="Program Name")
    {'ABAO': 'Applied Behavior Analysis', 'ACTG': 'Accounting', 'ADBR': 'Advertising and Brand Responsibility'}
    """
```

Again I have created a short test data file (`test_programs.csv`) 
for testing.  Like `read_csv_column`, this function will initialize 
the result, then loop through each line using a `DictReader`.  We 
won't bother checking whether there is already an entry for a given 
major code, as replacing it with the same values won't hurt anything.
You may want to start by copying the body of `read_csv_column`.
Then modify the copy to read two columns instead of one. 
After extracting the `key` and `val` strings from a row of the CSV 
table, update the `dict` with an assignment like this:

```python
table[key] = val
```


When `read_csv_dict` is working correctly, we can integrate it into 
our main function: 

```python
def main():
    doctest.testmod()
    majors = read_csv_column("data/roster_selected.csv", "Major")
    counts_by_major = counts(majors)
    program_names = read_csv_dict("data/programs.csv", "Code", "Program Name")
    for code, count in counts_by_major.items():
        program = program_names[code]
        print(count, program)
```

Now we should get something like this: 

```commandline
20 Data Science
40 Computer and Information Science
1 General Social Science
36 Computer Science
14 Exploring
...
```

### Sort by count

We are almost there, but it would be nice if the list were in order 
from most majors to fewest.  Python provides a built-in `sorted` 
function (which returns a sorted copy of a list) and a `sort` method 
for type `list` (which modifies the list), so it seems 
straightforward.  The tricky bit is 
that we want to sort by count, from largest to smallest.  We can 
extract a list of (major code, count) tuples by calling
`counts_by_major.items()`, but if we sort that list we will order 
them by major code, rather than by count.

The simplest ways to sort a collection using a key of our choice 
involve features that we haven't explored yet.  Let's try to do it 
with tools we already have.  If we try to sort a 
list of lists or a list of tuples, Python's `sorted` function will 
treat the first element in each sublist or tuple as more important 
than subsequent items, so for example

```python
sorted([(5, "q"), (3, "a"), (4, "m"), (2, "z")])
```

produces

```python
[(2, 'z'), (3, 'a'), (4, 'm'), (5, 'q')]
```

We've already seen how to loop through keys and values of a `dict`.  
Let's use one loop to create a list of tuples that begin with counts. 
We can then sort that list, then loop through it again for printing. 

```python
def main():
    doctest.testmod()
    majors = read_csv_column("data/roster_selected.csv", "Major")
    counts_by_major = counts(majors)
    program_names = read_csv_dict("data/programs.csv", "Code", "Program Name")
    # Convert to list of (count, code)
    by_count = []
    for code, count in counts_by_major.items():
        pair = (count, code)
        by_count.append(pair)
    by_count.sort(reverse=True)  # From largest to smallest
    for count, code in by_count:
        program = program_names[code]
        print(count, program)
```

This produces the desired output, but our `main` program is getting a 
bit long and harder to read.  I want you to _refactor_ it by writing a 
separate function for extracting a list of (value, key) pairs from a 
dict.  When you have created that function, which you will call 
`items_v_k`, the following `main` program should produce the desired 
output: 

```python
def main():
    doctest.testmod()
    majors = read_csv_column("data/roster_selected.csv", "Major")
    counts_by_major = counts(majors)
    program_names = read_csv_dict("data/programs.csv", "Code", "Program Name")
    # --- Next line replaces several statements
    by_count = items_v_k(counts_by_major)
    # ---  
    by_count.sort(reverse=True)  # From largest to smallest
    for count, code in by_count:
        program = program_names[code]
        print(count, program)
```

Note that `items_v_k` is _not_ specific to counts of majors.  It is 
more general:  It returns a list of (value, key) pairs for _any_ 
dict.   Thus variable names like `count` are not appropriate.  You 
can start by copying some code from the prior version of `main`, but 
rework it to use appropriate variable names.  Also provide a 
suitable header comment and doctest. 

## Recap

Summarizing collections of structured data is a very common task in 
programs.  Often non-programmers solve problems like this one using 
spreadsheets like Microsoft Excel or Google Sheets.  Sometimes those 
spreadsheets are very large, very hard to maintain, and often buggy. 
Large collections of numerical data, on the other hand, are 
increasingly analyzed using tools like Python Pandas, Numpy, or the 
R statistical programming language.

We have applied some basic programming techniques in summarizing 
structured data: 

- We used the comma-separated-values (CSV) format, a data exchange 
  format 
  that can produced by spreadsheets and many other applications.  We 
  read CSV files using Python's `csv` module.  

- We represented tabular data in multiple forms, including 
  dictionaries (type `dict`) and lists 
  (type `list`) of strings and of tuples (type `tuple`).

- We summarized data by counting occurrences of distinct values.  
  This is a variation on the fundamental _accumulator pattern_, 
  which you will use often in many different ways.

- We used a _destructuring assignment_ to extract elements from
  tuples, and used destructuring in a `for`loop to loop 
  through keys and values together (`for count, code in by_count:`). 

- We sorted a list of tuples to put the output in the right order. 

In addition, we continued to build skills in constructing and using 
functions.  In particular: 

-  We wrote the functions for this application in a sufficiently 
   general way that they could be used to summarize other tabular 
   data.  For example, if we chose to count enrollment by class 
   standing rather than major, only the `main` function would need 
   to change. 

- We built test cases for functions that use external data by 
  providing additional small data sources just for testing. 

- You were asked to come up with the header as well as the body for 
  `items_v_k`, to build skill in creating clear function interfaces 
  including test cases. 

## Challenge yourself

If you would like to explore further after finishing the project, 
consider testing the extent to which we have really succeeded in 
making our functions _general_.  How hard would it be to make this 
program summarize counts by class standing instead of major?  What 
if you wanted to apply the program to different data files?   How 
might you improve the program to make it more useful for analyzing 
enrollment in other classes?  