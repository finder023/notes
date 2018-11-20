# arrayInit demo

## 生成java或者Python的代码

运行命令 antlr4 arrayInit.g4即可，默认生成java代码，指定生成python加一行参数 `-Dlanguage=Python3`

对于例子{11,22,33}

> {11,22,33}
> 
> [@0,0:0='{',<1>,1:0]
>
> [@1,1:2='11',<4>,1:1]
> 
> [@2,3:3=',',<2>,1:3]
> 
> [@3,4:5='22',<4>,1:4]
> 
> [@4,6:6=',',<2>,1:6]
> 
> [@5,7:8='33',<4>,1:7]
>
> [@6,9:9='}',<3>,1:9]
>
> [@7,11:10='<EOF>',<-1>,2:0]

对于这个tokens的理解，以第三行为例，分别代表第三个语法单元，字符区间是3:3，类型为2，位于第一行第三个字符

这样，可以写一段代码将生成的文件集成，来模拟命令行的运行

贴上python的代码：
### test.py
```python
#!/usr/bin/env python3

import sys
from antlr4 import *
from ArrayInitLexer import ArrayInitLexer
from ArrayInitParser import ArrayInitParser
from rewriter import RewriteListener

def main(argv):
    istream = FileStream(argv[1])
    lexer = ArrayInitLexer(istream)
    stream = CommonTokenStream(lexer)
    parser = ArrayInitParser(stream)
    tree = parser.init()
    print(tree.toStringTree(recog=parser))

    walker = ParseTreeWalker()
    walker.walk(RewriteListener(), tree)
    print()

if __name__ == '__main__':
    main(sys.argv)
```

### rewriter.py

```python
from ArrayInitListener import ArrayInitListener

class RewriteListener(ArrayInitListener):
    # Enter a parse tree produced by ArrayInitParser#init.
    def enterInit(self, ctx):
        print("\"", end='')

    # Exit a parse tree produced by ArrayInitParser#init.
    def exitInit(self, ctx):
        print("\"", end='')

    # Enter a parse tree produced by ArrayInitParser#value.
    def enterValue(self, ctx):
        pass

    # Exit a parse tree produced by ArrayInitParser#value.
    def exitValue(self, ctx):
        data = ctx.INT().getText()
        print('\\u%04x' % int(data), end='')
```

这里使用的事Listener方法对语法书进行遍历，antlr提供了一个默认的listener的类，这个类只提供接口，要操纵数据需要继承这个默认的类，然后重载。这样对于代码转化来说，只要重载相应的规则函数，设定转换规则，就可以达到代码转换的目的。上述rewriter时对初始化数组和字符串进行的转换。