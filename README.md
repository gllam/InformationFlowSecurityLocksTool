# Information Flow Security Locks Tool ReadMe

Welcome to our code analysis tool! This tool helps you analyze programs for security vulnerabilities based on the type system presented in the related paper (Information Flow Security For a Concurrent Language With Lock-based Synchronization). To get started, please follow the instructions below.

## Prerequisites

Before you can use this code analysis tool, make sure you have Python installed on your system. If you haven't installed Python yet, you can download it from [python.org](https://www.python.org/downloads/).

## Usage

To analyze your code using this tool, follow these simple steps:

1. **Variables File (variables.txt)**: Create a `variables.txt` file with the free variables you want to analyze in your program. Each variable should follow the structure: `nameVariable:securityLevel,type;securityLevel,type; ...` The security levels are associated with the sensitivity of the variable, where "bot" represents the lowest security level for integers. For example:

```python
 username:h,ref;bot,int
```

In this example, `username` is a high-security level pointer, that contains a bot-security level integer.

2. **Program File (program.txt)**: Create a `program.txt` file that contains the program you want to analyze. Ensure that the program is written in the specified language for this tool.

3. **Running the Tool**: Open your terminal or command prompt, navigate to the project's folder, and execute the following command:

```shell
python3 .\main.py program.txt variables.txt
```

The tool will analyze your program based on the security levels defined in `variables.txt` and provide insights into potential security vulnerabilities. Make sure to review the output and take necessary actions to address any identified issues.

Feel free to explore our tool and enhance your program's security in concurrent programs with locks as the synchronization primitive.

If you have any questions or encounter issues, please don't hesitate to reach out to us for support.

Happy coding and secure programming! 👨‍💻🔒


