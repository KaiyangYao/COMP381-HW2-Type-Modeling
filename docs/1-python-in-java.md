# Part 1: Python in Java

In the `python-attr-lookup/` directory, I have set up a Java project that provides a simplified model of Python types and objects. Your job is to implement object instantiation and attribute lookup in this model.

**To open the project in IntelliJ:**

- From the IntelliJ main start screen, choose **Open**.
    - Note: That’s “Open,” **not** “Import Project!”
- Select the `python-attr-lookup/` directory.
    - Note: That’s the directory, **not** the `.iml` file! You open the iml when importing a module, but the directory when importing a project.
        - Note: Yes, this is ridiculous. Talk to the IntelliJ folks.
- If you get a message about importing the Gradle project, you can click “Skip.” I already set up this project for IntelliJ.

**To open the project in VS Code:**

- Open the `python-attr-lookup/` directory.
- If it asks you to trust the project, choose "Yes, Trust."
- After some time building, VS Code should recognize the Java project and show you the option to run tests in the leftmost navigation bar. If you don’t see tests showing up, or if you get errors opening the projects…_sigh._ Contact me for help!


## Part 1.0: Understand your starting point

Spend some time reading through the structure of the classes under `python-attr-lookup/src/`, especially `PythonObject` and `PythonType`. Their javadoc describes the behavior you are aiming for. The `"not implemented yet"` exceptions indicate the parts you need to fill in.

Now look over the tests in `PythonObjectTest.java`. What do they expect to happen, and why?


## Part 1.1: Implement object instantiation

Implement `PythonType.instantiate()`. Read the javadoc for that method to see what it is supposed to do. The solution is very simple to implement, but think carefully about what it is and why.

Implementing this will make the first test pass.


## Part 1.2: Implement method resolution order

Python first looks for attributes on an object itself, then on its type and the type’s base types (i.e. superclasses). Python uses a “method resolution order” (MRO) to determine where to look for attributes and in what order. (It is called “method” resolution order even though it also applies to attributes that are not methods.)

Real-life Python supports a class having more than one base class (a.k.a “multiple inheritance”), and uses a [fancy algorithm](https://en.wikipedia.org/wiki/C3_linearization) to work out the MRO. For this assignment, however, you will only be supporting single inheritance.

Implement `PythonType.buildMRO()` and `PythonObject.buildMRO()`. This will make the test under the `MRO tests` heading all pass.


## Part 1.3: Implement get() and set()

Make the rest of the tests pass by implementing `PythonObject.get()` and `PythonObject.set()`. When implemented correctly, these will make all the remaining tests pass — but they should not require a large amount of code.

I recommend making the tests pass one at a time, _in the order they appear in the test class_. They are set up to guide you through a good implementation strategy.


## Part 1.4: Test null overrides

The tests I’ve provided for you cover the problem domain fairly well, but there is one crucial test missing. Calling `set()` should _always_ override any value from either `type` or `base` — _even when setting the attribute to null_. Depending on how you implemented it, this might already work…or setting an attribute to `null` might incorrectly re-expose the inherited value.

You last task: **add an `overrideInheritedAttrsWithNull` test** to `PythonObjectTest` to test this scenario. (You will see a TODO for it. Don’t forget to remove the TODO when you’ve implemented the test!)

Think: What are you testing? Look at and understand the other tests, and use them as a starting point — but **do not just copy and hope**. Make sure that you understand _what_ condition you are testing for, and _why_ your test verifies that it is correctly implemented.

Make sure your new test passes, fixing your `PythonObject` implementation if necessary.


## Wrap it up

If you’ve been running individual test cases, go back and **double check that all the tests pass**.

Don’t forget to commit and push as you work!
