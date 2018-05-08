# Javascript 문법 복습

```
var car; // undefined
car = undefined // undefined
car = "" // empty
car = null // null
```

### null의 자료형은 object 이다.

```
typeof undefined // undefined
typeof null // object

```
```
null === undefined // false
null == undefined // true
```
즉 undefined와 자료형이 다르다.

### function의 자료형은 function 이다.
```
typeof function myFunc() {} // function
```

## string

```
var str = "Please locate where 'locate' occurs!";
var pos = str.indexOf("locate"); // 7
var pos2 = str.lastIndexOf("locate") // 21
```

