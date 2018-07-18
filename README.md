# muffins
This program takes as input two LaTeX files containing the procedures for dividing a certain number of muffins among
students. The output is a general procedure. 

### procgen.py
Given a procedure for f(NA + M, N) and f(NB + M, N), generates procedure for f(Nk + M, N), where N, M, A, and B are constants and k is a variable.

#### usage:
Run get_general(file1, file2) where file1 and file2 are strings containing the filenames for specific procedures.

###### OR

Run get_general_give_only(file1, file2) where file1 and file2 are strings containing the filenames for specific
procedures composed of only "Give N students $\[A:B]$" lines. No other formatting lines necessary. Outputs a full general procedure.

### re_proc.py
re_parse(proc_file, k) takes the name of a file containing a general procedure and a value of k and outputs a file with all the
formulas evaluated for the given k.
