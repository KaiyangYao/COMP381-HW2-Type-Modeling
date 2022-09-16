# Part 2: Java in Python

## Setup

You’ll need Python 3 installed. Try `python3` at the command line. (Make sure to include the `3`; old Pythons won’t work.) If that command gives an error, use an internet search or your friendly neighborhood professor for help installing it.

You can also use PyCharm for this if you have it installed, but it is not required. If you are willing to use the command line, then you can use any general-purpose programmer’s text editor with it (VS Code, Sublime Text, Atom, Brackets, Vim, etc.).

⚠️ Note that there are two separate projects in this homework repo, and **the root of the Python project is the `java-type-checker` subdirectory**. If you open the whole `type-modeling` directory in PyCharm, or only `cd` into `type-modeling` at the command line, nothing will work. Instead, you need to work in the `java-type-checker/` subdirectory. ⚠️


## Your job

I have given you some Python code that provides a simplified model of a few basic parts of Java’s static type system and its expression AST. Note that there is no parser here; the tests you will be working with build up the Java AST manually, creating the tree node by node.

By “simplified,” I mean that this model captures only a few language features: only a few basic kinds of expression (no arithmetic here, for example), and only the basics of the type system (no generics such as `List<String>`, no arrays, etc.). There is just enough structure here for you to get the feel of how a static type checker works.

You are going to do four things:

1. Implement the **subtype** relationship between types: Is a `Rectangle` a `GraphicsObject`? Is a `Rectangle` a `String`? How does Java decide this?
2. Determine the **static type** of expressions: If we write the expression `rect.getPosition().getX()`, what does Java know at compile time about what type that expression will evaluate to? How does Java figure this out without actually running the code?
3. Perform **static type checking** of expressions: Given the code `widget.frongulate(doodad)`, how does Java check whether the `frongulate` method exists? If it does, how does Java determine whether `doodad` is a valid argument?
4. Implement **type logic for `null`**: The value `null` is a special case in Java and most other object-oriented languages; it obeys rules no other type obeys. How so? That’s what you’ll find out!


## General hints

These are the most common student mistakes in this homework:

- **Overcomplicating things:** Some of the things you need to implement are very, very small. Some methods will have a single-line implementation. None of these things involve massive, sophisticated algorithms.
- **Using giant conditionals:** In several cases, you will have to implement the same method for several different types, using different logic for each. Do this using **polymorphism**, i.e. override the method in each different type. If you find yourself writing a big conditional that says something like “if it’s a JavaVariable…else if it’s a JavaLiteral…else if it’s a JavaAssignment…,” then you are doing it wrong! Instead, override that method in `JavaVariable`, then override it in `JavaLiteral`, etc.
- **Trying to handle the whole expression tree at once:** You will implement methods that live on nodes in a big tree of `JavaExpression` objects. There is sometimes a temptation to try to look down into the next level of the tree: “I am working on JavaAssignment, and what if the thing on the right-hand side is a JavaLiteral? But what if it is a JavaMethodCall? I have to handle both! Oh no!!” Don’t get wrapped around the axle this way; this approach will not serve you well here. When you are looking at children in the tree, do not assume anything about what _kind_ of child it is. Instead, rely only the methods that _every_ node in the tree is guaranteed to have, and let polymorphism choose the correct implementation for you.

If these hints are a little confusing now, refer back to them when you are in the middle of Part 2.2 or so.

## Hints about Python

If you took Comp 123 a long time ago, or didn’t take Comp 123 and started programming in a different language, you might be a little fuzzy on Python. And even if you remember Comp 123, it’s quite likely you didn’t learn much about OOP in Python. That is OK! One of the **primary purposes** of this class is for you to get practice and gain confidence **working outside of your comfort zone with languages and languge features you do not already know.**

In intro CS classes, we try to build things up for you step by step. We carefully introduce each little Lego piece of the language to you, and write activities and homeworks that only use the building blocks we’ve introduced so far. Those days are over. You are a capable programmer now! You already have what you need for self-directed language learning! Programmers in the wild frequently have to use unfamiliar features, unfamiliar languages, building blocks they’ve never even heard of until they encounter them — **and that is OK.** Embrace the unfamiliar! That is the life of a programmer.

That said, here are a few little hints about OOP in Python to give you a little boost:

