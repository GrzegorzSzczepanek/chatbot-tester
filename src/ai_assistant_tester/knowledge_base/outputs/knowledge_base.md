

```markdown
# EG-Zine - My Website

## Blog Posts

### Using Radare2 for Simple Binary Analysis
- **Date:** 2021-07-13
- **Tags:** #reverse engineering, #radare2, #linux

#### Overview
Radare2 is a reverse engineering framework developed by "Pancake" and contributors on GitHub. It is the successor to "Radare," created in 2006 for simple hexadecimal editing and data recovery. Radare stands for RAw DAta REcovery, initially designed to recover deleted PHP files from an HFS partition.

### Bash - Input/Output Redirections and Pipes
- **Date:** 2020-10-07
- **Tags:** #bash, #pipes, #linux

#### Overview
Bash (Bourne Again Shell) was created by Brian Fox and volunteers from the GNU project as an open-source alternative to the "sh" shell. Released in 1989, Bash has become the standard shell in Linux terminals due to its ease of use and learning curve, while also offering advanced features for experienced users.

## Tags

- **#bash** (1 post)
  - Bash - Input/Output Redirections and Pipes

- **#linux** (2 posts)
  - Using Radare2 for Simple Binary Analysis
  - Bash - Input/Output Redirections and Pipes

- **#pipes** (1 post)
  - Bash - Input/Output Redirections and Pipes

- **#radare2** (1 post)
  - Using Radare2 for Simple Binary Analysis

- **#reverse engineering** (1 post)
  - Using Radare2 for Simple Binary Analysis

## About Me
Hello, World!

## Blog Archive

- **2021-07-13**
  - Using Radare2 for Simple Binary Analysis

- **2020-10-07**
  - Bash - Input/Output Redirections and Pipes
```


```markdown
# EG-Zine - My Website

## Blog Post: Using Radare2 for Simple Binary Analysis

- **Date:** 2021-07-13
- **Tags:** #reverse engineering, #radare2, #linux

### Overview
Radare2 is a reverse engineering framework developed by "Pancake" and contributors on GitHub. It evolved from "Radare," a tool created in 2006 for hexadecimal editing and data recovery. Radare2 was rewritten to support a modular design, allowing for extensive future enhancements. It is widely used in binary analysis and reverse engineering, with its source code available on [GitHub](https://github.com/radareorg/radare2) under the LGPLv3 license.

### Note about Rizin
In December 2020, some Radare2 contributors forked the project to create "Rizin," due to differing project directions. Currently, Rizin remains similar to Radare2, but this may change.

### Installation

#### Linux
- **Recommended:** Clone the Radare2 GitHub repository and build from source:
  ```bash
  git clone https://github.com/radareorg/radare2
  cd radare2
  sys/install.sh
  ```
- **Alternative:** Use prebuilt binaries via package managers (e.g., `sudo apt install radare2` or `sudo pacman -S radare2`). Note that these may be outdated.

#### MacOS
- **Recommended:** Same as Linux.
- **Alternative:** Use a package manager like Brew, though not officially supported.

#### Windows
- Use prebuilt binaries from the Radare2 GitHub release page or a package manager like Chocolatey.

### Binary Analysis Example

#### Source Code for Challenge
```c
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    printf("PASSWORD: ");
    char password[64];
    int ret;
    scanf("%s", password);
    ret = strncmp(password, "S3CR3T_P455W0RD", 64);
    if (ret == 0) {
        printf("Access granted\n");
    } else {
        printf("Try again\n");
    }
    return 0;
}
```
- **Compile on Linux:** `gcc file_name.c -o crackme`

#### Analyzing the Binary
1. **Open Binary:** Ensure Radare2 is in your PATH or copy the binary to the build directory. Open with:
   ```bash
   r2 crackme
   ```
   On Windows:
   ```bash
   .\radare2.exe crackme.exe
   ```

2. **Help System:** Use `?` to explore commands, e.g., `a?` for analysis options.

3. **Analyze Binary:** Use `aaa` to analyze the binary, extracting function positions and names.

4. **Print Functions:** Use `afl` to list functions. The main function is a good starting point.

5. **Navigate to Main Function:** Use `s main` to move to the main function.

6. **Print Disassembly:** Use `pdf` to view disassembled instructions.

7. **Graph View:** Use `VV` for a graphical representation of the function flow.

#### Cracking the Binary
1. **Open in Write Mode:** Use `oo+` to enable modifications.
2. **Modify Instruction:** Change `jne` to `je` at the address of interest using:
   ```bash
   s 0x000011e3
   wa je 0x11f6
   ```
3. **Verify Changes:** Use `VV` to confirm the instruction change.

#### Conclusion
Running the modified binary with any password should now grant access, demonstrating a successful crack. This overview introduces basic Radare2 functions, encouraging further exploration of binary exploitation.

## Additional Reading
- [Bash - Input/Output Redirections and Pipes](#)
```

