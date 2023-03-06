# Appendix A - Virtual environments

This appendix provides a brief introduction to implementing virtual environments in Jason, including environment actions.

<!-- TOC -->

## Getting started

Create a new Jason project in Eclipse called `appendix_a`.

### Step 1 - Environment class

Every Jason project includes a **virtual environment** that is shared by all agents in the project. The default environment in Jason is empty and includes no **environment actions** so it plays no role in an execution of the project. To interact with the virtual environment from your agent files (e.g. using environment actions) you must extend the particular Java class in Jason that implements the default virtual environment. Extending this class gives you a custom virtual environment where you can implement shared environmental observations and environment actions.

With the `src/java` directory in the Jason project highlighted in Eclipse select **File > New > Class**.

Enter `MyEnvironment` in the **Name** field.

![Figure](figures/new-class.png)

Select **Finish**.

A new Java file should be automatically created at `src/java/appendix_a/MyEnvironment.java`. Edit the file as follows:

```java
package appendix_a;

import jason.environment.Environment;

public class MyEnvironment extends Environment {

}
```

This Java class is where we will later implement shared observations and environment actions.

### Step 2 - Source percept annotations

We have seen in [Tutorial 4](tutorial-4.html) that Jason automatically annotates beliefs and goals with `source(self)` if they originate from the agent itself, or with `source(agent)`if they originate from another agent (called `agent`) following its execution of a Jason communication action. The third and final annotation applied automatically by Jason is `source(percept)`, which is applied to all beliefs that originate from the environment. Such beliefs may be referred to simply as **percepts**.

Create a new agent file called `environment_agent.asl`:

```jason
/* Initial beliefs and rules */

/* Initial goals */

/* Plans */

+weather(Attribute, Value)[source(self)] : true <- .print("I believe the ", Attribute, " is ", Value).

+weather(Attribute, Value)[source(percept)] : true <- .print("I observe the ", Attribute, " is ", Value).
```

Notice the important role of `source(X)` annotations when implementing agent files that integrate with a custom virtual environment. In this example both plans relate to belief addition events of the form `+weather(Attribute, Value)` but the first plan is only relevant when the event originates from the agent itself (`source(self)`) while the second plan is only relevant when the event originates from the environment (`source(percept)`). This demonstrates that Jason allows us to to implement agent files that distinguish between **beliefs** and **observations**.

### Step 3 - Jason configuration file

With a custom environment class implemented, the final step is to tell Jason to instantiate the virtual environment from this Java class by adding an `environment` option to the Jason configuration file that points to the new class.

Edit the Jason configuration file as follows:

```jason
MAS appendix {

  infrastructure: Centralised
  
  environment: appendix_a.MyEnvironment

  agents:
    alice environment_agent [beliefs="weather(temperature, cold)"];
    bob environment_agent;

  aslSourcePath:
    "src/asl";
}
```

The line `environment: appendix.MyEnvironment` tells Jason to instantiate the virtual environment from the new Java class `MyEnvironment` included in the `appendix_a` package of the Jason project.

Run the Jason project.

```text
[alice] I believe the temperature is cold
```

The new custom environment is working but is currently no different from the default virtual environment. For a meaningful virtual environments we need to implement shared initial percepts and/or environment actions.

## Initial percepts

Initial percepts are implemented in Jason by overriding the `Environment.init(...)` method included in the default virtual environment. Jason provides lots of functionality that can be used within this new method but most commonly you will add percepts using the `Environment.addPercept(...)` method. In practice this is much like defining initial base beliefs in the agent file, except it is achieved using Java code.

### Step 4 - Agent percepts

Initial percepts can be defined individually for each agent using `Environment.addPercept(agentName, literal)` where `agentName` is a string representing the name of an agent in the Jason project and `literal` is a Jason `Literal` object representing the percept to be added.

> **Note:** A Jason `Literal` object can be conveniently parsed from a string using `ASSyntax.parseLiteral(...)`. This method may throw a `ParseException` which you will need to catch yourself.

Edit `MyEnvironment.java` as follows:

```java
package appendix_a;

import jason.asSyntax.ASSyntax;
import jason.asSyntax.parser.ParseException;
import jason.environment.Environment;

public class MyEnvironment extends Environment {
  
    @Override
    public void init(String[] args) {
        try {
            this.addPercept("bob", ASSyntax.parseLiteral("weather(temperature, cold)"));
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }

}
```

