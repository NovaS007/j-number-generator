# J-Number Generator

A powerful Python application for generating, analyzing, and exploring J-numbers in any integer base. Features a user-friendly GUI for exploring mathematical properties of J-numbers, including prime factorization and export to CSV/Excel.

## What is a J-Number?

A **J-number** is a generalized number sequence defined as:

**J_k(a,b,c) = ab followed by c repeated k times**

Where:
- `a`, `b`, `c` are digits in your chosen base (0 to base-1)
- `k` is the number of times digit `c` is repeated
- The base can be any integer ≥ 2

### Examples in Base 10

For the seed (a=1, b=2, c=3):

| k | J_k(1,2,3) | Interpretation |
|---|------------|---|
| 0 | 12 | Just ab |
| 1 | 123 | ab + c once |
| 2 | 1233 | ab + cc |
| 3 | 12333 | ab + ccc |
| 4 | 123333 | ab + cccc |

### Why J-Numbers?

J-numbers are interesting for number theory research because:
- They follow a predictable mathematical pattern
- Their prime factorizations often reveal surprising structures
- Different bases reveal different mathematical properties
- They're useful for exploring generalized digit sequences

## Installation

### Requirements

- Python 3.8+
- pandas
- openpyxl
- sympy

### Setup

1. Clone or download this project
2. Install dependencies:
```bash
pip install pandas openpyxl sympy
```

3. Run the GUI:
```bash
python -m j_numbers.gui.main_window
```

Or if running from the `j_numbers` directory:
```bash
python gui/main_window.py
```

## How to Use the Program

### Launching the GUI

```bash
python -m j_numbers.gui.main_window
```

The GUI will open with a clean interface for generating and analyzing J-numbers.

### Main Features

#### 1. **Basic Generation**

- **Base**: Choose any base ≥ 2 (default: 10)
- **k (max c repeats)**: How many times to repeat digit c (default: 15)
- Click **"Generate and Save CSV"** to generate all J-numbers

#### 2. **Filtering (Optional Seed Digits)**

Generate specific J-numbers by providing seed digits:

- **Seed a**: Fix the first digit (leave blank for all values 0 to base-1)
- **Seed b**: Fix the second digit (leave blank for all)
- **Seed c**: Fix the repeated digit (leave blank for all)

**Examples:**
- Leave all blank: Generates all J-numbers for the base
- Set a=1, b=2, leave c blank: Generates J_k(1,2,c) for all c values
- Set a=1, b=2, c=3: Generates only J_k(1,2,3) for k=0 to max_repeat

#### 3. **Output Display**

- **Show results in window**: Toggle to display results in the application
- Results show: j_num, seed digits (a,b,c), k value, prime factors, and whether the number is prime

#### 4. **Exporting Data**

**CSV Export:**
- Automatically prompted when generating
- Save location: Defaults to Desktop (customizable)
- Format: One J-number per row with all data columns

**Excel Export:**
- Click **"Export to Excel"** button
- Prime factors automatically split into separate columns (pf_0, pf_1, etc.)
- Great for data analysis in Excel/Sheets

#### 5. **Clearing Output**

- Click **"Clear Output"** to remove results from the display

### Typical Workflow

1. **Set Parameters**
   - Choose a base (e.g., 10, 16, 2)
   - Set k value (higher = more numbers generated)

2. **(Optional) Filter by Seed**
   - Set a, b, c if you want specific numbers only

3. **Generate**
   - Click "Generate and Save CSV"
   - Choose save location
   - Results appear in the window

4. **Analyze**
   - View prime factorizations in the window
   - Click "Export to Excel" for detailed analysis

## Examples

### Example 1: Base 10, All Seeds

**Settings:**
- Base: 10
- k: 5
- No seed filters

**Result:** Generates all 1000 J-numbers (base³ = 10³) with k from 0-5, showing their prime factorizations.

### Example 2: Binary (Base 2) Numbers

**Settings:**
- Base: 2
- k: 10
- No seed filters

**Result:** Generates 8 J-numbers (2³ = 8) in binary notation.

### Example 3: Specific Sequence

**Settings:**
- Base: 10
- k: 10
- Seed a: 1
- Seed b: 2
- Seed c: (leave blank)

**Result:** Generates 10 J-numbers: J_k(1,2,0), J_k(1,2,1), ..., J_k(1,2,9) for k=0-10.

### Example 4: Single J-Number

**Settings:**
- Base: 10
- k: 15
- Seed a: 1, b: 2, c: 3

**Result:** Shows only J_k(1,2,3) for k=0-15 with complete factorization.

## Understanding the Output

### CSV Columns

| Column | Description |
|--------|---|
| `j_num` | The computed J-number value |
| `a` | First digit of seed |
| `b` | Second digit of seed |
| `c` | Repeated digit |
| `k` | How many times c was repeated |
| `prime_factors` | Semicolon-separated list of prime factors |
| `is_prime` | 1 if j_num is prime, 0 otherwise |

### In-Window Display Format

```
j_num | a b c k | prime_factors | is_prime
12 | a=1 b=2 c=0 k=0 | [2, 2, 3] | 0
```

## File Structure

```
j_numbers/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── calculations.py      # J-number generation logic
│   └── factorizations.py    # Prime factorization
├── gui/
│   ├── __init__.py
│   └── main_window.py       # Tkinter GUI application
└── io/
    ├── __init__.py
    └── csv_writer.py        # CSV export functionality
```

## Advanced Usage

### Programmatic Access

You can also use the J-number generator in your own Python code:

```python
from j_numbers.core import calculations

# Generate all J-numbers for base 10, k up to 5
results = calculations.getAllJNums(max_repeat=5, base=10)

# Generate for a specific seed
results = calculations.getJNumsForSeed(a=1, b=2, c=3, max_repeat=10, base=10)

# Fast path for fixed a,b
results = calculations.getJNumsForAB(a=1, b=2, max_repeat=15, base=10)
```

## Mathematical Notes

- **Formula**: J_k(a,b,c) = a·base^(k+1) + b·base^k + c·(base^k - 1)/(base - 1)
- **Uniqueness**: The same J-number value can be derived from different (a,b,c,k) combinations; the tool stores unique values only
- **Prime Factorization**: Uses sympy for accurate factorization
- **Base Generalization**: Works for any base ≥ 2, including binary (2), octal (8), hexadecimal (16), etc.

## Troubleshooting

### "Base and k must both be integers"
- Ensure both Base and k fields contain only numbers
- No text or special characters allowed

### "Base must be at least 2"
- Enter a base value of 2 or higher

### "Seed digits must be between 0 and X"
- For base 10, digits must be 0-9
- For base 16, digits must be 0-15
- Adjust based on your chosen base

### Excel export fails
- Ensure openpyxl is installed: `pip install openpyxl`

## Performance Notes

- **Small k values** (0-10): Very fast, even in base 10
- **Large k values** (20+): May take a few seconds depending on hardware
- **High bases** (base > 20): Generates many numbers; be patient
- **Filtering**: Providing seed digits significantly speeds up generation

## Contributing

This project is open for enhancement. Potential improvements:
- Additional statistical analysis
- Visualization of prime factor distributions
- Batch processing for multiple bases
- Custom mathematical filters

## License

Created for mathematical exploration and research.

## Questions?

Explore the code in `j_numbers/core/calculations.py` to understand the mathematical implementation, or modify the GUI in `j_numbers/gui/main_window.py` to add custom features.

