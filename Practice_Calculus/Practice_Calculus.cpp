#include <Windows.h>
#include <iostream>
#include <iomanip>
#include <conio.h>
#include <string>
#include <cmath>

using namespace std;

long double f(long double x, unsigned int func_id) {
    switch (func_id) {
    case  1: return powl(x, 2);
    case  2: return sqrtl(abs(x));
    case  3: return logl(abs(x));
    case  4: return expl(x);
    case  5: return sinl(x);
    case  6: return 2 * x * cosl(x);
    case  7: return 2 * x * x + 3 * x - 1;
    case  8: return (9 * x + 5) / (x - 8);
    case  9: return expl(3 * x) * sinl(x * x);
    case 10: return x / sqrtl(powl(x, 4) + 16);
    default: return 0;
    }
}

long double integral(unsigned int func_id, long double a, long double b, long double h) {
    unsigned long long int n = abs(b - a) / h;
    long double sum = 0;
    int sign = 1;
    if (a > b) {
        swap(a, b);
        sign = -sign;
    }

    for (int i = 1; i <= n; i++) {
        sum += f(a + ((2 * i - 1) * h / 2), func_id);
    }

    return h * sum * sign;
}

string floating_point(long double d) {
    string s = to_string(d);
    while (!s.empty() && *(s.end() - 1) == '0') s.pop_back();
    if (!s.empty() && *(s.end() - 1) == '.') s.pop_back();
    return s;
}

int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    system("color F0");

    int func_id;
    long double a, b, step;

    while (1) {
        system("cls");
        func_id = 0;
        cout << "Добро пожаловать в решатель определённых интегралов методом серединных прямоугольников!\n"
            "Пожалуйста, выберите функцию и введите её номер:\n"
            " 1) x^2\n"
            " 2) sqrt(|x|)\n"
            " 3) ln(|x|)\n"
            " 4) e^x\n"
            " 5) sin(x)\n"
            " 6) 2x * cos(x)\n"
            " 7) 2x^2 + 3x - 1\n"
            " 8) (9x + 5) / (x - 8)\n"
            " 9) e^(3x) * sin(x^2)\n"
            "10) x / sqrt(x^4 + 16)\n";
        while (func_id < 1 || func_id > 10) {
            cout << "\n>> ";
            cin >> func_id;
            cout << "\n";
            if (func_id <= 0) {
                cout << "\033[31m" "Я вас не понимаю. Пожалуйста, введите число от 1 до 10.\n" "\033[30m";
                cin.clear();
                cin.ignore(INT_MAX, '\n');
            }
            if (func_id > 10) {
                cout << "\033[31m" "У меня нет функции под номером " << func_id << ". Пожалуйста, введите число от 1 до 10.\n" "\033[30m";
                cin.clear();
                cin.ignore(INT_MAX, '\n');
            }
        }

        cout << "Хорошо, теперь введите нижний и верхний пределы интегрирования через пробел.\n";
        while (1) {
            cout << "\n>> ";
            cin >> a >> b;
            cout << "\n";
            if (cin.fail()) {
                cout << "\033[31m" "Это не число :(\n" "\033[30m";
                cin.clear();
                cin.ignore(INT_MAX, '\n');
            }
            else break;
        }

        cout << "Отлично. Осталось только ввести шаг интегрирования - ширину прямоугольников. Например, 0.0001\n";
        while (1) {
            cout << "\n>> ";
            cin >> step;
            cout << "\n";
            if (cin.fail()) {
                cout << "\033[31m" "Это не число :(\n" "\033[30m";
                cin.clear();
                cin.ignore(INT_MAX, '\n');
            }
            else break;
        }


        string ascii_image[10];
        ascii_image[0] = R"(    /                      )" "\n"
                         R"(   |  2                    )" "\n"
                         R"(   | x  dx                 )" "\n"
                         R"(   |                       )" "\n"
                         R"(  /                        )" "\n";
        ascii_image[1] = R"(    /                      )" "\n"
                         R"(   |   ___                 )" "\n"
                         R"(   | \/|x| dx              )" "\n"
                         R"(   |                       )" "\n"
                         R"(  /                        )" "\n";
        ascii_image[2] = R"(    /                      )" "\n"
                         R"(   |                       )" "\n"
                         R"(   | ln|x| dx              )" "\n"
                         R"(   |                       )" "\n"
                         R"(  /                        )" "\n";
        ascii_image[3] = R"(    /                      )" "\n"
                         R"(   |  x                    )" "\n"
                         R"(   | e  dx                 )" "\n"
                         R"(   |                       )" "\n"
                         R"(  /                        )" "\n";
        ascii_image[4] = R"(    /                      )" "\n"
                         R"(   |                       )" "\n"
                         R"(   | sinx dx               )" "\n"
                         R"(   |                       )" "\n"
                         R"(  /                        )" "\n";
        ascii_image[5] = R"(    /                      )" "\n"
                         R"(   |                       )" "\n"
                         R"(   | 2 x cosx dx           )" "\n"
                         R"(   |                       )" "\n"
                         R"(  /                        )" "\n";
        ascii_image[6] = R"(    /                      )" "\n"
                         R"(   | /    2           \    )" "\n"
                         R"(   | | 2 x  + 3 x - 1 | dx )" "\n"
                         R"(   | \                /    )" "\n"
                         R"(  /                        )" "\n";
        ascii_image[7] = R"(    /                      )" "\n"
                         R"(   |  9 x + 5              )" "\n"
                         R"(   | --------- dx          )" "\n"
                         R"(   |   x - 8               )" "\n"
                         R"(  /                        )" "\n";
        ascii_image[8] = R"(    /                      )" "\n"
                         R"(   |  3 x      2           )" "\n"
                         R"(   | e    sin x  dx        )" "\n"
                         R"(   |                       )" "\n"
                         R"(  /                        )" "\n";
        ascii_image[9] = R"(    /                      )" "\n"
                         R"(   |       x               )" "\n"
                         R"(   | _____________  dx     )" "\n"
                         R"(   |     _______           )" "\n"
                         R"(   |    / 4                )" "\n"
                         R"(   |  \/ x  + 16           )" "\n"
                         R"(  /                        )" "\n";

        system("cls");
        cout << "\n     " << floating_point(b) << "\n";
        cout << ascii_image[func_id - 1];
        cout << "  " << floating_point(a) << "\n";

        cout << "\nВычисляю интеграл...";

        long double I = integral(func_id, a, b, step);
        string I_str = floating_point(I);

        cout << "\rИнтеграл приблизительно равен " << fixed << setprecision(numeric_limits<double>::max_digits10) << I_str << endl;

        cout << "\n\nНажмите любую клавишу, чтобы вернуться в главное меню.";
        _getch();
    }
}