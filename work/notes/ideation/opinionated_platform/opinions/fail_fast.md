+++
title = "Fail Fast, Formulate Feedback!"
author = "Stijn Dejongh"
problem = "Invalid input data causing your software to crash midway through its execution is expensive, both in terms of processing power and resolution time."
description = "Validate input data before processing to avoid unnecessary resource consumption and ensure efficient error handling."
summary="""
Prevent costly crashes and wasted resources in your software by validating input data upfront. Learn how to implement a 'fail fast' approach with clear feedback mechanisms, ensuring your applications run smoothly even when unexpected errors arise. Explore practical examples and tips for improving data processing efficiency.
"""
categories = [
    "software development",
]
tags = [
    "Efficiency", "Testing", "Programming", "Design"
]
uuid="336b0448-e78b-4428-83a5-d4d473afda63"
aliases=["336b0448-e78b-4428-83a5-d4d473afda63"]
outputs = ['html', 'json']
ammerse = [
  {name = "agile", delta = "0.1", rationale = "The practice supports agility by catching errors early, but it may introduce some rigidity due to the complexity of validation rules, which can limit quick adaptability."},
  {name = "minimal", delta = "0.5", rationale = "The technique promotes minimalism by avoiding unnecessary processing, but the initial setup and complexity of validation might introduce some overhead, reducing the minimalistic approach slightly."},
  {name = "maintainable", delta = "0.5", rationale = "While the practice generally supports maintainability by ensuring errors are caught early, the overhead of maintaining complex validation rules can detract from this, leading to potential long-term maintenance challenges."},
  {name = "environmental", delta = "0.5", rationale = "The technique improves user experience by reducing the need for repeated submissions, but the necessity of balancing security with user feedback and potential complexity of validation rules slightly limits its broader environmental impact."},
  {name = "reachable", delta = "0", rationale = "The technique has a minimal impact on goal achievement. While it ensures reliability and prevents errors, the overhead from maintaining complex validation rules can slightly detract from its effectiveness in supporting goal attainment."},
  {name = "solvable", delta = "1", rationale = "The practice is highly effective in problem-solving, as it catches errors early and provides clear feedback, significantly improving the ability to address and resolve issues quickly."},
  {name = "extensible", delta = "0.4", rationale = "The practice is moderately extensible, as validation logic can be adapted to different scenarios, but maintaining and updating these rules as the system evolves can present challenges."}
]
pubdate="2024-05-18"
image="practices/fail_fast_feedback"
related_concepts = [
]
related_practices = [
  "1848f4a6-3acb-4dc8-aa49-e57a1b87cf3b"
]
further_exploration = [
  {type="biblio", id="8572443d-2c27-462a-b9d7-839dd6e4d58b"},
  {type="biblio", id="704fb2a3-0207-4f8d-87f9-31b7fa5949c0"},
  {type="raw", author="Software Design Knights", year="2021", title="Fail Fast (FF)", site="PrinciplesWiki.net", link="http://principles-wiki.net/principles:fail_fast" },
  {type="raw", author="SD Development", year="2023", title="Java Modular Validators", site="GitHub.com", link="https://github.com/sddevelopment-be/modular-validators" },
  {type="raw", author="Gorts, S.", year="2023", title="Better Validation Rules with ValidationResults", publisher="Self-published on Public Domain", link="/attachments/GORTS_Better-Validation-Rules.pdf" }
]
+++

## Problem statement

Invalid input data causing your software to crash midway through its execution is costly in terms of processing power and resolution time.

## Intent

Avoid wasting resources by not processing data known to be invalid. Provide clear feedback on errors in the input data to facilitate quick
resolution.

## Solution

When processing data, validate as much of the input as possible before processing. This typically involves checking whether:

* The input data is present
* The input is in the expected format
* All required fields are present
* The data is within the expected range
* The data is logically consistent
* No duplicates are present

If any of these checks fail, halt processing and provide feedback on what is wrong with the input data. Feedback can range from a simple message to
the user, a detailed error log for internal use, or a notification event sent to a logging and auditing system.

{{<tip text=`
In cases where confidentiality or security is a concern, consider providing a generic error message to the user while recording a detailed error log for internal use.
Example:

     An error occurred while processing your request. 
     We apologize for the inconvenience. Our development team has been notified and will take corrective action. 

     If you want to be notified when the issue is resolved,
     please contact our support team and provide the following reference number: 1234567890
` >}}

## Contextual forces

### Enablers
The following factors support effective application of the practice:

* Processing data is a core task of software applications
* Clear understanding of the expected input data format and structure
* Software designed to handle errors gracefully, allowing for quick recovery from unexpected issues
* Established logging and monitoring infrastructure to capture and analyse detailed error information
* Existing robust input validation mechanisms, making comprehensive checks easier to implement early in the process