- **In Python, the standard name for the variable that means “the object who is responding to this method call” is `self`, not `this`.** Both names have a long tradition in OOP, and both names are common in various OOP languages. (The first OOP languages were Simula and Smalltalk. The name `this` originated in Simula, and Java, C++, C#, D, PHP use it. The name `self` originated in Smalltalk, and Python, Ruby, Rust, Swift, Perl, and Objective-C all use it.)
- **Python requires explicit `self` in method calls.** In Java, you do not have to say `this.dance()`; you can just say `dance()`. In Python, you _have_ to say `self.dance()`; the `self.` is required. Many languages have a similar rule.
- **Python also requires explicit `self` in method _declarations_.** For example, if you a making a `TalkingHorse` class with a `say` method, you would declare it like this:

    ```python
    class TalkingHorse:
      def say(self, text):      # 2 declared parameters
        ...
    ```

    …and call it like this:

    ```python
    mr_ed.say("Hello, Wilbur")  # 1 argument provided
    ```

    Note that we _declared_ the method with 2 parameters, but we only _called_ it with only 1 argument. That is because the receiver (the value to the left of the dot) becomes the first parameter:

    - `mr_ed` → `self`
    - `"Hello, Wilbur"` → `text`

    This bizarre choice is pretty much unique to Python. In almost every other object-oriented language, `self` / `this` appears automatically on its own.

    <details>
      <summary>Why does Python do this?!</summary>

    Sometimes people make a case based on clarity: “explicit is better than implicit,” they say, “so self should be explicit!”  I (Paul) basically don’t buy that at all — choosing to make some things implicit is the _heart_ of programming language design — but it’s an interesting argument to consider.

    The creator of Python has an [elaborate justification](http://neopythonic.blogspot.com/2008/10/why-explicit-self-has-to-stay.html) based on how this decision intersects with other language features of Python. There are some more convincing ideas in there, though it’s worth noting that other languages managed to solve these problems. Then again, given the [hideous](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this) [mess](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_objects/Function/bind) that resulted from JavaScript’s attempts to solve those problems while making `this` implicit, I’m hard pressed to say that Python made the worst choice possible!
    </details>

I leave it to you to research how to declare a list in Python, how to loop over a list, how to instantiate an object, etc. **Studying the existing code in the project** is a good place to start.

---

## Part 2.0: Study the starting code

Run these tests; they should already pass:

```bash
cd java-type-checker  # A subdirectory of the assignment

python3 -m tests.test_01_class_structure
```

(If you get `ModuleNotFoundError: No module named 'tests'`, then you are in the wrong directory.)

- Study those tests, and understand what principle each one is testing.
- Study the classes in `types.py` and `expressions.py`. I strongly suggest **drawing a diagram** of the classes, their relationships, and what methods each one has. Understand that class structure, because you are about to add behavior to it. How do the roles of the things in those two files differ? What parts of Java do they represent?
- Study the code in `tests/fixtures.py`, which uses the expression and type classes above to create test data.

**Don’t proceed with the assignment** until you have a decent understanding of the items above. Send questions!


## Part 2.1: Implement subtype logic

What does “subtype” mean? Type B is a **subtype** of type A if a value of type B works in a contexts that expect a value of type A. In other words, it defines the “is a” relationship.

For example, this works:

```
GraphicsObject rect = new Rectangle(0, 0, 100, 100);
```

…because `Rectangle` is a subtype of `GraphicsObject`. However, this does not work:

```
GraphicsObject string = "Hello";  // Compile error
```

…because `String` is not a subtype of `GraphicsObject`.

Implement the `Type` class’s `is_subtype_of()` method to make these tests pass:

```bash
python3 -m tests.test_02_type_relationships
```

<details>
  <summary>Click for hint: I’m not sure where to start.</summary>
    
  You need to override the `is_subtype_of` method in both `JavaPrimitiveType` and `JavaObjectType`.
</details>
<details>
  <summary>Click for hint: What’s the Python syntax for overriding a method?</summary>
    
  For example:
  ```python
  class JavaPrimitiveType(JavaType):
      """Here is some documentation for the class.
      """

      def is_subtype_of(self, other):   # ← add this line to override the method
          return ????????
  ```
</details>


## Part 2.2: Implement expression types

What is the static type of an expression? It is the type that compiler uses to check whether an expression fits its context. For example, given this:

```
GraphicsObject rect = new Rectangle(0, 0, 100, 100);
```

…then the static type of `rect.getPosition()` is `Point`, because that expression always evaluates to a `Point`. But what is the static type of `rect`? It is `GraphicsObject`. Why? Even though the expression `rect` actually will evaluate to a `Rectangle` at runtime, we declared the variable as a `GraphicsObject`, so the compile will use _that_ type for type checking.

Implement `static_type()` for all the subclasses of `Expression`, to make these tests pass:

```bash
python3 -m tests.test_03_expression_static_types
```

These implementations will be quite small. Please take a moment to think about each one, what it means, and why the test is asking you to implement the behavior it describes.



<details>
  <summary>Click for hint: I’m a little overwhelmed by what to do for JavaMethodCall…</summary>
  
  It may be helpful to study a specific example:

  ```java
  "Macalester".length()
  ```

  What is the static type of this `JavaMethodCall`? The answer is `int`.

  Why? Here’s the logic:

  - The receiver of the method call is the expression `"Macalester"`.
  - That expression’s static type is `String`.
  - The `String` type has a method named `length`.
  - That method returns `int`.

  Each step of that is important, and something you need to implement in code. It only takes a tiny bit of code to take each step….
</details>


## Part 2.3: Implement the type checker

Implement `check_types()` for all the subclasses of `Expression` to make these tests pass:

```bash
python3 -m tests.test_04_basic_type_checking
```

```bash
python3 -m tests.test_05_assignment_type_checking
```

```bash
python3 -m tests.test_06_method_call_type_checking
```

```bash
python3 -m tests.test_07_nested_type_checking
```

This is the most labor-intensive part of this assignment. The tests will guide you through it; I recommend making the tests pass one at a time within each file, in numbered order.

Many of you may be rusty on Python; if you are, please seek help from me, or from fellow students on our Slack channel. (Be careful **not** to post code that would give away part of the solution for other students! Do however feel free to ask “What’s the Python syntax for….”)

<details>
  <summary>Click for hint: What value am I supposed to return from `check_types`?</summary>
    
  Nothing. You do not return a value.

  If there is a problem, `check_types` raises an exception. If there is no type error, the method simply returns nothing.
</details>
<details>
  <summary>Click for hint: Wait…what is `check_types` even supposed to to for `JavaLiteral` and `JavaVariable`?</summary>
    
  Remember the rules for the `check_types` method: If there is a problem, then `check_types` raises an exception. If there is no type error, the method simply returns nothing.

  Now, read the test names and documentation in `test_04_basic_type_checking.py`. When would those methods need to raise an exception? When would they need to return nothing?

</details>
<details>
  <summary>Click for hint: What is the syntax for returning nothing in Python?</summary>

  You can just say `return`. Also, if you want to make an empty block — the equivalent of `{}` in Java — then you can use the special keyword `pass`, which basically means “this space intentionally left blank.” Python needs a special syntax for that because of its indentation-based block structure. Without it, how do you tell the difference between “empty nested block is here” and “nothing is here?”
</details>
<details>
  <summary>Click for hint: How do I format these complex error messages the tests want me to return?</summary>
    
  Because you may especially be rusty on Python string formatting, and because formatting error messages is not the point of this assignment, here are two snippets you may find useful (and that give you a tiny hit about the shape of the solution):

  ```python
  raise SomeKindOfTypeError(
      "Wrong number of arguments for {0}: expected {1}, got {2}".format(
          call_name,
          len(expected_types),
          len(actual_types)))
  ```

  And then later, you’ll need this:


  ```python
  raise SomeKindOfTypeError(
      "{0} expects arguments of type {1}, but got {2}".format(
          call_name,
          _names(expected_types),
          _names(actual_types)))
  ```

  Note that this second snippet uses the `_names()` helper **already implemented for you** in `expressions.py`.
</details>
<details>
  <summary>Click for hint: I’m getting lost trying to loop over the arguments.</summary>
  
  Here are some looping patterns in Python that may help you:

  ```python
  # Iterate over a list
  for item in list_of_things:
    ...

  # Iterate from 0 to n
  for i in range(n):
    ...

  # Iterate over the indices of a list
  for index in range(len(list_of_things)):
    ...

  # Iterate over the items in a list, with their indices
  for (index, item) in enumerate(list_of_things):
    ...

  # Iterate over corresponding pairs of items from two different lists:
  for (item0, item1) in zip(list0, list1):
    ...
  ```
</details>
<details>
  <summary>Click for hint: I’m confused: all the previous tests passed, but now `nested_type_checking` fails.</summary>
    
  Calling `some_node.check_types()` should not only type check `some_node` itself, but also all of its children.

  <details>
  <summary>How do I make that happen?</summary>

  Inside `check_types()`, recursively call `check_types()` for all the child nodes. And what are the child nodes? It depends on what kind of node this is! For example, the children of a method call are (1) the receiver and (2) each of the arguments.
  </details>
  <details>
  <summary>I did that, but `method_call_children_get_type_checked_first` is still failing.</summary>

  Study that test. What is it checking for? What is it saying your code should do? How do you make that happen? The information you need is all there in the test; slow down and study it carefully.
  </details>
</details>


## Part 2.4: Support `null`

Java’s `null` is a quirky special case:

- it cannot be instantiated and
- it has no methods, yet
- it behaves like a subtype of every class and every interface.

Making it work properly requires a special class in our type checker, `JavaNullType`. Implement it. (You will find a placeholder for it in `types.py`.)

You’ll find this poses some tricky questions: what should you subclass to implement it? Can it inherit any of its logic from existing classes in that file? There is no single correct answer. However, although this takes a lot of thinking, the solution _does not take a lot of code._ Don’t go down a rabbit hole!

Get the null tests to pass:

```bash
python3 -m tests.test_08_null
```


## Bonus: Support `void` and constructor calls

If you want an additional challenge, enable the tests in `test_bonus_constructor_call` and `test_bonus_void` by deleting the `@unittest.skip(…)` lines, then make the tests pass.

A good challenge: try to do this without duplicating any more core than you can help betwen the `JavaMethodCall` and `JavaConstructorCall` classes.

This is a nice exercise in keeping code organized as it grows in a tricky object model. It is also a nice way to think about the structure of Java: how void is / isn’t like other types, and how constructor calls are and are not like method calls.


## Wrap it up

Double check that **all** the tests pass:

```bash
python3 -m unittest
```

(If you chose not to do the bonus problems, you will see some tests skipped. That is fine!)

Commit and push your work. Then take a pleasant walk as you muse on how much work it takes to implement an entire programming language.
