template<typename T>
class List {
public:
    virtual ~List() = default;
    virtual void add(const T& value) = 0;
    virtual bool remove(const T& value) = 0;
    virtual T get(int index) const = 0;
    virtual int findByValue(const T& value) const = 0;
    virtual int size() const = 0;
    virtual std::string toString() const = 0;
    virtual void saveToFile(const std::string& filename) const = 0;
    virtual void loadFromFile(const std::string& filename) = 0;
};

template<typename T>
class SinglyLinkedList : public List<T> {
private:
    struct Node {
        T data;
        Node* next;
        Node(const T& value) : data(value), next(nullptr) {}
    };
    Node* head;
    int listSize;

public:
    SinglyLinkedList() : head(nullptr), listSize(0) {}

    ~SinglyLinkedList() override {
        clear();
    }

    void add(const T& value) override {
        Node* newNode = new Node(value);
        if (!head) {
            head = newNode;
        } else {
            Node* temp = head;
            while (temp->next) {
                temp = temp->next;
            }
            temp->next = newNode;
        }
        listSize++;
    }

    bool remove(const T& value) override {
        if (!head) return false;
        if (head->data == value) {
            Node* temp = head;
            head = head->next;
            delete temp;
            listSize--;
            return true;
        }
        Node* temp = head;
        while (temp->next && temp->next->data != value) {
            temp = temp->next;
        }
        if (temp->next) {
            Node* toDelete = temp->next;
            temp->next = temp->next->next;
            delete toDelete;
            listSize--;
            return true;
        }
        return false;
    }

    T get(int index) const override {
        if (index < 0 || index >= listSize) throw std::out_of_range("Index out of range");
        Node* temp = head;
        for (int i = 0; i < index; ++i) {
            temp = temp->next;
        }
        return temp->data;
    }

    int findByValue(const T& value) const override {
        Node* temp = head;
        int index = 0;
        while (temp) {
            if (temp->data == value) return index;
            temp = temp->next;
            index++;
        }
        return -1;  // Not found
    }

    int size() const override {
        return listSize;
    }

    std::string toString() const override {
        std::ostringstream oss;
        Node* temp = head;
        while (temp) {
            oss << temp->data << " -> ";
            temp = temp->next;
        }
        oss << "nullptr";
        return oss.str();
    }

    void saveToFile(const std::string& filename) const override {
        std::ofstream file(filename);
        Node* temp = head;
        while (temp) {
            file << temp->data << "\n";
            temp = temp->next;
        }
    }

    void loadFromFile(const std::string& filename) override {
        clear();
        std::ifstream file(filename);
        T value;
        while (file >> value) {
            add(value);
        }
    }

    void clear() {
        Node* temp = head;
        while (temp) {
            Node* next = temp->next;
            delete temp;
            temp = next;
        }
        head = nullptr;
        listSize = 0;
    }
};

int main() {
    SinglyLinkedList<int> intList;
    intList.add(1);
    intList.add(2);
    intList.add(3);

    std::cout << "Integer list: " << intList.toString() << std::endl;

    SinglyLinkedList<std::string> stringList;
    stringList.add("Hello");
    stringList.add("World");

    std::cout << "String list: " << stringList.toString() << std::endl;

    intList.saveToFile("int_list.txt");
    SinglyLinkedList<int> loadedIntList;
    loadedIntList.loadFromFile("int_list.txt");
    std::cout << "Loaded integer list from file: " << loadedIntList.toString() << std::endl;

    return 0;
}
