#include <windows.h>
#include <direct.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <conio.h>
#include <vector>
#include <string>
#include <tuple>
#include <map>

using namespace std;

pair<bool, long double> float_from_string(string s) {
    bool has_point = 0;
    for (int i = 0; i < s.size(); i++) {
        if (!((s[i] >= '0' && s[i] <= '9') || s[i] == '-' || s[i] == '.' || s[i] == ',')) return { 0, 0 };
        else {
            if (s[i] == '-' && i != 0) return { 0, 0 };
            if (s[i] == '.' || s[i] == ',') {
                if (has_point) return { 0, 0 };
                else {
                    has_point = 1;
                    if (i == 0) {
                        s.insert(0, 1, '0');
                        i++;
                    }
                    else if (i == s.size() - 1) {
                        s.pop_back();
                        has_point = 0;
                    }
                    if (s[i] == ',') s[i] = '.';
                }
            }
        }
    }
    return { 1, stof(s) };
}

vector<vector<long double>> read_matrix(string file_path) {
    vector<vector<long double>> matrix;
    ifstream f(file_path);
    if (!f.is_open()) {
        f.close();
        ofstream newfile(file_path, fstream::app);
        newfile.close();
        ifstream check(file_path);
        if (!check.is_open()) {
            check.close();
            cout << "\033[31m" "[ОШИБКА] Отказано в доступе к файлу \'" << file_path << "\'.\n" "\033[30m";
            cout << "\n\nНажмите любую клавишу, чтобы выйти.";
            _getch();
            return {};
        }
        check.close();
        cout << "\033[32m" "Файл \'" << file_path << "\' создан.\nПожалуйста, заполните его матрицей, затем снова запустите программу.\n" "\033[30m";
        cout << "\n\nНажмите любую клавишу, чтобы выйти.";
        _getch();
        return {};
    }

    int size = 0, row = 0;
    string line, entry;
    stringstream line_stream;

    while (getline(f, line)) {
        row++;
        matrix.push_back({});

        line_stream.clear();
        line_stream.str(line);

        while (line_stream >> entry) {
            auto temp = float_from_string(entry);
            if (!temp.first) {
                cout << "\033[31m" "[ОШИБКА] Не удалось прочитать число \'" << entry << "\' из " << row << "-й строки.\n";
                cout << "Пожалуйста, проверьте вашу матрицу ещё раз.\n" "\033[30m";
                cout << "\n\nНажмите любую клавишу, чтобы выйти.";
                _getch();
                return {};
            }
            else matrix[row - 1].push_back(temp.second);
        }
        if (size == 0) size = matrix[0].size();
        if (matrix[row - 1].size() != size) {
            cout << "\033[31m" "[ОШИБКА] Количество чисел в " << row << "-й строке не совпадает с предыдущими.\n";
            cout << "Пожалуйста, проверьте вашу матрицу ещё раз.\n" "\033[30m";
            cout << "\n\nНажмите любую клавишу, чтобы выйти.";
            _getch();
            return {};
        }
    }

    if (size == 0) {
        cout << "\033[31m" "[ОШИБКА] Файл \'" << file_path << "\' пуст.\n" "\033[30m";
        cout << "\n\nНажмите любую клавишу, чтобы выйти.";
        _getch();
        return {};
    }

    if (row != size) {
        cout << "\033[31m" "[ОШИБКА] Определитель можно вычислить только для квадратной матрицы. Размерность вашей матрицы: " << row << "x" << size << ".\n";
        cout << "Пожалуйста, проверьте вашу матрицу ещё раз.\n" "\033[30m";
        cout << "\n\nНажмите любую клавишу, чтобы выйти.";
        _getch();
        return {};
    }

    return matrix;
}

void print_matrix(vector<vector<long double>> matrix) {
    size_t size = matrix.size();

    size_t max_number_length = 0;
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            stringstream temp;
            temp << matrix[i][j];
            size_t this_length = temp.str().size();
            if (this_length > max_number_length) max_number_length = this_length;
        }
    }

    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            cout.width(max_number_length);
            cout << matrix[i][j];
            cout << "  ";
        }
        cout << "\n";
    }
}

vector<vector<long double>> submatrix(vector<vector<long double>> matrix, int del_row, int del_col) {
    size_t new_size = matrix.size() - 1;
    vector<vector<long double>> new_matrix(new_size, vector<long double>(new_size));
    int i = 0, j = 0;
    for (int row = 1; row <= matrix.size(); row++) {
        if (row != del_row) {
            for (int col = 1; col <= matrix.size(); col++) {
                if (col != del_col) {
                    new_matrix[i][j] = matrix[row - 1][col - 1];
                    j++;
                }
            }
            i++;
            j = 0;
        }
    }
    return new_matrix;
}

long double determinant(vector<vector<long double>> matrix, int column) {
    static map<tuple<vector<vector<long double>>, int, int>, long double> cache;

    if (matrix.empty()) return 0;
    if (matrix.size() == 1) return matrix[0][0];

    long double det = 0;
    int size = matrix.size(), sign;
    if (size < column) column = 1;
    for (int row = 1; row <= size; row++) {
        if (matrix[row - 1][column - 1] != 0) {
            if ((row + column) % 2 == 0) sign = 1;
            else sign = -1;

            long double submatr_det;
            auto cache_iter = cache.find({ matrix, row, column });
            if (cache_iter != cache.end()) {
                submatr_det = cache_iter->second;
            }
            else {
                submatr_det = determinant(submatrix(matrix, row, column), column);
                cache[{ matrix, row, column }] = submatr_det;
            }

            det += sign * matrix[row - 1][column - 1] * submatr_det;
        }
    }
    return det;
}

int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    system("color F0");
    
    vector<vector<long double>> matrix;
    string filename = "matrix.txt";
    string cwd = _getcwd(NULL, 0);
    matrix = read_matrix(cwd + "\\" + filename);
    if (matrix.empty()) return 0;

    cout << "Ваша матрица:\n\n";
    print_matrix(matrix);

    cout << "\n";
    cout << "Сейчас я вычислю определитель этой матрицы. Для начала задайте номер столбца,\n";
    cout << "по которому будет выполняться разложение. Если ничего не введено, введён\n";
    cout << "посторонний символ или число вне допустимого диапазона, то разложение матрицы\n";
    cout << "будет производиться по первому столбцу. При разложении матрицы с меньшим размером,\n";
    cout << "чем введённое число, разложение будет также производиться по первому столбцу.\n";
    cout << "\n";
    cout << "Итак, введите номер столбца ниже:\n";
    cout << ">> ";
    unsigned int column;
    cin >> column;
    if (column < 1 || column > matrix.size()) column = 1;
    cout << "\n";

    cout << "Идёт подсчёт...";
    long double det = determinant(matrix, column);
    cout << "\rОпределитель данной матрицы равен " << det << "\n";

    cout << "\n\nНажмите любую клавишу, чтобы выйти.";
    _getch();
}