package exception;

public class NotFoundException extends Exception {
    public NotFoundException(String s) {
        super(s + " not found");
    }
}
