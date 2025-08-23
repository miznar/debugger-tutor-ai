EXAMPLES = {
    "python": """def add_numbers(a, b)
    return a + c

result = add_numbers(5, 10
print("Result is:", result)""",
    "javascript": """function sum(a, b) {
  return a + c
}

const result = sum(2, 3;
console.log("Result:", result);""",
    "cpp": """#include <iostream>
int main() {
    int a = 5
    int b = 10;
    int s = a + c;
    std::cout << "Sum: " << s << std::endl;
    return 0;
}""",
    "java": """public class Buggy {
    public static void main(String[] args) {
        int a = 5
        int b = 10;
        int s = a + c;
        System.out.println("Sum: " + s);
    }
}""",
}