### Deterrents
The following factors prevent effective application of the practice:

* Validation checks are computationally expensive, introducing unacceptable latency or resource consumption
* Lack of experience or expertise in implementing effective error handling and validation mechanisms
* Input data specifications are unclear or frequently changing
* Absence of adequate logging infrastructure
* Errors are seldom monitored or acted upon

## Application

### Consequences
While the approach brings numerous benefits in terms of efficiency and reliability, it can also lead to several unexpected or undesired outcomes:

* **Increased User Frustration:** If the validation process is too strict or frequently results in errors, users might become frustrated,
  especially if they don't understand why their input is being rejected. This can lead to a negative user experience, particularly if the error
  messages are not clear or helpful.
* **False Positives:** Overly aggressive validation checks can sometimes reject valid data as erroneous, leading to what are known as false
  positives. This can prevent legitimate data from being processed and may cause disruptions in workflows or services.
* **Performance Overhead:** While validation is meant to save resources by preventing the processing of bad data, in some cases, the validation
  process itself can become a significant performance bottleneck. This is especially true if the checks are complex, require interaction with
  external systems, or if they are applied to large datasets.
* **Maintenance Burden:** As the number of validation rules increases, the complexity of maintaining them can grow. This can lead to higher
  maintenance costs and the risk of introducing bugs during updates or changes to the validation logic.
* **Security Risks from Detailed Feedback:** Providing detailed error messages as part of the "fail fast" approach can inadvertently expose
  sensitive information about the system's internals. This can be exploited by malicious users to gain insights into how the system works or to
  identify potential vulnerabilities.
* **Dependency on Accurate Specifications:** The effectiveness of the "fail fast" approach relies heavily on having accurate and stable input data
  specifications. If these specifications are unclear, incomplete, or frequently changing, the validation logic can quickly become outdated, leading
  to more errors and a less stable system.

### Mitigation strategies

To mitigate the potential negative consequences of the approach:

* **Balance Validation Rigor with Performance:** Ensure that your validation checks are comprehensive but not overly complex. Focus on
  validating the most critical aspects of the input data that could cause significant failures, while avoiding checks that add unnecessary overhead.
* **Design User-Friendly Error Messages:** When providing feedback on validation failures, craft messages that are clear, concise, and
  informative. For end-users, avoid exposing technical details that could confuse them or expose vulnerabilities. Instead, use generic messages that
  maintain security while offering a path to resolution. Internally, maintain detailed logs that developers can use to diagnose and fix issues.
* **Implement Progressive Validation:** In scenarios where input data is extensive or complex, consider breaking down the validation process
  into stages. This allows you to catch and report errors as early as possible without delaying the overall process. For example, validate the
  presence of required fields first, then move on to format checks, and finally perform more detailed logical consistency checks.
* **Use Validation Libraries:** Instead of writing custom validation logic from scratch, leverage existing validation libraries or frameworks
  that have been optimized for performance and security. This not only reduces development time but also ensures that your validation processes are
  built on well-tested and reliable code.
* **Regularly Review and Update Validation Rules:** As your application evolves, so will the types of input data it processes. Periodically
  review and update your validation rules to ensure they remain relevant and effective. This is especially important in dynamic environments where
  data specifications may change frequently.

## Examples

### Python Data Processing

#### Outline

Say you are writing code to process a data file containing information about characters in a fictional universe. 
Your data supplier tells you the file will have the following fields: `allegiance`, `homeworld`, `species`, and `name`. 
The goal is to use this input data and convert it to a Markdown table to be used inside a publication of sorts. 

You are given the file `star_wars_characters_example.csv` as a reference input file.

```csv
name,height,mass,hair_color,skin_color,eye_color,birth_year,gender,homeworld,species,allegiance
Luke Skywalker,172,77,blond,fair,blue,19BBY,male,Tatooine,Human,Light Side
C-3PO,167,75,NA,gold,yellow,112BBY,NA,Tatooine,Droid,Light Side
R2-D2,96,32,NA,"white, blue",red,33BBY,NA,Naboo,Droid,Light Side
Darth Vader,202,136,none,white,yellow,41.9BBY,male,Tatooine,Human,Dark Side
```

Passing this input file to your script should result in the following Markdown table:

```markdown
| allegiance | homeworld | species | name           |
|------------|-----------|---------|----------------|
| Light Side | Tatooine  | Human   | Luke Skywalker |
| Light Side | Tatooine  | Droid   | C-3PO          |
| Light Side | Naboo     | Droid   | R2-D2          |
| Dark Side  | Tatooine  | Human   | Darth Vader    |
```

