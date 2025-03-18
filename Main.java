
interface IArithmeticDiv{
    double division(double a,double b);
}

public class Main implements IArithmeticDiv{
    public static  void main(String[] args){
        System.out.println("CodeBlack\n Tester/Scrum Master\n albertbrozyna12\nDeveloper\nDanielSzymczak\nDevOps\n kuba122388\nDeveloper\n SzkopikRafal\n");


    }

    public double division(double a,double b){
        if(b == 0){
            return 0;
        }
        return a/b;
    }
}

