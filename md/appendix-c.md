# Appendix C - Custom internal actions

This appendix provides a (very) brief introduction to implementing custom internal actions in Jason.

<!-- TOC -->

## Getting started

Create a new Jason project in Eclipse called `appendix_c`.

## Example - Euclidean distance

Suppose we want to calculate the Euclidean distance between `P1 = point(X1, Y1)` and `P2 = point(X2, Y2)`. This functionality could be implemented in Jason with a custom internal action of the form `euclidean_distance(P1, P2, Q)` where its execution would serve to instantiate variable `Q` with a number representing the distance between `P1` and `P2`.

With the Jason project highlighted in Eclipse select **File > New > Internal Action**.

Enter `euclidean_distance` in the **Name** field and select **Finish**.

A new Java file should be automatically created at `src/java/appendix_c/euclidean_distance.java`. Edit the file as follows:

```java
package appendix_c;

import jason.asSemantics.DefaultInternalAction;
import jason.asSemantics.TransitionSystem;
import jason.asSemantics.Unifier;
import jason.asSyntax.LiteralImpl;
import jason.asSyntax.NumberTerm;
import jason.asSyntax.NumberTermImpl;
import jason.asSyntax.Term;

public class euclidean_distance extends DefaultInternalAction {

    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        LiteralImpl p1 = (LiteralImpl)args[0];
        LiteralImpl p2 = (LiteralImpl)args[1];
        
        NumberTerm x1 = (NumberTerm)p1.getTerm(0);
        NumberTerm y1 = (NumberTerm)p1.getTerm(1);
        
        NumberTerm x2 = (NumberTerm)p2.getTerm(0);
        NumberTerm y2 = (NumberTerm)p2.getTerm(1);
        
        double value = Math.sqrt( Math.pow(x2.solve() - x1.solve(), 2) + Math.pow(y2.solve() - y1.solve(), 2) ); 
        
        NumberTerm q = new NumberTermImpl(value);
        
        return un.unifies(q, args[2]);
    }
    
}
```

Custom internal actions are implemented by extending the base class `DefaultInternalAction` from Jason and overriding its `execute` method. The syntax for executing custom internal actions within an agent file is `package_name.class_name`. Our action can thus be executed using `appendix_c.euclidean_distance(P1, P2, Q)`.

> **Note:** Standard convention for naming of classes in Java is [camel case](https://en.wikipedia.org/wiki/Camel_case), but standard convention for naming of actions in Jason is [snake case](https://en.wikipedia.org/wiki/Snake_case). We follow the latter convention in this example.

An important feature of internal actions is that arguments need not be fully ground when the action is executed. In our case the code assumes that `P1` and `P2` are fully ground literals of the form `point(X, Y)`, while `Q` is a variable that is instantiated by the action itself.

> **Note:** Details on how to implement the `execute` method can be found in Section 7.1 of the [Jason textbook](https://jason.sourceforge.net/jBook/jBook/Home.html).

Edit `sample_agent.asl` as follows:

```jason
/* Initial beliefs and rules */

/* Initial goals */

!distance(point(1, 2), point(3, 4)).

/* Plans */

+!distance(P1, P2) :
  true <-
    appendix_c.euclidean_distance(P1, P2, Q);
    .print("Euclidean distance from ", P1, " to ", P2, " is ", Q).
```

Run the Jason project.

```text
[agent1] Euclidean distance from point(1,2) to point(3,4) is 2.8284271247461903
```

The new custom internal action appears to be working correctly.

## Conclusion

In this appendix we have seen very briefly how to implement custom internal actions in Jason using an example of calculating the Euclidean distance between two points.

This appendix is provided for the sake of completeness only, and you should **think carefully** about whether a custom internal action is really necessary for your Jason project; custom internal actions are **easy to abuse**, and may duplicate functionality that is **already supported** in Jason by default. For example, the Euclidean distance could in fact be easily implemented in an agent file using built-in arithmetic operations without the need to resort to custom internal actions.
