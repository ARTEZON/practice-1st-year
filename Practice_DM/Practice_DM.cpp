#include <windows.h>
#include <direct.h>
#include <iostream>
#include <fstream>
#include <conio.h>
#include <string>
#include <vector>

using namespace std;

bool is_pow_2(int n) {
    return (n > 0 && ((n & (n - 1)) == 0));
}

unsigned int log_2(unsigned int n) {
    int log = 0;
    while (n >= 2) {
        log++;
        n /= 2;
    }
    return log;
}

vector<string> read_file(string path) {
    vector<string> func_list;
    ifstream f(path);
    if (!f.is_open()) {
        f.close();
        ofstream newfile(path, fstream::app);
        newfile.close();
        ifstream check(path);
        if (!check.is_open()) {
            check.close();
            cout << "\033[31m" "[ОШИБКА] Отказано в доступе к файлу \'" << path << "\'.\n" "\033[30m";
            cout << "\n\nНажмите любую клавишу, чтобы выйти.";
            _getch();
            return {};
        }
        check.close();
        cout << "\033[32m" "Файл \'" << path << "\' создан.\n"
            "Пожалуйста, заполните его списком ДДФ в векторной форме (по одной функции на строку).\n"
            "Затем снова запустите программу.\n" "\033[30m";
        cout << "\n\nНажмите любую клавишу, чтобы выйти.";
        _getch();
        return {};
    }

    int count = 0;
    string func;
    while (getline(f, func)) {
        if (!func.empty()) {
            count++;
            for (char ch : func) {
                if (ch != '0' && ch != '1') {
                    cout << "\033[31m" "[ОШИБКА] В " << count << "-й строке найден недопустимый символ: \'" << ch << "\'\n";
                    cout << "ДДФ в векторной форме может содержать только нули и единицы.\n" "\033[30m";
                    cout << "\n\nНажмите любую клавишу, чтобы выйти.";
                    _getch();
                    return {};
                }
            }
            if (!is_pow_2(func.size())) {
                cout << "\033[31m" "[ОШИБКА] Длина вектор функции в " << count << "-й строке равна " << func.size() << ", а должна быть равна 2^n.\n" "\033[30m";
                cout << "\n\nНажмите любую клавишу, чтобы выйти.";
                _getch();
                return {};
            }
            func_list.push_back(func);
        }
    }
    if (count == 0) {
        cout << "\033[31m" "[ОШИБКА] Файл \'" << path << "\' пуст.\n" "\033[30m";
        cout << "\n\nНажмите любую клавишу, чтобы выйти.";
        _getch();
        return {};
    }
    f.close();
    return func_list;
}

string bin(int n, unsigned int len) {
    string b;
    while (n) {
        b.insert(0, to_string(n & 1));
        n >>= 1;
    }
    int fill_zeros = len - b.size();
    if (fill_zeros > 0) b.insert(0, fill_zeros, '0');
    return b;
}

vector<string> triangle(string func) {
    vector<string> trngl;
    trngl.push_back(func);
    string new_layer;
    while (func.size() > 1) {
        for (int ch = 0; ch < func.size() - 1; ch++) {
            bool a = bool(func[ch] - '0');
            bool b = bool(func[ch + 1] - '0');
            if (a != b) new_layer.push_back('1');
            else new_layer.push_back('0');
        }
        func = new_layer;
        trngl.push_back(func);
        new_layer.clear();
    }
    return trngl;
}

string anf(string func) {
    vector<string> trngl = triangle(func);
    string anf_str;
    unsigned int var_count = log_2(trngl[0].size());
    for (int i = 0; i < trngl.size(); i++) {
        bool left_number = bool(trngl[i][0] - '0');
        string truth_table_row = bin(i, var_count);
        if (left_number) {
            anf_str += " + ";
            if (i == 0) anf_str += "1";
            else {
                for (int j = 0; j < var_count; j++) {
                    if (truth_table_row[j] == '1') anf_str += "x" + to_string(j + 1);
                }
            }
        }
    }
    anf_str.erase(0, 3);
    if (anf_str.empty()) anf_str = "не существует";
    return anf_str;
}

int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    system("color F0");

    string filename_in = "input.txt";
    string filename_out = "output.txt";
    string cwd = _getcwd(NULL, 0);

    vector<string> func_list = read_file(cwd + "\\" + filename_in);
    if (func_list.empty()) return 0;

    ofstream out(cwd + "\\" + filename_out);

    string polynomial;
    unsigned int n = 0;
    for (auto it = func_list.begin(); it != func_list.end(); it++) {
        n++;
        polynomial = anf(*it);
        cout << "Функция " << n << ":\n\tВведённый вектор:\t" << *it << "\n\tПолином Жегалкина:\t" << polynomial << "\n\n";
        if (out.is_open()) {
            if (n != 1) out << '\n';
            out << polynomial;
        }
    }
    if (out.is_open()) cout << "\033[32m" "Результат(ы) записан(ы) в файл \'" << cwd + "\\" + filename_out << "\'.\n" "\033[30m";
    else cout << "\033[31m" "[ОШИБКА] Не удалось открыть файл \'" << cwd + "\\" + filename_out << "\' для записи.\n" "\033[30m";
    out.close();

    cout << "\n\nНажмите любую клавишу, чтобы выйти.";
    _getch();
}