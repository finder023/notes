# STL NOTES

## Iterator

迭代器可以认为是一种智能指针，比较重要的环节是重载两个运算符，*和->

### 偏特化

如果class template拥有一个以上的参数，那么可以针对其中数个参数做特化，也就是说，可以在泛化设计中提供特化版本，偏特化不一定是对某个参数制定特定值，其实是提供另一份template定义式。如下：

```c++
// 泛化版本，可以接受任何类型
template <class T>
class C { };
// 特化版本，只接受指针类型
template <class T>
class C<T*> { }
```

### Iterator_traits

```C++
template <class T>
struct iterator_traits {
    typedef typename T::iterator_category   iterator_category;
    typedef typename T::value_type          value_type;
    typedef typename T::difference_type     difference_type;
    /* ... */
}
// 特化版本
template <class T>
struct iterator_traits<T*> {
    typedef T value_type;
}

template <class T>
struct iterator_traits<const T*> {
    typedef T value_type;
}
```

以上便是stl迭代器类型萃取的机制，可以接受各种class的迭代器类型，亦可以接受原生指针，这就要求迭代器的类必须包含萃取机中的类型，其实iterator的base类定义是这样的：
```c++
template <class Category, class T, class Distance = ptrdiff_t, 
            class Pointer = T*, class Reference = T&>
struct iterator {
    typedef Category    iterator_category;
    typedef T           value_type;
    typedef Distance    difference_type;
    typedef Pointer     pointer;
    typedef Reference   reference;
}
```

每种不同的迭代器都需要继承这个基类，才能使iterator_traits正常工作。

#### Iterator_category

iterator_category有5种迭代器类型，主要是为了针对不通的类型，在算法中调用最高效的方法考虑的，定义如下：

```c++
struct input_iterator_tag {};
struct output_iterator_tag {};
struct forward_iterator_tag : public input_iterator_tag {};
struct bidirectional_iterator_tag : public forward_iterator_tag {};
struct random_acess_iterator_tag : public bidirectional_iterator_tag {};

template <class T>
inline typename iterator_traits<T>::iterator_category
iterator_category(const I&) {
    typedef typename iterator_traits<I>::iterator_category category;
    return category();
}

// advance 的例子
template <class InputIterator, class Distance>
inline void __advance(InputIterator& i, Distance n, input_iterator_tag) {
    while (n--) ++i;
}

template <class ForwardIterator, class Distance>
inline void __advance(ForwardIterator& i, Distance n, forward_iterator_tag) {
    __advance(i, n, input_iterator_tag());
}

template <class BidirectionalIterator, class Distance>
inline void __advance(BidirectionalIterator& i, Distance n, bidirect_iterator_tag) {
    if (n >= 0)
        while (n--) ++i;
    else
        while (n++) --i;
}

template <class RandomAccessIterator, class Distance>
inline void __advance(RandomAccessIterator& i, Distance n, random_access_iterator_tag) {
    i += n;
}

template <class InputIterator, class Distance>
inline void advance(InputIterator& i, Distance n, input_iterator_tag) {
    __advance(i, n, iterator_traits<InputIterator>::iterator_category());
}
```

通过迭代器的iterator_traits可以从迭代器中萃取到原本的数据类型，以及让算法使用适当的方法（在编译阶段就能确认）。

### __type_traits

type_traits不同于iterator_traits，它通过特化的设定，可以萃取数据类型的特性：指的是这个类型是否具备`non-trivial default ctor, non-trivial copy ctor, non-trivial assignment opetator, non-tirvial dtor`，如果这些构造或者析构函数是不重要的，那么就无需在复制，拷贝中调用构造函数，可以直接采用内存操作，malloc, memcpy等。

```c++

struct __true_type {};
struct __false_type {};

template <class type>
struct __type_traits {
    typedef __true_type this_dummy_member_must_be_first;
    
    typedef __false_type    has_trivial_default_constructor;
    typedef __false_type    has_trivial_copy_constructor;
    typedef __false_type    has_trivial_assignment_operator;
    typedef __false_type    has_trivial_destructor;
    typedef __false_type    is_POD_type; // Plain Old Data, C struct or original data type
};

// 默认的这些构造函数都是有用的，都需要去调用，可以对不同类型进行特化
template <>
struct __type_traits<char> {
    typedef __true_type    has_trivial_default_constructor;
    typedef __true_type    has_trivial_copy_constructor;
    typedef __true_type    has_trivial_assignment_operator;
    typedef __true_type    has_trivial_destructor;
    typedef __true_type    is_POD_type;
};

template <>
struct __type_traits<MyType> {
    typedef __true_type     has_trivial_default_constructor;
    typedef __false_type    has_trivial_copy_constructor;
    typedef __false_type    has_trivial_assignment_operator;
    typedef __false_type    has_trivial_destructor;
    typedef __false_type    is_POD_type;
};

// 以copy函数为例

template <class T>
inline void copy(T* source, T* dst, int n) {
    copy(source, dst, n, 
        typename __type_traits<T>::has_trivial_copy_constructor());
}

template <class T>
inline void copy(T* source, T* dst, int n, __false_type) {
    /* ... */
}

template <class T>
inline void copy(T* source, T* dst, int n, __true_type) {
    /* ... */
}
```

### 偏特化其他用途

对于一个模板参数，如果我们不希望其设定成某个值，则在编译阶段就报错，而不是到运行时，可以对这个参数进行一个特化操作：

```c++
template <class T, int size>
class obj { /*...*/ };

template <class T>
class obj<T, 0> {
private:
    obj() {}
    obj(const obj&) {}
    obj& operator=(const obj&) {}
}
```

将default constructor, copy constructor, assignment constructor全部设为private，就无法创建参数为2的obj，其实也不用设为private，因为特化的obj是一个空类，创建后调用其方法或者成员时就会出错。再进一步，`只要将器默认构造函数设为private即可`，因为参数不同，编译时就是两个类，无法进行copy或者assignment。