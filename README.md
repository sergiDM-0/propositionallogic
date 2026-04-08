# Propositional Logic Engine

This project provides a robust engine for working with propositional logic, offering functionalities for parsing, evaluating, and generating truth tables for logical expressions. It's designed with a clean, modular architecture and a user-friendly Command Line Interface (CLI).

## 🚀 Features

*   **Logical Expression Parsing:** Parse complex logical statements into an internal representation.
*   **Truth Table Generation:** Automatically generate truth tables for given propositional logic formulas.
*   **Logical Operator Support:** Supports standard logical operators such as AND (`&`), OR (`|`), NOT (`~`), Implication (`>`), Biconditional (`=`), XOR (`^`).
*   **CLI Interface:** An intuitive command-line interface to interact with the logic engine.
*   **Extensible Design:** Modular design allows for future expansion to other areas of logic (e.g., first-order logic).
*   **Error Handling:** Robust error checking and reporting for invalid expressions.

## 🛠️ Installation

### Prerequisites

*   Python 3.7+

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd propositionallogic
    ```

2.  **Set up a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.\venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    The project lists `requirements.txt`, so you can install dependencies using pip.
    ```bash
    pip install -r requirements.txt
    ```

## 📚 Usage

### Command Line Interface (CLI)

The primary way to interact with the engine is through the CLI.

#### Generating Truth Tables

To generate a truth table for a given logical expression, use the `truth_table` command:

```bash
python -m src.cli.main truth_table "<logical_expression>"
```

**Examples:**

*   **Simple AND:**
    ```bash
    python -m src.cli.main truth_table "P & Q"
    ```
    Output will display a truth table for P AND Q.

*   **Implication with negation:**
    ```bash
    python -m src.cli.main truth_table "~P > Q"
    ```
    Output will display a truth table for NOT P IMPLIES Q.

*   **More complex expression:**
    ```bash
    python -m src.cli.main truth_table "(P | Q) & ~(P & Q)"
    ```
    This represents the XOR operation.

#### Available Operators:
*   `&` : AND
*   `|` : OR
*   `~` : NOT
*   `>` : Implication
*   `=` : Biconditional
*   `^` : XOR

#### Notes:
*   Enclose your logical expression in double quotes (`"`) to prevent shell interpretation issues.
*   Variable names should be single letters (e.g., P, Q, R) or short alphanumeric strings.

### Programmatic Usage (Advanced)

You can also use the library directly within your Python code.

```python
from src.cli.truth_table import generate_truth_table_cli # Example import, adjust based on actual module structure

# This part would need to be adapted based on the actual public API of the library
# Example:
# expression = "P | ~Q"
# table_data = generate_truth_table(expression)
# print(table_data)
```
*(Note: The exact programmatic API might require further exploration of the `src` directory to define.)*

## ⚖️ License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPLv3)**. See the [LICENSE](LICENSE) file for more details.

## 🧑‍💻 Authors

*   **Luis Fernando** - *Initial work and development* - [luisfbl](https://github.com/luisfbl)
*   **Sergio Duarte** - *Refactoring and Improvements* - [sergiDM-0](https://github.com/sergiDM-0)

This project is an evolution of a previous codebase, with a significant rewrite (90%+) to improve performance and stability. Major changes include:
*   **Logical Parser Correction:** Addressed recursion error in unary operators (like negation `~`).
*   **Modular Architecture:** Clear separation between evaluation logic (`truth_table`) and user interface (`cli`).
*   **Error Handling:** Implemented validations to prevent unexpected crashes (`KeyError`).
*   **Licensing:** Standardization under **GNU AGPLv3** to ensure free software.