Run the Jason project.

```text
[alice] I believe the temperature is cold
[bob] I observe the temperature is cold
```

Referring back to the original agent file we can see that `bob` has selected the plan with triggering event `+weather(Attribute, Value)[source(percept)]` to respond to this initial percept. The percept was thus added to the belief base of `bob` and annotated with `source(percept)` but otherwise handled as a standard belief addition event.

### Step 5 - Shared percepts

Shared initial percepts can also be defined for all agents using `Environment.addPercept(literal)` where `literal` is as before and there is no `agentName` parameter.

Add the following line to `MyEnvironment.java` below the existing `Environment.addPercept(...)` line:

```java
this.addPercept(ASSyntax.parseLiteral("weather(cloud_cover, sunny)"));
```

Run the Jason project.

```text
[alice] I believe the temperature is cold
[bob] I observe the temperature is cold
[alice] I observe the cloud_cover is sunny
[bob] I observe the cloud_cover is sunny
```

This method simply adds the percept to the belief base of every agent in the Jason project.

## Environment actions

Environment actions are implemented in Jason by overriding `Environment.executeAction(agentName, environmentAction)` within the custom environment class. Environment actions can then be executed within plan bodies much like [standard internal actions](https://jason.sourceforge.net/api/jason/stdlib/package-summary.html), with the only syntactic difference being that they do not start with `.` (full stop).

### Step 6 - Execution

Edit `environment_agent.asl` as follows:

```jason
/* Initial beliefs and rules */

/* Initial goals */

!go_to(class).

/* Plans */

+weather(Attribute, Value)[source(self)] : true <- .print("I believe the ", Attribute, " is ", Value).

+weather(Attribute, Value)[source(percept)] : true <- .print("I observe the ", Attribute, " is ", Value).

+!go_to(Destination) :
  weather(cloud_cover, sunny) & not weather(temperature, cold) <-
    ?location(Agent, Location);
    .wait(1000);
    walk(Location, Destination).

+!go_to(Destination) :
  .my_name(Agent) <-
    ?location(Agent, Location);
    .wait(1000);
    drive(Location, Destination).

+location(Agent, Location) : .my_name(Agent) <- .print("I am at ", Location).
```

In this example `walk(Location, Destination)` and `drive(Location, Destination)` are environment actions whereas `.wait(1000)` is a standard internal action. In each case variables `Location` and `Destination` must be instantiated **before** the action is executed.

Suppose `alice` executes environment action `walk(home, class)`. Jason will automatically trigger `Environment.executeAction(agentName, environmentAction)` such that `agentName = "alice"` and `environmentAction` is a Jason `Structure` object representing `walk(home, class)`.

Since the same method is called for all environment actions, it is necessary to inspect the `Structure` object within this method in order to determine what environment action has actually be executed. This can be achieved using the `Structure.getFunctor()` and `Structure.getTerms()` methods.

Edit `MyEnvironment.java` as follows:

```java
package appendix_a;

import jason.asSyntax.ASSyntax;
import jason.asSyntax.Structure;
import jason.asSyntax.parser.ParseException;
import jason.environment.Environment;

public class MyEnvironment extends Environment {
    
    @Override
    public void init(String[] args) {
        try {
            this.addPercept("bob", ASSyntax.parseLiteral("weather(temperature, cold)"));
            this.addPercept(ASSyntax.parseLiteral("weather(cloud_cover, sunny)"));

            this.addPercept(ASSyntax.parseLiteral("location(alice, home)"));
            this.addPercept(ASSyntax.parseLiteral("location(bob, work)"));
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }
    
    @Override
    public boolean executeAction(String agentName, Structure environmentAction) {
        System.out.println("> " + agentName + " is executing functor " + environmentAction.getFunctor() + " applied to terms " + environmentAction.getTerms());
        return true;
    }

}
```

If `Environment.executeAction(agentName, environmentAction)` is called such that `environmentAction` is a Jason `Structure` object representing `walk(home, class)`, then `environmentAction.getFunctor()` will return the string `walk` and `environmentAction.getTerms()` will return a list of `Term` objects containing `home` and `class`.

Notice that the method `Environment.executeAction(...)` must return a Boolean value where `true` indicates that the environment action succeeded and `false` indicates that it failed. In this example the action always succeeds.

Edit the Jason configuration file as follows:

```jason
MAS appendix_a {

    infrastructure: Centralised
    
    environment: appendix_a.MyEnvironment

    agents:
        alice environment_agent;
        bob environment_agent;

    aslSourcePath:
        "src/asl";
}
```

Run the Jason project.

```text
[alice] I am at home
[bob] I am at work
[bob] I observe the temperature is cold
[bob] I observe the cloud_cover is sunny
[alice] I observe the cloud_cover is sunny
> bob is executing functor drive applied to terms [work, class]
> alice is executing functor walk applied to terms [home, class]
```

Here we see that `alice` executed environment action `walk(home, class)` because she observed she was at `home` and that it was `sunny`, but did not believe it was `cold`. Conversely, `bob` executed environment action `drive(work, class)` because he observed he was at `home` and that it was `cold`.

### Step 7 - Effects

The significance of environment actions is that they affect changes to the environment, which is shared by all agents. This means that the execution of an environment action by one agent may affect other agents, not just itself.

In Jason the effects of actions are implemented, for the most part, by adding and removing percepts from within the `Environment.executeAction(...)` method. Percepts can be added as before using `Environment.addPercept(...)`, and removed using its corresponding method `Environment.removePercept(...)`. Most of the implementation effort is to determine **what** percepts should be added or removed, and **when**.

Edit `MyEnvironment.java` as follows:

```java
package appendix_a;

import jason.asSyntax.ASSyntax;
import jason.asSyntax.Structure;
import jason.asSyntax.parser.ParseException;
import jason.environment.Environment;

public class MyEnvironment extends Environment {

    @Override
    public void init(String[] args) {
        try {
            this.addPercept("bob", ASSyntax.parseLiteral("weather(temperature, cold)"));
            this.addPercept(ASSyntax.parseLiteral("weather(cloud_cover, sunny)"));
            
            this.addPercept(ASSyntax.parseLiteral("location(alice, home)"));
            this.addPercept(ASSyntax.parseLiteral("location(bob, work)"));
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }
    
    @Override
    public boolean executeAction(String agentName, Structure environmentAction) {
        try {
            String functor = environmentAction.getFunctor();
            if ( ( functor.equals("walk") || functor.equals("drive") ) && environmentAction.getArity() == 2 ) {
                System.out.println("> " + agentName + " is executing environment action " + environmentAction);
                this.removePercept(ASSyntax.parseLiteral("location(" + agentName + ", " + environmentAction.getTerm(0) + ")"));
                this.addPercept(ASSyntax.parseLiteral("location(" + agentName + ", " + environmentAction.getTerm(1) + ")"));
                return true;
            } else {
                System.err.println("> " + agentName + " is attempting to execute unknown environment action " + environmentAction);
                return false;
            }
        } catch (ParseException e) {
            e.printStackTrace();
            return false;
        }
    }

}
```

This example implements support for two environment actions `walk/2` and `drive/2`. In both cases the action effect is the same: if `walk(X, Y)` or `drive(X, Y)` is executed then `location(agent, X)` will be deleted as a shared percept and `location(agent, Y)` will be added, with `agent` the name of the agent who executed the action. If the method is called with any action other than `walk/2` or `drive/2` then the method will return `false` indicating that the action has failed (because no such action is defined).

Run the Jason project.

```text
[alice] I am at home
[bob] I am at work
[alice] I observe the cloud_cover is sunny
[bob] I observe the temperature is cold
[bob] I observe the cloud_cover is sunny
> bob is executing environment action drive(work,class)
> alice is executing environment action walk(home,class)
[bob] I am at class
[alice] I am at class
```

Here we see that that the effects of `walk/2` and `drive/2` have been applied correctly. For example, `alice` was initially at `home`, she executed `walk(home, class)`, which caused her to arrive at `class`.

### Step 8 - Consistency

According to the previous example if `alice` were to execute `walk(home, class)` while she was at `work` rather than at `home`, then `location(alice, class)` would still be added as a shared percept.

> **Note:** An attempt would also be made to delete `location(alice, work)` as a shared percept, but this attempt would silently fail because that percept did not exist.

It is your responsibility as Jason programmer to maintain consistency of your environment actions.

Edit the first `+!go_to` plan in `environment_agent.asl` as follows:

```jason
+!go_to(Destination) :
  weather(cloud_cover, sunny) & not weather(temperature, cold) <-
    .wait(1000);
    walk(work, Destination).
```

According to this plan if it is `sunny` and not `cold` then the agent will attempt to `walk` from `work` to its destination, regardless whether it it currently at `work` or not.

Edit `MyEnvironment.java` as follows:

```java
package appendix_a;

import jason.asSyntax.ASSyntax;
import jason.asSyntax.Literal;
import jason.asSyntax.Structure;
import jason.asSyntax.parser.ParseException;
import jason.environment.Environment;

public class MyEnvironment extends Environment {

    @Override
    public void init(String[] args) {
        try {
            this.addPercept("bob", ASSyntax.parseLiteral("weather(temperature, cold)"));
            this.addPercept(ASSyntax.parseLiteral("weather(cloud_cover, sunny)"));
            
            this.addPercept(ASSyntax.parseLiteral("location(alice, home)"));
            this.addPercept(ASSyntax.parseLiteral("location(bob, work)"));
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }
    
    @Override
    public boolean executeAction(String agentName, Structure environmentAction) {
        System.out.println(this.consultPercepts(agentName));
        try {
            String functor = environmentAction.getFunctor();
            if ( ( functor.equals("walk") || functor.equals("drive") ) && environmentAction.getArity() == 2 ) {
                System.out.println("> " + agentName + " is executing environment action " + environmentAction);
                System.out.println(this.consultPercepts(agentName));
                Literal locationBefore = ASSyntax.parseLiteral("location(" + agentName + ", " + environmentAction.getTerm(0) + ")");
                if (!this.consultPercepts(agentName).contains(locationBefore)) {
                    return false;
                }
                this.removePercept(locationBefore);
                this.addPercept(ASSyntax.parseLiteral("location(" + agentName + ", " + environmentAction.getTerm(1) + ")"));
                return true;
            } else {
                System.err.println("> " + agentName + " is attempting to execute unknown environment action " + environmentAction);
                return false;
            }
        } catch (ParseException e) {
            e.printStackTrace();
            return false;
        }
    }

}
```

The method `Environment.consultPercepts(...)` returns the current list of percepts for an agent, which can then be used to implement preconditions for environment actions. According to this example if an agent called `agent` attempts to execute `walk(X, Y)` or `drive(X, Y)` but `location(agent, X)` is not in the current list of percepts, then the method will return `false` meaning that the action has failed.

Run the Jason project.

```text
[bob] I am at work
[alice] I am at home
[bob] I observe the temperature is cold
[alice] I observe the cloud_cover is sunny
[bob] I observe the cloud_cover is sunny
> bob is executing environment action drive(work,class)
> alice is executing environment action walk(work,class)
[bob] I am at class
[alice] No failure event was generated for +!go_to(class)[code(walk(work,class)),code_line(16),code_src("file:src/asl/environment_agent.asl"),error(action_failed),error_msg(""),source(self)]
intention 1: 
    +!go_to(class)[source(self)] <- ... walk(work,Destination) / {Destination=class}
```

Here we see that the plan failed because `alice` attempted to execute `walk(work, class)` when she was at `home`.

Undo the change to the first `+!go_to` plan in `environment_agent.asl`, i.e.:

```jason
+!go_to(Destination) :
  weather(cloud_cover, sunny) & not weather(temperature, cold) <-
    ?location(Agent, Location);
    .wait(1000);
    walk(Location, Destination).
```

Run the Jason project.

```text
[alice] I am at home
[bob] I am at work
[alice] I observe the cloud_cover is sunny
[bob] I observe the temperature is cold
[bob] I observe the cloud_cover is sunny
> bob is executing environment action drive(work,class)
> alice is executing environment action walk(home,class)
[bob] I am at class
[alice] I am at class
```

Here we see that the plans succeed as long as the executed environment actions satisfy the preconditions implemented in `Environment.executeAction(...)`.

### Step 9 - Environment state

In the previous examples all information needed to determine the effects on an environment action were embedded in the action itself (e.g. by the variables `Location` and `Destination`). However, `MyEnvironment` is just a standard Java class so you are free to use whatever internal data structures you wish.

Suppose each agent has an energy level and the two environment actions `walk/2` and `drive/2` have secondary effects of consuming energy. We assume that `walk/2` consumes three units of energy and `drive/2` consumes one unit. All agents start with five units of energy.

Edit `MyEnvironment.java` as follows:

```java
package appendix_a;

import java.util.HashMap;
import java.util.Map;

import jason.asSyntax.ASSyntax;
import jason.asSyntax.Literal;
import jason.asSyntax.Structure;
import jason.asSyntax.parser.ParseException;
import jason.environment.Environment;

public class MyEnvironment extends Environment {
    
    int DEFAULT_ENERGY = 5;
    
    Map<String, Integer> energy;

    @Override
    public void init(String[] args) {
        try {
            this.addPercept("bob", ASSyntax.parseLiteral("weather(temperature, cold)"));
            this.addPercept(ASSyntax.parseLiteral("weather(cloud_cover, sunny)"));
            
            this.addPercept(ASSyntax.parseLiteral("location(alice, home)"));
            this.addPercept(ASSyntax.parseLiteral("location(bob, work)"));
            
            this.addPercept(ASSyntax.parseLiteral("energy(" + DEFAULT_ENERGY + ")"));
            
            energy = new HashMap<String, Integer>();
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }
    
    @Override
    public boolean executeAction(String agentName, Structure environmentAction) {
        try {
            String functor = environmentAction.getFunctor();
            if ( ( functor.equals("walk") || functor.equals("drive") ) && environmentAction.getArity() == 2 ) {
                System.out.println("> " + agentName + " is executing environment action " + environmentAction);
                
                Literal locationBefore = ASSyntax.parseLiteral("location(" + agentName + ", " + environmentAction.getTerm(0) + ")");
                if (!this.consultPercepts(agentName).contains(locationBefore)) {
                    return false;
                }
                
                int energyBefore = energy.getOrDefault(agentName, DEFAULT_ENERGY);
                
                this.removePercept(locationBefore);
                this.removePercept(agentName, ASSyntax.parseLiteral("energy(" + energyBefore + ")"));
                
                int energyCost;
                if (functor.equals("walk")) {
                    energyCost = 3;
                } else {
                    energyCost = 1; 
                }
                
                int energyAfter = energyBefore - energyCost;
                energy.put(agentName, energyAfter);
                
                this.addPercept(ASSyntax.parseLiteral("location(" + agentName + ", " + environmentAction.getTerm(1) + ")"));
                this.addPercept(agentName, ASSyntax.parseLiteral("energy(" + energyAfter + ")"));
                
                return true;
            } else {
                System.err.println("> " + agentName + " is attempting to execute unknown environment action " + environmentAction);
                return false;
            }
        } catch (ParseException e) {
            e.printStackTrace();
            return false;
        }
    }

}
```

The internal data structure `energy` is just a mapping from agent names to energy levels that we use to track the energy level of each agent during execution of the Jason project. If an agent executes either environment action then `energy` is updated within the `Environment.executeAction(...)` method according to the new energy level.

When either environment action is executed by an agent called `agent` in this example, then a percept of the form `energy(X)` is added to the belief base of `agent`. This means that each agent can observe its own energy level but not the energy level of other agents. We could likewise choose to hide this information from the agent itself (i.e. by not adding the percept) and the environment would still continue to track energy levels as before.

Add the following plan to the bottom of `environment_agent.asl`:

```jason
+energy(Value) : true <- .print("my energy is ", Value).
```

Run the Jason project.

```text
[alice] my energy is 5
[bob] my energy is 5
[alice] I am at home
[bob] I am at work
[alice] I observe the cloud_cover is sunny
[bob] I observe the temperature is cold
[bob] I observe the cloud_cover is sunny
> alice is executing environment action walk(home,class)
> bob is executing environment action drive(work,class)
[alice] my energy is 2
[alice] I am at class
[bob] I am at class
[bob] my energy is 4
```

Here we see that the energy level for `alice` is 2 after she executes environment action `walk(home,class)`, while the energy level for `bob` is 4 after he executes environment action `drive(work,class)`.

## Conclusion

In this appendix we have seen how to implement virtual environments in Jason by extending the `Environment` Java class that implements the default virtual environment. In particular, the `Environment.init(...)` method is used to implement initial percepts and the `Environment.executeAction(...)` method is used to implement environment actions.
