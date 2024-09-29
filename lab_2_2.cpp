#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <random>
#include <sstream>

// Шаблонний клас для роботи з даними різних типів
template <typename T>
class DataStructure {
private:
    std::vector<T> data;
    
public:
    // Метод для додавання елемента
    void add(const T& value) {
        data.push_back(value);
    }
    
    // Метод для отримання текстового подання
    std::string toString() const {
        std::stringstream ss;
        for (const auto& item : data) {
            ss << item << " ";
        }
        return ss.str();
    }
    
    // Метод для генерації випадкових даних (для чисел)
    void generateRandomData(int size) {
        std::default_random_engine generator;
        std::uniform_int_distribution<int> distribution(0, 100);
        for (int i = 0; i < size; ++i) {
            data.push_back(static_cast<T>(distribution(generator)));
        }
    }
    
    // Метод для запису даних у файл
    void writeToFile(const std::string& filename) const {
        std::ofstream file(filename);
        if (file.is_open()) {
            for (const auto& item : data) {
                file << item << " ";
            }
            file.close();
        }
    }
    
    // Метод для зчитування даних з файлу
    void readFromFile(const std::string& filename) {
        std::ifstream file(filename);
        T value;
        if (file.is_open()) {
            while (file >> value) {
                data.push_back(value);
            }
            file.close();
        }
    }
};

// Спеціалізація шаблонного класу для роботи з рядками
template <>
void DataStructure<std::string>::generateRandomData(int size) {
    for (int i = 0; i < size; ++i) {
        data.push_back("RandomString" + std::to_string(i));
    }
}

// Демонстрація роботи з різними типами
int main() {
    // Примітивні типи
    DataStructure<int> intStructure;
    intStructure.generateRandomData(5);
    std::cout << "Integer Structure: " << intStructure.toString() << std::endl;
    intStructure.writeToFile("integers.txt");
    
    DataStructure<double> doubleStructure;
    doubleStructure.generateRandomData(5);
    std::cout << "Double Structure: " << doubleStructure.toString() << std::endl;
    doubleStructure.writeToFile("doubles.txt");
    
    // Бібліотечні типи
    DataStructure<std::string> stringStructure;
    stringStructure.generateRandomData(3);
    std::cout << "String Structure: " << stringStructure.toString() << std::endl;
    stringStructure.writeToFile("strings.txt");

    return 0;
}

class Document {
private:
    std::string titlePage;
    std::vector<std::string> sections;
    std::vector<std::string> lists;
    std::vector<std::string> images;
    std::string tableOfContents;
    
public:
    void setTitlePage(const std::string& title) {
        titlePage = title;
    }
    
    void addSection(const std::string& section) {
        sections.push_back(section);
    }
    
    void addList(const std::string& list) {
        lists.push_back(list);
    }
    
    void addImage(const std::string& image) {
        images.push_back(image);
    }
    
    std::string toString() const {
        std::stringstream ss;
        ss << "Title Page: " << titlePage << "\n";
        ss << "Table of Contents: " << tableOfContents << "\n";
        for (const auto& section : sections) {
            ss << "Section: " << section << "\n";
        }
        for (const auto& list : lists) {
            ss << "List: " << list << "\n";
        }
        for (const auto& image : images) {
            ss << "Image: " << image << "\n";
        }
        return ss.str();
    }
    
    void setTableOfContents(const std::string& toc) {
        tableOfContents = toc;
    }
    
    void writeToFile(const std::string& filename) const {
        std::ofstream file(filename);
        if (file.is_open()) {
            file << toString();
            file.close();
        }
    }
    
    void readFromFile(const std::string& filename) {
        std::ifstream file(filename);
        std::string line;
        if (file.is_open()) {
            while (std::getline(file, line)) {
                // Обробка файлу для заповнення документа
                // (можна додати логіку для парсингу окремих компонентів)
                std::cout << line << std::endl;
            }
            file.close();
        }
    }
};

// Демонстрація роботи з документами
int main() {
    Document doc;
    doc.setTitlePage("Title: Object-Oriented Programming");
    doc.addSection("Introduction to OOP");
    doc.addList("List: C++ features");
    doc.addImage("Image: Diagram.jpg");
    doc.setTableOfContents("Table of Contents: 1. Intro, 2. Classes, 3. Inheritance");
    
    std::cout << doc.toString();
    doc.writeToFile("document.txt");
    
    return 0;
}

void Document::validate() const {
    if (titlePage.empty()) {
        std::cout << "Error: No title page.\n";
    }
    if (tableOfContents.empty()) {
        std::cout << "Error: No table of contents.\n";
    }
    if (sections.empty()) {
        std::cout << "Error: No sections in document.\n";
    }
}
