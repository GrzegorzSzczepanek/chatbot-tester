

```markdown
# EG-Zine - My Website

## Blog Posts

### Using radare2 for Simple Binary Analysis
*Date: 2021-07-13*  
*Tags: #reverse engineering, #radare2, #linux*

Radare2 is a reverse engineering framework developed by "Pancake" and contributors on the public GitHub repository. It is the second version of a project called "Radare," which was initiated in 2006 by "Pancake" to create a simple hexadecimal editor. The original purpose was to support pattern searching and dumping search results to recover deleted PHP files from an HFS partition. The name Radare stands for RAw DAta REcovery.

---

### Bash - Input/Output Redirections and Pipes
*Date: 2020-10-07*  
*Tags: #bash, #pipes, #linux*

Bash (Bourne Again Shell) was created by Brian Fox with contributions from volunteers of the GNU project as an open-source alternative to the older "sh - shell." First released in 1989, Bash has become the de facto standard for shell environments in Linux terminals. Its widespread adoption is due to its status as the default shell in most Linux distributions, offering ease of use for beginners while providing advanced features for experienced users.

---

## Tags
- **bash** (1 post)
- **linux** (2 posts)
- **pipes** (1 post)
- **radare2** (1 post)
- **reverse engineering** (1 post)

---

## About Me
Hello, World!
```


```markdown
# EG-Zine - My Website

## Blog Posts

### Using radare2 for Simple Binary Analysis
*Date: 2021-07-13*  
*Tags: #reverse engineering, #radare2, #linux*

#### Overview
Radare2 is a reverse engineering framework developed by "Pancake" and contributors on GitHub. It is the successor to the original Radare project, which began in 2006 as a simple hexadecimal editor aimed at recovering deleted PHP files from an HFS partition. The name Radare stands for RAw DAta REcovery.

Radare2 was designed with a modular architecture to allow for extensive future enhancements. Since its inception, it has become one of the most popular frameworks for binary analysis and reverse engineering. The source code is available on [GitHub](https://github.com/radareorg/radare2) and is licensed under the LGPLv3.

#### Note on Rizin
In December 2020, some key contributors of Radare2 forked the project to create "Rizin" due to disagreements on the project's direction. As of now, both projects remain similar, but this may change in the future.

#### Installation

**Linux:**
1. Clone the repository and build from source:
   ```bash
   git clone https://github.com/radareorg/radare2
   cd radare2
   sys/install.sh
   ```
2. Alternatively, use your package manager (note that this may install an outdated version):
   ```bash
   sudo apt install radare2  # For Debian/Ubuntu
   sudo pacman -S radare2    # For Arch
   ```

**MacOS:**
- Follow the same installation steps as for Linux or use Homebrew (not officially supported).

**Windows:**
- Download prebuilt binaries from the [release page](https://github.com/radareorg/radare2/releases) or use Chocolatey.

#### Example Challenge: Cracking a Simple Binary
The following C code represents a simple challenge binary:

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

To compile this code on Linux:
```bash
gcc file_name.c -o crackme
```

#### Analyzing the Binary
1. Open the binary with Radare2:
   ```bash
   r2 crackme
   ```
   On Windows:
   ```bash
   .\radare2.exe crackme.exe
   ```

2. Use the help system by appending `?` to commands for guidance.

3. Analyze the binary with:
   ```bash
   aaa
   ```

4. Print all functions found:
   ```bash
   afl
   ```

5. Seek to the main function:
   ```bash
   s main
   ```

6. Print the disassembly of the main function:
   ```bash
   pdf
   ```

#### Understanding the Binary
The disassembly will show function calls to `printf` and `scanf`, indicating user interaction. The critical instruction for cracking is the `jne` (Jump Not Equal) at address `0x000011e3`. To bypass the password check, change `jne` to `je` (Jump Equal).

#### Modifying the Binary
1. Make the binary writable:
   ```bash
   oo+
   ```

2. Seek to the instruction:
   ```bash
   s 0x000011e3
   ```

3. Modify the instruction:
   ```bash
   wa je 0x11f6
   ```

4. Verify the change using the graph view:
   ```bash
   VV
   ```

5. Exit Radare2:
   ```bash
   q
   ```

#### Checking Results
Run the modified binary. Enter any password to see "Access granted," indicating successful cracking.

#### Conclusion
This overview provides a glimpse into Radare2's capabilities. For a deeper understanding, further exploration of Radare2 and binary exploitation is encouraged. Happy hacking!

---

## Tags
- **bash** (1 post)
- **linux** (2 posts)
- **pipes** (1 post)
- **radare2** (1 post)
- **reverse engineering** (1 post)

---

## About Me
Hello, World!
```