You can write a simple Python script that is able to process the file and generate the markdown output table.
The script below reads the input file and processes it line by line, checking if all the required fields are present in the input file.
When a field is missing, the script will print an error message and exit the script.

```python
import csv
import sys
from enum import Enum


class HeaderFields(Enum):
    ALLEGIANCE = 'allegiance'
    HOME_WORLD = 'homeworld'
    SPECIES = 'species'
    NAME = 'name'


def process_file(file_to_process):
    with open(file_to_process, newline='') as file:

        print('|', ' | '.join([field.value for field in HeaderFields]), end=' |\n', file=sys.stdout, flush=False)
        print('|', ' | '.join(['---' for _ in HeaderFields]), end=' |\n', file=sys.stdout, flush=False)
        data = csv.DictReader(file)
        for i, row in enumerate(data):
            output = []
            for field in HeaderFields:
                if field.value not in row:
                    print('Error: Missing field [', field.value, '] in input file at line: ', i + 1)
                    sys.exit(1)
                output.append(row[field.value])
            print('|', ' | '.join(output), end='|\n', file=sys.stdout, flush=False)


def main():
    if len(sys.argv) < 2:
        print("Usage: python dataLoader.py <filename>")
        sys.exit(1)

    input_file = sys.argv[1]
    process_file(file_to_process=input_file)


if __name__ == "__main__":
    main()
```

#### Problem

Your script works as expected, but when you receive the real data file from the supplier, the output of your code is:

```shell
| allegiance | homeworld | species | name |
|------------|-----------|---------|------|
Error: Missing field [ allegiance ] in input file at line:  1
```

Given the error message, you can see that the `allegiance` field is missing in the input file.
The script stops processing the file and exits, so you have to change your code or data file to match the expected structure.

Imagine you have a large amount of data files with many lines, and you need to check each of them for missing fields.
For this example, the amount of fields is small, but in a real-world scenario, you could have dozens (if not hundreds) of fields to check.
Running the program for each file, checking the output, and making the required change is a tedious proposition.

#### Solution using Fail Fast structure

Rather than processing the file line by line, until we encounter an error, you can read the first line of the file and check if all the required fields are present. 

The `main` function is updated to first validate the input file, and then process the file only if the validation is successful.

```python
def main():
    if len(sys.argv) < 2:
        print("Usage: python dataLoader.py <filename>")
        sys.exit(1)

    input_file = sys.argv[1]
    is_valid = validate_file(file_to_check=input_file)
    if not is_valid:
        print('Error: Invalid input file, SKIPPING [', input_file, ']')
    else:
        process_file(file_to_process=input_file)
```

Our new `validate_file` function reads the first line of the file and checks if all the required fields are present.
Furthermore, this new version of the function will give you detailed feedback on which fields are missing in the provided input file.

```python
def validate_file(file_to_check):
    is_valid = True
    with open(file_to_check, newline='') as file:
        header = next(csv.reader(file))
        for field in HeaderFields:
            if field.value not in header:
                print('Error: Missing field [', field.value, '] in input file [', file_to_check, ']')
                is_valid = False
    return is_valid
```

If we run the script with the real data file, the output will be:

```shell
Error: Missing field [ allegiance ] in input file [ star_wars_hair_dressers_database.csv ]
Error: Missing field [ homeworld ] in input file [ star_wars_hair_dressers_database.csv ]
Error: Missing field [ species ] in input file [ star_wars_hair_dressers_database.csv ]
Error: Invalid input file, SKIPPING [ star_wars_hair_dressers_database.csv ]
```

Taking a look at the error message, you can see that the `allegiance`, `homeworld`, and `species` fields are missing in one of the input files.
This is suspicious as the supplier told you that all files would have the same structure. Taking a closer look at the erroneous file, you can see 
that the supplier made a mistake, and sent you the data intended for the 'Galactic Hairdressers Data Convention'.

```csv
name,hair_color
Luke Skywalker,blond
C-3PO,NA
R2-D2,NA
Darth Vader,none
```

You can now contact the supplier and ask for the correct file.

{{<tip text=`
Failing fast with full feedback allows you to save valuable system resources and troubleshoot the issue quickly.
In real-world scenarios, you could have hundreds of files to check, and the processing of the data is likely to be computationally expensive.
` >}}

## Criticism & Clarifications

- Over-validating can slow hot paths or break incompatible clients; profile frequently and version contracts when behaviour must change.
- Error payloads need governance—reveal enough detail for remediation without leaking internals an attacker can weaponise.
- A fail-fast culture still needs recovery stories: pair quick exits with observability, retries, or compensating workflows so the user can succeed.