# Tutorial Series - Programming in Jason

[Jason](https://jason-lang.github.io/) is an **agent-oriented programming** platform that provides:

- An **interpreter** for [AgentSpeak](https://doi.org/10.1007/BFb0031845), which is an agent-oriented programming language that extends **logic programming** and sits within the belief-desire-intention (BDI) paradigm
- A **broader infrastructure** for implementing multi-agent systems, including **agent communication** and **virtual environments**

This is a tutorial series for [EMATM0042 - Intelligent Information Systems](https://www.bris.ac.uk/unit-programme-catalogue/UnitDetails.jsa?unitCode=EMATM0042) that provides a brief introduction to programming multi-agent systems in Jason.

All steps and screenshots are based on **macOS** but should work similarly for **Windows** and **Linux**.

<!-- TOC -->

## Getting started

This section describes how to get started with Jason development and should be completed prior to the lab sessions.

<!-- Where possible, students are strongly encouraged to use their own machines for Jason development. Students who are able bring a laptop to the lab sessions should follow Tutorial 1a and can safely ignore Tutorial 1b. Students who are unable to bring a laptop should follow Tutorial 1b to access Jason on a lab machine. -->

Students are requested to install Jason on their own laptops and to use them during the lab sessions. For students who are unable to do so, details will be provided separately on how to access Jason on the lab machines.

- [Tutorial 1 - Installing Jason](tutorial-1.html)

<!-- - Tutorial 1b - Jason on lab machines &#9940; &#128679; -->

## Lab sessions

### Tuesday 5 March 2024

A basic understanding of logic programming is essential to Jason programming. This section provides a brief introduction to logic programming using the SWISH web interface for SWI-Prolog.

<!-- - Tutorial 2 - Logic programming &#9940; &#128679; -->

- [Tutorial 2 - Logic programming](tutorial-2.html)

### Tuesday 12 March 2024

Agents are implemented in Jason using a variant of the AgentSpeak language, denoted by files with the `.asl` extension.
This section provides a brief introduction to implementing `.asl` files.

<!-- - Tutorial 3 - Agents &#9940; &#128679; -->

- [Tutorial 3 - Agents](tutorial-3.html)

### Tuesday 19 March 2024

Multi-agent systems are configured in Jason using a Jason configuration file, denoted by the `.mas2j` extension.
Jason also provides a family of actions, available when implementing `.asl` files, that allow agents to communicate with each other. This section provides a brief introduction to the `.mas2j` file and to Jason communication actions.

<!-- - Tutorial 4 - Multi-agent systems &#9940; &#128679; -->

- [Tutorial 4 - Multi-agent systems](tutorial-4.html)

## Advanced material

Experience with Java programming is desirable but not essential to Jason programming. This section provides details on advanced topics that require at least some Java programming.

The material covered in this section is **not required** to achieve full marks in the assignment. However, experienced programmers (especially those with Java experience) should find them straightforward and they will allow you to implement more interesting applications in Jason.

<!-- - Appendix A - Virtual environments &#9940; &#128679;
- Appendix B - Graphical user interfaces &#9940; &#128679;
- Appendix C - Custom internal actions &#9940; &#128679; -->

- [Appendix A - Virtual environments](appendix-a.html)
- [Appendix B - Graphical user interfaces](appendix-b.html)
- [Appendix C - Custom internal actions](appendix-c.html)

## Further resources

- [Jason textbook](https://jason.sourceforge.net/jBook/jBook/Home.html)
- [Solutions to exercises in Jason textbook](https://jason.sourceforge.net/jBook/jBook/Examples.html)
- [Demos of selected Jason functionality](https://github.com/jason-lang/jason/tree/main/demos) (also in [Jason download](https://sourceforge.net/projects/jason/files/jason/))
- [Examples of applications implemented in Jason](https://github.com/jason-lang/jason/tree/main/examples) (also in [Jason download](https://sourceforge.net/projects/jason/files/jason/))
