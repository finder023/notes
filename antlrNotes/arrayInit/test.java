import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

public class test {
    public static void main(string[] args) throws Exception {
        ANTLRInputStream input = new ANTLRInputStream(System.in);

        arrayInitLexer lexer = new arrayInitParser(input);

        CommonTokenStream tokens = new CommonTokenStream(lexer);

        arrayInitParser parser = new arrayInitParser(tokens);

        PraseTree tree = parser.init();

        System.out.println(tree.toStringTree(parser));
    }
}