# Programming Languages: Type Modeling

This assignment asks you to

- implement a simplified model of Java’s static type checking in Python, and
- implement a simplified model of Python’s object attribute lookup in Java.

Please note the important difference between the two parts of this assignment. In the first part, you are simulating how Java checks types and resolves method calls in expressions **at compile time**, i.e. for _all possible values_ that might actually show up in that expression whenever the code actually does run. In the second part, you are simulating how the Python interpreter handles _individual objects_ **at runtime**.

In both cases, I have given you a starting structure and tests that show you what you need to implement. You **should not modify any of the existing tests** in this assignment. (Do let me know if you find a mistake, however!)

Learning goals for this assignment:

- **Deepen your understanding of the differences between dynamically and statically typed languages.** Implementing something in code is a great way to think through it in detail!
- **Practice switching between languages often.** In this class, we look at many languages side by side. As we do, note the differences not just in the features, but in their aesthetics, their taste and texture, the kinds of programming and thinking habits they favor. Getting used to switching languages is also good practual for software development out in the wild.
- **Gain insight into what types are.** The two halves of this assignment are very different in the kind of algorithms they ask you to implement. Yet in both halves, you are creating a notion of “type.”


## The assignment

- Part 1: [Simulating Python’s object attribute lookup in Java](docs/1-python-in-java.md)
- Part 2: [Simulating Java’s static type checker in Python](docs/2-java-in-python.md)

⚠️ WARNING ⚠️ This is a big assignment, and part 2 is much larger than part 1. **Start early!**