```markdown
# EG-Zine - My Website

## Blog Posts

### Using Radare2 for Simple Binary Analysis
- **Date:** 2021-07-13
- **Tags:** #reverse engineering, #radare2, #linux

#### Overview
Radare2 is a reverse engineering framework developed by "Pancake" and contributors on GitHub. It evolved from "Radare," a tool created in 2006 for hexadecimal editing and data recovery. Radare2 was rewritten to support a modular design, allowing for extensive future enhancements. It is widely used in binary analysis and reverse engineering, with its source code available on [GitHub](https://github.com/radareorg/radare2) under the LGPLv3 license.

#### Note about Rizin
In December 2020, some Radare2 contributors forked the project to create "Rizin," due to differing project directions. Currently, Rizin remains similar to Radare2, but this may change.

#### Installation

##### Linux
- **Recommended:** Clone the Radare2 GitHub repository and build from source:
  ```bash
  git clone https://github.com/radareorg/radare2
  cd radare2
  sys/install.sh
  ```
- **Alternative:** Use prebuilt binaries via package managers (e.g., `sudo apt install radare2` or `sudo pacman -S radare2`). Note that these may be outdated.

##### MacOS
- **Recommended:** Same as Linux.
- **Alternative:** Use a package manager like Brew, though not officially supported.

##### Windows
- Use prebuilt binaries from the Radare2 GitHub release page or a package manager like Chocolatey.

#### Binary Analysis Example

##### Source Code for Challenge
```c
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    printf("PASSWORD: ");
    char password[64];
    int ret;
    scanf("%s", password);
    ret = strncmp(password, "S3CR3T_P455W0RD", 64);
    if (ret == 0) {
        printf("Access granted\n");
    } else {
        printf("Try again\n");
    }
    return 0;
}
```
- **Compile on Linux:** `gcc file_name.c -o crackme`

##### Analyzing the Binary
1. **Open Binary:** Ensure Radare2 is in your PATH or copy the binary to the build directory. Open with:
   ```bash
   r2 crackme
   ```
   On Windows:
   ```bash
   .\radare2.exe crackme.exe
   ```

2. **Help System:** Use `?` to explore commands, e.g., `a?` for analysis options.

3. **Analyze Binary:** Use `aaa` to analyze the binary, extracting function positions and names.

4. **Print Functions:** Use `afl` to list functions. The main function is a good starting point.

5. **Navigate to Main Function:** Use `s main` to move to the main function.

6. **Print Disassembly:** Use `pdf` to view disassembled instructions.

7. **Graph View:** Use `VV` for a graphical representation of the function flow.

##### Cracking the Binary
1. **Open in Write Mode:** Use `oo+` to enable modifications.
2. **Modify Instruction:** Change `jne` to `je` at the address of interest using:
   ```bash
   s 0x000011e3
   wa je 0x11f6
   ```
3. **Verify Changes:** Use `VV` to confirm the instruction change.

##### Conclusion
Running the modified binary with any password should now grant access, demonstrating a successful crack. This overview introduces basic Radare2 functions, encouraging further exploration of binary exploitation.

## Additional Reading
- [Bash - Input/Output Redirections and Pipes](#)
```

```markdown
# EG-Zine - My Website

## Blog Post: Bash - Input/Output Redirections and Pipes

- **Date:** 2020-10-07
- **Tags:** #bash, #pipes, #linux

### Overview
Bash (Bourne Again Shell) was created by Brian Fox and volunteers from the GNU project as an open-source alternative to the "sh" shell. Released in 1989, Bash has become the standard shell in Linux terminals due to its ease of use and learning curve, while also offering advanced features for experienced users. Although there are alternatives with more advanced functionality, Bash remains popular for its simplicity and widespread use.

### Understanding the Shell
The shell is a command interpreter that reads user input from the terminal, communicates with the OS to execute commands, and returns output to the terminal. It uses three main streams:
- **Standard Input (stdin):** File descriptor 0, typically the keyboard.
- **Standard Output (stdout):** File descriptor 1, displays output in the terminal.
- **Standard Error (stderr):** File descriptor 2, used for error messages.

### How Command Line Works
When a command is entered, the shell processes it, executes the corresponding program, and returns the output or error message based on the return value:
- **0:** Success, output to stdout.
- **1:** Error, output to stderr.

### Bash Pipes
Pipes (`|`) redirect output from one command to the input of another. Example:
```bash
ls -lah | grep asdf.py
```
This command lists files and filters the output to show only lines containing "asdf.py".

### Bash Input/Output Redirections
Redirections use `<` and `>` to direct data flow:
- **Output Redirection (`>`):** Directs stdout to a file.
  ```bash
  ls > files.txt
  ```
- **Append (`>>`):** Adds output to the end of a file.
  ```bash
  ls -lah >> files.txt
  ```
- **Input Redirection (`<`):** Directs file content to a command.
  ```bash
  grep word < file.txt
  ```
- **Stream Redirection:** Redirects specific streams using file descriptors.
  ```bash
  find / -name usr 2> /dev/null
  ```

### Combining Redirections
Multiple redirections can be used in a single command:
```bash
grep word < file.txt > result.txt
```
This searches for "word" in `file.txt` and writes the results to `result.txt`.

### Conclusion
This guide provides a foundational understanding of Bash, its command line operations, and the use of pipes and redirections. While this is a basic overview, there is much more to explore in Bash scripting and command line operations.

## Additional Reading
- [Using Radare2 for Simple Binary Analysis](#)
```