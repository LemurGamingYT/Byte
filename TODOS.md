# TODOS
What needs to be done soon/next

- [ ] including local files
- [ ] first-class functions
- [ ] mutable and public class fields
- [ ] move `error` to `builtins.byte`
- [ ] mangle function and class names based on the file name they come from (e.g. `builtins::string.new`)
- [ ] static classes (and use them on `Math` and `System`)
- [ ] `Random` class
- [ ] generics inside classes
- [ ] static arrays
- [ ] immutable arrays
- [ ] make sure all forward declarations work
  - *currently, doing a method extension does not work with forward declarations*
- [ ] `fstream` library
- [ ] clean up AST
  - [x] type extensions have the type extension + the type and then the name in the `.byteast files` (e.g. `string.string.new`)
