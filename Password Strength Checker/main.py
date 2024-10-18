from model.model import predict   # import model

def main():
    password_to_test = input("Enter a password to check its strength: ")   # get password from terminal
    predicted_class = int(predict(password_to_test))   # evaluate password strength
    print(f"Password strength classification: {predicted_class} / 2")   # output 0 - weak, 1 - moderate, or 2 - strong

if __name__ == "__main__":  main()