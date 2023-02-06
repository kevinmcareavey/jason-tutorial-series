# Tutorial 2 - Logic programming

This tutorial provides a brief introduction to logic programming using the [SWISH](https://swish.swi-prolog.org/) web interface for [SWI-Prolog](https://www.swi-prolog.org/), which is a popular implementation of [Prolog](https://en.wikipedia.org/wiki/Prolog).

<!-- TOC -->

## Getting started

### Step 1 - Launch SWISH

Open [SWISH](https://swish.swi-prolog.org/) in a web browser.

![Figure](figures/swish-1.png)

The interface for SWISH is divided into three panels:

- **Program panel** on the left allows you to create and edit Prolog programs
- **Query panel** on the bottom-right allows you to input queries to your Prolog program
- **Results panel** on the top-right displays the results from your queries

### Step 2 - Create a new program

In the program panel ensure that **Empty** is checked and then select **Program**.

![Figure](figures/swish-2.png)

### Step 3 - Add some code

Add the following Prolog code to the program panel:

```prolog
% Facts

female(alice).
female(carol).
female(eve).
female(grace).
female(heidi).
female(judy).
female(peggy).
female(wendy).

male(bob).
male(dave).
male(frank).
male(ivan).
male(mike).
male(oscar).
male(rupert).
male(ted).
male(victor).

parent(dave, alice).
parent(dave, bob).
parent(eve, alice).
parent(eve, bob).
parent(ivan, carol).
parent(ivan, dave).
parent(heidi, carol).
parent(heidi, dave).
parent(mike, eve).
parent(mike, frank).
parent(judy, eve).
parent(judy, frank).
parent(peggy, grace).
parent(peggy, ivan).
parent(rupert, grace).
parent(rupert, ivan).
parent(ted, judy).
parent(ted, oscar).
parent(victor, judy).
parent(victor, oscar).
parent(wendy, judy).
parent(wendy, oscar).
```

![Figure](figures/swish-3.png)

The expression `parent(dave, alice)` is an example of a **fact**:

- `parent(dave, alice)` means that Alice is a parent of Dave
- `female(alice)` means that Alice is female
- `male(dave)` means that Dave is male

> **Note:** You might wonder why we used `parent(dave, alice)` rather than `parent(alice, dave)` to mean that Alice is a parent of Dave. This is just a design choice. Either option is valid as long as you pick one and use it consistently throughout your Prolog program.

The term `alice` is an example of an **atom**, and the symbol `parent` is an example of a **predicate**. A predicate describes a property or relation over zero or more **terms**, where an atom is one kind of term.

The expected number of terms for a predicate is called its **arity**. When referencing a predicate it is common to include both the symbol and the arity separated by the `/` (backslash) symbol, e.g. `female/1`, `male/1`, and `parent/2`.

The symbol `%` denotes the start of a **comment**. Comments are ignored by the Prolog interpreter.

### Step 4 - Save your program

Select **File > Save**, uncheck the **Public** option, and select **Save**.

![Figure](figures/swish-4.png)

A random name will be automatically assigned to your Prolog program as shown in the tab name.

You can use this save function and the generated URL to return to your Prolog program in the future.

## Queries

### Step 5 - Simple queries

In the query panel enter `parent(dave, alice)` and select **Run!**.

![Figure](figures/swish-5.png)

The query result `true` means it can be proved from your Prolog program that Alice is a parent of Dave.

Change the query to `parent(alice, dave)` and select **Run!** again.

![Figure](figures/swish-6.png)

The query result `false` means it cannot be proved from your Prolog program that Dave is a parent of Alice.

> **Note:** Results from previous queries will remain in the results panel until they are manually closed.

### Step 6 - Queries with variables

Change the query to `parent(dave, X)` and select **Run!**.

The first query result should be `X = alice`. Select **Next** under the query result to cycle through the remaining results.

![Figure](figures/swish-7.png)

The term `X` is an example of a **variable**. A Prolog interpreter answers queries by **instantiating** variables with other terms (e.g. atoms) such that the instantiation can be proved from the Prolog program.

Variables always start with an **uppercase letter**.

The query `parent(dave, X)` can thus be read as: **who is a parent of Dave?**

The query results `X = alice` and `X = bob` can then be read as: **Alice and Bob are parents of Dave.**

Change the query to `parent(X, dave)` and select **Run!**.

The first query result should be `X = ivan`. Select **Next** under the query result to cycle through the remaining results.

![Figure](figures/swish-8.png)

This example demonstrates that positioning of terms is significant and that consistent usage is required to correctly ascribe meaning to your Prolog program.

The query `parent(dave, X)` should thus be read as: **who has Dave as a parent?**

The query results `X = ivan` and `X = heidi` can then be read as: **Ivan and Heidi have Dave as a parent.**

### Step 7 - Queries with the anonymous variable

Change the query to `parent(_, alice)` and select **Run!**.

![Figure](figures/swish-9.png)

The term `_` (underscore) is called the **anonymous variable**. It can be used in place of a standard variable when you want to check if an instantiation **exists** but do not care about the instantiation itself.

The query `parent(_, alice)` can thus be read as: **is Alice a parent?**

Change the query to `parent(_, _)` and select **Run!**.

![Figure](figures/swish-10.png)

The query `parent(_, _)` can be read as: **does a parent exist?**

This query of course is not particularly informative, but is valid nonetheless.

## Rules

### Step 8 - Simple rules

Add the following code to the bottom of your Prolog program:

```prolog
% Rules

child(X, Y) :- parent(Y, X).
```

The expression `child(X, Y) :- parent(Y, X)` is an example of a **rule** with `child(X, Y)` called the **head** and `parent(Y, X)` called the **body**. The rule can be read as: **`Y` is a child of `X` if `X` is a parent of `Y`** or, equivalently, **if `X` is a parent of `Y` then `Y` is a child of `X`**.

In the query panel enter `child(dave, X)` and select **Run!**. The query results should be `X = ivan` and `X = heidi`. In other words, Ivan and Heidi are children of Dave.

This matches the intuitive meaning of the previous query `parent(X, dave)` where the results said that Ivan and Heidi have Dave as a parent.

> **Note:** It should be obvious that this rule is a simple rewrite of the `parent/2` predicate. In some instances this kind of rewriting may aid readability, but it many instances it has the opposite effect: cluttering your Prolog program with redundant rules. We are typically interested in rules that are more informative.

### Step 9 - Conjunction

Add the following rules to the bottom of your Prolog program:

```prolog
mother(X, Y) :- parent(X, Y), female(Y).

father(X, Y) :- parent(X, Y), male(Y).
```

The symbol `,` (comma) in Prolog denotes conjunction. The first rule can thus be read as: **if `Y` is a parent of `X` and `Y` is female then `Y` is a mother of `X`**.

In the query panel enter `mother(dave, X)` and select **Run!**. The query result should be `X = alice`.

### Step 10 - Relational expressions

Add the following rule to the bottom of your Prolog program:

```prolog
sibling(X, Y) :- parent(X, Z), parent(Y, Z).
```

In the query panel enter `sibling(dave, X)` and select **Run!**. The query result should be `true`.

Now enter `sibling(dave, dave)` and select **Run!**. The query result should again be `true`, which implies that Dave is a sibling of himself.

This of course is not the result we want. The reason for the result is that, while Prolog prohibits **different instances of the same variable** within a rule (e.g. `Z`) from having **different instantiations**, it does not prohibit **different variables** (e.g. `X` and `Y`) from having the **same instantiantion**.

To achieve the desired result we must therefore explicitly enforce an inequality within the rule.

Update the rule as follows:

```prolog
sibling(X, Y) :- parent(X, Z), parent(Y, Z), X \== Y.
```

In the query panel enter `sibling(dave, eve)` and select **Run!**. The query result should be `true`.

Now enter `sibling(dave, dave)` and select **Run!**. The query result should be `false`, which is the result we want.

The expression `X \== Y` is an example of a **relational expression**. Prolog supports several kinds of relational expressions, with the most common being:

- `X == Y` evaluates to true if terms `X` and `Y` are **equal**
- `X \== Y` evaluates to true if terms `X` and `Y` are **not equal**
- `X = Y` evaluates to true if terms `X` and `Y` **unify**
- `X \= Y` evaluates to true if terms `X` and `Y` **do not unify**

### Step 11 - Arithmetic expressions

Add the following facts below your existing facts:

```prolog
age(alice, 91).
age(bob, 92).
age(carol, 61).
age(dave, 62).
age(eve, 63).
age(frank, 64).
age(grace, 31).
age(ivan, 32).
age(heidi, 33).
age(mike, 34).
age(judy, 35).
age(oscar, 36).
age(peggy, 1).
age(rupert, 2).
age(ted, 3).
age(victor, 4).
age(wendy, 5).
```

Notice that the second term in `age/2` is always a **number**.

In the query panel enter `age(oscar, X)` and select **Run!**. The query result should be `X = 36`.

In the query panel enter `age(peggy, X)` and select **Run!**. The query result should be `X = 1`.

Add the following rule below your existing rules:

```prolog
adult(X) :- age(X, Y), Y >= 18.
```

In the query panel enter `adult(oscar)` and select **Run!**. The query result should be `true`.

In the query panel enter `adult(peggy)` and select **Run!**. The query result should be `false`.

Most standard arithmetic expressions (e.g. `X > Y`, `X < Y`, `X <= Y`) can be used in a similar manner, assuming that `X` and `Y` are numbers.

### Step 12 - Negation

Add the following rule to the bottom of your Prolog program:

```prolog
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

cousin(X, Y) :- grandparent(X, Z), grandparent(Y, Z), X \== Y.
```

In the query panel enter `grandparent(ivan, X)` and select **Run!**. Next enter `grandparent(mike, X)` and select **Run!**. The results for both queries should be `X = alice` and `X = bob`.

In the query panel enter `cousin(ivan, mike)` and select **Run!**. The query results should be `true`, as expected, since we know that Ivan and Mike share the same grandparents Alice and Bob.

In the query panel enter `cousin(ivan, heidi)` and select **Run!**. The query results should be `true`, but this is not what we want since although Ivan and Heidi share the same grandparents, they also share the same parents (and thus are siblings rather than cousins).

Update the second rule as follows:

```prolog
cousin(X, Y) :- grandparent(X, Z), grandparent(Y, Z), not(sibling(X, Y)), X \== Y.
```

In the query panel enter `cousin(ivan, mike)` and select **Run!**. The query results should be `true`.

In the query panel enter `cousin(ivan, heidi)` and select **Run!**. The query results should be `false`, which is the result we want.

### Step 13 - Disjunction

Add the following rule to the bottom of your Prolog program:

```prolog
immediate_family(X, Y) :- parent(X, Y); child(X, Y); sibling(X, Y).
```

The symbol `;` (semi-colon) in Prolog denotes disjunction. The rule can thus be read as: **if `Y` is a parent of `X` or `Y` is a child of `X` or `Y` is a sibling of `X` then `Y` is an immediate family member of `X`**.

In the query panel enter `immediate_family(dave, X)` and select **Run!**. The query results should be `X = alice`, `X = bob`, `X = ivan`, `X = heidi`, `X = eve`, and `X = eve`.

> **Note:** The reason `X = eve` is returned twice is that there are two ways to prove that Eve is a sibling of Dave: via Alice, and via Bob. This kind of duplication is not typically a cause of concern in Prolog, but it [can be avoided](https://en.wikipedia.org/wiki/Cut_(logic_programming)) if deemed necessary.

Replace the rule with the following:

```prolog
immediate_family(X, Y) :- parent(X, Y).
immediate_family(X, Y) :- child(X, Y).
immediate_family(X, Y) :- sibling(X, Y).
```

In the query panel enter `immediate_family(dave, X)` and select **Run!**. The query results should again be `X = alice`, `X = bob`, `X = ivan`, `X = heidi`, `X = eve`, and `X = eve`.

This example demonstrates that disjunction can be implemented both using a single rule with disjunction in the body, or by multiple rules with the same head.

> **Note:** If in doubt, you should implement disjunction using multiple rules with the same head.

### Step 14 - Recursion

Add the following rule to the bottom of your Prolog program:

```prolog
ancestor(X, Z) :- parent(X, Z).
ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).
```

In the query panel enter `ancestor(peggy, X)` and select **Run!**. The query results should be `X = grace`, `X = ivan`, `X = carol`, `X = dave`, `X = alice`, and `X = bob`.

The definition of the `ancestor/2` implements disjunction using multiple rules with the same head. The first rule is the **boundary** case and the second rule is the **recursive** case. This kind of recursive definition forces the Prolog interpreter to explore the space of solutions with the boundary case providing a terminating condition that avoids an infinite loop.

> **Note:** Much of the power of Prolog comes from recursion, but it can be tricky to use correctly. When using recursion it essential that you always account for the boundary case.

## Summary

In this tutorial we have has a brief introduction to logic programming using SWISH, including how to write facts and rules, how to submit queries and interpret the results, and how to make use of core language features such as conjunction, disjunction, and negation.

In the [next tutorial](iis-tutorials-3.html) we will see how AgentSpeak and Jason extend logic programming to allow us to implement belief-desire-intention (BDI) agents.

### Complete listing

```prolog
% Facts

female(alice).
female(carol).
female(eve).
female(grace).
female(heidi).
female(judy).
female(peggy).
female(wendy).

male(bob).
male(dave).
male(frank).
male(ivan).
male(mike).
male(oscar).
male(rupert).
male(ted).
male(victor).

parent(dave, alice).
parent(dave, bob).
parent(eve, alice).
parent(eve, bob).
parent(ivan, carol).
parent(ivan, dave).
parent(heidi, carol).
parent(heidi, dave).
parent(mike, eve).
parent(mike, frank).
parent(judy, eve).
parent(judy, frank).
parent(peggy, grace).
parent(peggy, ivan).
parent(rupert, grace).
parent(rupert, ivan).
parent(ted, judy).
parent(ted, oscar).
parent(victor, judy).
parent(victor, oscar).
parent(wendy, judy).
parent(wendy, oscar).

age(alice, 91).
age(bob, 92).
age(carol, 61).
age(dave, 62).
age(eve, 63).
age(frank, 64).
age(grace, 31).
age(ivan, 32).
age(heidi, 33).
age(mike, 34).
age(judy, 35).
age(oscar, 36).
age(peggy, 1).
age(rupert, 2).
age(ted, 3).
age(victor, 4).
age(wendy, 5).

% Rules

child(X, Y) :- parent(Y, X).

mother(X, Y) :- parent(X, Y), female(Y).

father(X, Y) :- parent(X, Y), male(Y).

sibling(X, Y) :- parent(X, Z), parent(Y, Z), X \== Y.

adult(X) :- age(X, Y), Y >= 18.

grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

cousin(X, Y) :- grandparent(X, Z), grandparent(Y, Z), not(sibling(X, Y)), X \== Y.
immediate_family(X, Y) :- parent(X, Y).
immediate_family(X, Y) :- child(X, Y).
immediate_family(X, Y) :- sibling(X, Y).

ancestor(X, Z) :- parent(X, Z).
ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).
```
