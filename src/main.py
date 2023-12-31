from lexer import Lexer


lexer = Lexer(
    """\
let a = 32.2;
fn helloworld() {
    print("nothing.");
    return 0;
}
helloworld();
//helloworld
/*
hello world
/**/
*/
"""
)
for t in lexer.all():
    print(t, end="\t")
