# Homework 1 Corrections
Mitchell Harrison
POLSCI 427

### Question 4
I mistakenly used `n=1200` for the number of months to iterate, results in 
exponentially wealthier people than should have been. I've corrected it
to `n=120`, marking 10 years, not 100.

### Question 5
I did more than change existing parameters, I added two new ones that were
distributed identically to `bmean` and `bstdev`. In my original submission,
I noted that there appeared to be an infinite loop, but that is no longer
the case. The apparent infinite loop was actually just an increase in
runtime given the new parameters, but data is being generated correctly.

