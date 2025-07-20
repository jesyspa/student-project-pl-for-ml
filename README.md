# ML for PL (Summer Practice)

Student project looking into how PL techniques can be used
to improve (ML-based) code generation.

## How to Run the Project
1. Install Python
Make sure you have Python 3.11 or higher installed.

2. Install Dependencies
The project does not need any extra libraries, except pytest for running tests.

```bash
pip install pytest
```

## Running Tests
### From Terminal

Go to the project root folder and run:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_scanner.py
```

## From PyCharm

1. Open the project in PyCharm

2. Right-click the tests/ folder

3. Click “Run 'pytest in tests'”

4. Or click the green ▶ next to a test function

## Interpreter
### Arithmetic operation rules
```
1. scalar + scalar -> standard arithmetic (e.g., 2 + 3 = 5)
2. list + scalar  -> elementwise (e.g., [1, 2] + 3 = [4, 5])
3. scalar + list  -> elementwise (e.g., 3 + [1, 2] = [4, 5])
4. list + list    -> not supported (raises error)

~ same rules apply for -, *, /
~ if operands are not numbers or lists -> convert to a string and merge (in case of '+')
```


### Principles for List Handling

#### Arithmetic and Comparison Work Elementwise
If one or both arguments are lists, operations are applied element-by-element:

```
(+ (list 1 2 3) 10)        => (11 12 13)
(+ 10 (list 1 2 3))        => (11 12 13)
(+ (list 1 2) (list 3 4))  => (4 6)

(< (list 1 2 3) 5)         => (true true true)
(= (list 1 2) (list 1 3))  => (true false)
```

#### Core List Functions

```
(list a b c)         creates a list
(head lst)           returns the first element
(tail lst)           returns the list without the first element
(append lst1 lst2)   merges two lists
(reverse lst)        reverses the list
(push x lst)         pushes an element into the list [2,3] => [x,2,3]
(get lst idx)        gets an element at a specific index
(length lst)         returns the length of a list
(empty? lst)         returns true if list is empty
```