```markdown
# EG-Zine - My Website

## Blog Posts

### Using radare2 for Simple Binary Analysis
*Date: 2021-07-13*  
*Tags: #reverse engineering, #radare2, #linux*

---

### Bash - Input/Output Redirections and Pipes
*Date: 2020-10-07*  
*Tags: #bash, #pipes, #linux*

---

## Tags Overview
- **#reverse engineering** (1 post)
- **#radare2** (1 post)
- **#linux** (2 posts)
- **#bash** (1 post)
- **#pipes** (1 post)

---
```

```markdown
# EG-Zine - My Website

## Blog Post: Bash - Input/Output Redirections and Pipes
*Date: 2020-10-07*  
*Tags: #bash, #pipes, #linux*

### Overview of Bash
Bash (Bourne Again Shell) was created by Brian Fox and volunteers from the GNU project as an open-source alternative to the older "sh" shell. First released in 1989, Bash has become the de facto standard for shell environments in Linux terminals. Its popularity stems from its ease of use and powerful scripting capabilities, making it the default shell in most Linux distributions.

### What is a Shell?
A shell is a command interpreter that reads user input from a terminal, processes it, communicates with the operating system to execute commands, and returns output to the terminal. It uses three main streams:
- **Standard Input (stdin)**: File descriptor 0 (e.g., keyboard input).
- **Standard Output (stdout)**: File descriptor 1 (output displayed in the terminal).
- **Standard Error (stderr)**: File descriptor 2 (used for error messages).

### How the Command Line Works
When a command is entered in the terminal, such as:
```bash
echo "Hello, World!"
```
Bash processes this input, executes the `echo` command, and returns the output to the terminal based on the command's return value.

### Bash Pipes
Pipes in Bash, represented by the `|` character, redirect output from one command to the input of another. For example:
```bash
ls -lah | grep asdf.py
```
This command lists files in detail and filters the output to show only lines containing "asdf.py".

You can also chain multiple pipes:
```bash
ls -lah | grep asdf.py | awk '{print $1}'
```

### Bash Input/Output Redirections
Redirections are represented by `<` and `>` characters, allowing you to redirect output to a file or input from a file.

**Examples:**
1. Redirecting output to a file:
   ```bash
   ls > files.txt
   ```
   This command saves the list of files to `files.txt`.

2. Appending output to an existing file:
   ```bash
   ls -lah >> files.txt
   ```

3. Redirecting standard error to `/dev/null`:
   ```bash
   find / -name usr 2>/dev/null
   ```
   This command suppresses error messages by redirecting them to a special file that discards the output.

4. Redirecting input from a file:
   ```bash
   grep word < file.txt
   ```

5. Combining input and output redirections:
   ```bash
   grep word < file.txt > result.txt
   ```

### Conclusion
You now have a foundational understanding of Bash, command line operations, pipes, and input/output redirections. While this guide covers essential concepts, there is much more to explore in the world of Bash scripting and command line usage. Thank you for reading, and don't forget to check out my other posts!

---

## Related Posts
- [Using radare2 for Simple Binary Analysis](#)
```

```markdown
# EG-Zine - My Website

## Blog Post: Bash - Input/Output Redirections and Pipes
*Date: 2020-10-07*  
*Tags: #bash, #pipes, #linux*

---

### Overview
This post covers the concepts of input/output redirections and pipes in Bash, a widely used shell in Linux environments.

### Key Concepts
- **Bash**: An open-source shell and scripting language that serves as the default command interpreter in many Linux distributions.
- **Pipes**: A method to redirect the output of one command to the input of another, allowing for powerful command chaining.

---

## Tags Overview
- **#bash** (1 post)
- **#pipes** (1 post)
- **#linux** (1 post)

---
```