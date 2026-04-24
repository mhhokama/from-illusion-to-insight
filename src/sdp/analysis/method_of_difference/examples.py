"""
Examples and tip templates for method-of-difference prompt generation.
"""

defect_examples = """
[Example]
In the following, you are given different kinds of defects along with their descriptions, 
an example, and the reason they are considered a defect.

[Defect1]
"pattern_name": "NullPointerException",
"description": "Accessing methods or fields on an object without checking for null.",
"example": "user.getName().toLowerCase();",
"why_is_defect": "Will throw NullPointerException if 'user' is null."
[/Defect1]

[Defect2]
"pattern_name": "ConcurrentModification",
"description": "Modifying a collection while iterating over it.",
"example": "for (String s : list) { list.remove(s); }",
"why_is_defect": "Causes ConcurrentModificationException at runtime."
[/Defect2]

[Defect3]
"pattern_name": "IndexOutOfBounds",
"description": "Accessing list or array elements using an invalid index.",
"example": "int x = array[5]; // when array.length == 5",
"why_is_defect": "ArrayIndexOutOfBoundsException will be thrown."
[/Defect3]

[Defect4]
"pattern_name": "EqualsAndHashCodeMismatch",
"description": "Overriding equals() without overriding hashCode().",
"example": "Only equals() method is implemented.",
"why_is_defect": "Leads to inconsistent behavior in hash-based collections."
[/Defect4]

[Defect5]
"pattern_name": "SilentExceptionCatching",
"description": "Catching Exception but not logging or handling it.",
"example": "try { ... } catch (Exception e) { }",
"why_is_defect": "Silences the error and makes debugging impossible."
[/Defect5]

[Defect6]
"pattern_name": "ResourceLeak",
"description": "Failing to close opened resources.",
"example": "InputStream in = new FileInputStream(\"file.txt\"); // no in.close()",
"why_is_defect": "Can exhaust system resources and lead to memory leaks."
[/Defect6]

[Defect7]
"pattern_name": "RaceCondition",
"description": "Accessing shared variables without synchronization in multithreaded context.",
"example": "sharedVar++; // without synchronized block",
"why_is_defect": "Results in unpredictable and incorrect program behavior."
[/Defect7]

[Defect8]
"pattern_name": "OffByOne",
"description": "Loop runs one time too many or too few.",
"example": "for (int i = 0; i < array.length; i++)",
"why_is_defect": "Incorrect loop boundaries may cause out-of-bounds access or missed iterations."
[/Defect8]

[Defect9]
"pattern_name": "IncorrectLogic",
"description": "Logical condition has wrong operator or structure.",
"example": "if (a = b) // meant to be '=='",
"why_is_defect": "Assignment instead of comparison leads to incorrect logic flow."
[/Defect9]

[Defect10]
"pattern_name": "InvalidCast",
"description": "Casting to an incorrect type without proper checks.",
"example": "Dog d = (Dog) animal; // without instanceof",
"why_is_defect": "Will throw ClassCastException at runtime."
[/Defect10]

[Defect11]
"pattern_name": "MutableDefaultField",
"description": "Using mutable objects as default field values shared across instances.",
"example": "private List<String> tags = new ArrayList<>();",
"why_is_defect": "Can lead to shared state across instances if the field is static or reused incorrectly."
[/Defect11]

[Defect12]
"pattern_name": "ImproperEqualsComparison",
"description": "Comparing objects using '==' instead of '.equals()'.",
"example": "if (name == \"John\")",
"why_is_defect": "Leads to incorrect logic when comparing Strings or objects."
[/Defect12]

[Defect13]
"pattern_name": "UncheckedExceptionHandling",
"description": "Not handling required checked exceptions like IOException.",
"example": "FileReader fr = new FileReader(\"file.txt\"); // no try/catch",
"why_is_defect": "May silently break functionality if exception is thrown."
[/Defect13]

[Defect14]
"pattern_name": "FieldShadowing",
"description": "Local variable hides class field with same name.",
"example": "this.count = count; // parameter 'count' hides field",
"why_is_defect": "Can result in uninitialized field or unexpected behavior."
[/Defect14]

[Defect15]
"pattern_name": "MemoryLeak",
"description": "Retaining references to objects no longer needed, preventing garbage collection.",
"example": "static List<Data> cache = new ArrayList<>(); // items never removed",
"why_is_defect": "Leads to increased memory usage and potential OutOfMemoryError."
[/Defect15]

[Defect16]
"pattern_name": "InfiniteLoop",
"description": "Loop condition never becomes false, causing the program to hang.",
"example": "while (i >= 0) { i++; }",
"why_is_defect": "Program gets stuck in an endless loop, consuming CPU."
[/Defect16]

[Defect17]
"pattern_name": "OffByTwoOrMore",
"description": "Loop boundaries are off by more than one, causing skipped or repeated iterations.",
"example": "for (int i = 0; i <= array.length + 1; i++)",
"why_is_defect": "Can cause IndexOutOfBoundsException or miss processing elements."
[/Defect17]

[Defect18]
"pattern_name": "WrongExceptionType",
"description": "Throwing or catching the wrong type of exception.",
"example": "catch(IOException e) { ... } // actually throws FileNotFoundException",
"why_is_defect": "Exception handling fails, causing crashes or silent failures."
[/Defect18]

[Defect19]
"pattern_name": "MagicNumberUsage",
"description": "Using hard-coded numbers instead of constants or enums.",
"example": "if (status == 3) { ... }",
"why_is_defect": "Makes code unreadable, error-prone, and hard to maintain."
[/Defect19]

[Defect20]
"pattern_name": "ImproperSynchronization",
"description": "Incorrect use of locks, leading to deadlocks or data corruption.",
"example": "synchronized(a) { synchronized(b) { ... } } // other thread locks b then a",
"why_is_defect": "Can cause deadlocks or inconsistent state."
[/Defect20]

[Defect21]
"pattern_name": "IncorrectInitialization",
"description": "Variables or objects used before proper initialization.",
"example": "int total; total += 5; // total not initialized",
"why_is_defect": "Leads to unpredictable behavior or compilation errors."
[/Defect21]

[Defect22]
"pattern_name": "OffByOneInArrayCopy",
"description": "Incorrectly copying array elements, causing data loss or corruption.",
"example": "System.arraycopy(src, 0, dest, 0, src.length + 1);",
"why_is_defect": "Throws IndexOutOfBoundsException or copies extra invalid elements."
[/Defect22]

[Defect23]
"pattern_name": "FloatingPointPrecisionError",
"description": "Relying on exact equality for floating-point comparisons.",
"example": "if (a + b == 0.3) { ... }",
"why_is_defect": "Floating-point rounding can lead to unexpected failures."
[/Defect23]

[Defect24]
"pattern_name": "IncorrectResourcePath",
"description": "Using wrong file, URL, or configuration path.",
"example": "FileReader fr = new FileReader(\"config.txt\"); // wrong folder",
"why_is_defect": "Causes FileNotFoundException or incorrect behavior."
[/Defect24]

[/Example]
"""

