![banner](https://raw.githubusercontent.com/MatuMaKa/images/refs/heads/main/Eliz%20Assets/3000x720.png)

# Eliz
A custom programming language combining Java &amp; Python

> [!TIP]
> Videos regarding this will be posted on https://www.youtube.com/@citzeh_lover22

## To-Do List

**Language features:**
- [ ] Function declarations with fn, parameters, and return values
- [ ] Class declarations and methods
- [ ] Object creation with new ClassName()
- [ ] Constructors using init()
- [ ] Instance fields and the this keyword
- [ ] Property access and method calls, such as greeter.greet()
- [ ] For loops
- [ ] else if branches
- [ ] Correct short-circuit behavior for and/or
- [ ] Consistent type checking for assignments and function arguments
- [ ] Return-value handling and errors for invalid function calls

**Project and module system:**
- [ ] Read main from eliz.json and launch the configured entry point
- [ ] Resolve module and import declarations across multiple .eliz files
- [ ] Ensure imported classes and functions are accessible
- [ ] Validate missing files, invalid modules, and circular imports
- [ ] Support both eliz run main.eliz and eliz run examples/Greeting

**CLI and developer experience:**
- [ ] Implement eliz init to create a project template
- [ ] Implement eliz check to report syntax and other detectable errors without running the program
- [ ] Implement a proper eliz help command
- [ ] Implement eliz update, or clearly report that self-updating is unsupported
- [ ] Improve syntax and runtime error messages with source locations
- [ ] Remove temporary test/demo code from production modules

**Testing and quality:**
- [ ] Create a comprehensive parser tests
- [ ] Create interpreter tests for every supported expression and statement
- [ ] Add integration tests that run complete .eliz files
- [ ] Add tests for imports, constructors, type errors, and invalid syntax
- [ ] Verify all tests pass together with python -m unittest discover -s tests -b
- [ ] Verify all Greeting example runs end-to-end

**Documentation and release:**
- [ ] Document the language syntax and operator precedence
- [ ] Document variables, types, functions, classes, and modules
- [ ] Document eliz.json and CLI commands
- [ ] Finish README.md and CHANGELOG.md
- [ ] Check pyproject.toml version and package metadata are consistent
- [ ] Prepare a GitHub release with working exampels and tests

**Other long-term plans:**
- Create a compiler, most likely .jar files, but maybe .exe as well or a native compiler. Probably needs to have a rewrite in a different language then...
- Evolution: Interpreter, Language specifications, Compiler prototype, Compile Eliz