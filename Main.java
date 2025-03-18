
interface IArithmeticsAdd {
    double add(double a, double b);
}

interface IArithmeticsMult{
    double Multiplication(double A, double B);
}

interface IArithmeticsDiff{
    double Difference(double A, double B);
}

interface IArithmeticDiv{
    double division(double a,double b);
}

public class Main implements IArithmeticDiv,IArithmeticsDiff,IArithmeticsMult,IArithmeticsAdd{

    public static  void main(String[] args){
        System.out.println("CodeBlack\n Tester/Scrum Master\n albertbrozyna12\nDeveloper\nDanielSzymczak\nDevOps\n kuba122388\nDeveloper\n SzkopikRafal\n");
    }

    //Dodawanie
    public double add(double a, double b) {
        return a + b;
    }

    public double Difference(double A, double B){
        return A-B;
    }

    public double division(double a,double b){
        if(b == 0){
            return 0;
        }
        return a/b;
    }
    
     public double Multiplication(double A, double B) {
        return A * B;
    }

}