TIPS = """
Here are some useful tips:

---

**1. Scrutinize API Contract Changes Carefully**
- **Constructors and Public Methods**: Removing or altering public API elements (constructors, methods, constants) often introduces backward compatibility or functionality issues—treat these as high-risk unless migration plans are explicit.
- **Method Signatures**: Changes in parameters, return types, or making methods abstract are frequently *not* safe to assume as merely refactoring—they can break subclasses or clients.

**2. Evaluate Semantic Impact of Parameter and Constructor Changes**
- **Defaults & Flags**: Explicitly supplied parameters (like booleans, enums) can alter runtime behavior significantly. Confirm that defaults align with previous behavior, and that the change doesn’t switch modes silently.
- **Behavioral Effects**: Understand whether new parameters influence control flow, state, or concurrency semantics—not just data structure choices.

**3. Be Wary of Data Structure Substitutions**
- **Type and Equality Semantics**: Swapping arrays, lists, or collections with different implementations (arrays, sets, buffers) can change equality, mutability, or synchronization assumptions, impacting correctness.
- **Internal Handling**: Verify whether data normalization, identity checks, or locking assumptions aren't invalidated.

**4. Recognize that Annotations and Language Features Can Have Behavioral Effects**
- **Annotations (like @Override)**: Can create compile-time constraints; adding/removing them may cause compilation failures or change overriding behavior.
- **Language Features (Generics, Raw Types)**: Moving between raw types and generics, or removing casts, can introduce subtle type errors or runtime `ClassCastException`s—treat these as potential defects.

**5. Watch for Changes in Lifecycle, Initialization, and State Management**
- **Constructor Removals / Modifications**: Those that perform necessary initialization may lead to uninitialized state or incorrect runtime behavior.
- **Order of Execution**: Reflect on whether code refactors alter sequence-dependent setup logic.

**6. Consider the External Contract and Consumer Impact**
- **Backward Compatibility**: Changes to public classes, methods, or interfaces often impact external clients; treat them with suspicion until explicitly migrated.
- **Testing & Usage Patterns**: Review test coverage for those APIs. Even if no new code is added, existing tests might reveal regressions.

**7. Treat Silent Behavioral Changes as Defects**
- Minor refactors, style updates, or “improvements” that conceal changed assumptions or logic pathways should be validated through behavioral tests or formal invariants.
- Subtle differences in handling edge cases, exceptions, or concurrency are common sources of defects.

---

**Summary:**
When classifying code changes, focus not only on *what* changed but *why*, ensuring that changes not only look safe syntactically but also preserve *behavioral semantics*, *API contracts*, and *system invariants*. High-risk patterns include removal or alteration of public interfaces, constructor and initialization modifications, data structure substitutions affecting equality semantics, and any change influencing control flow, concurrency, or resource management.
"""
