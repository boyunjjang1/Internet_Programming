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

#### 위치찾기
```
var str = "Please locate where 'locate' occurs!";
var pos = str.indexOf("locate"); // 7
var pos2 = str.lastIndexOf("locate") // 21
var pos3 = str.indexOf("locate", 15); // 21, 15번째 이후로 존재하는 locate를 찾는다.
var pos4 = str.search("locate");
```

#### 문자열 분할
1.
```
var str = "Apple,Banana,Kiwi";
var res = str.slice(7,13); // Banana , slice(시작인덱스,끝 인덱스+1)
var res2 = str.slice(-12,-6); //Banana
var res3 = str.slice(7); // Banana,Kiwi //7부터 이후로
var res4 = str.substring(7,13); // Banana
var res5 = str.substr(7,6); // Banana , substr(시작인덱스,길이)
```
2.  split (문자열로 반환함)
```
var str = "a,b|c,d|e,f";
var arr = str.split(","); // ["a","b|c","d|e","f"];
var arr2 = str.split("|"); // ["a,b","c,d","e,f"];
var arr3 = str.split(""); // ["a,b|c,","d|e,f"]
var arr4 = str.split(""); // ["a",",","b","|","c",",","","d","|","e",",","f"]
```

#### 문자열 전환
```
str = "Please visit Microsoft";
var n = str.replace("Microsoft","W3Schools");
// Please visit W3Schools
```

#### 대소문자
```
var text1 = "Hello World!";
var text2 = text1.toUpperCase(); // HELLO WROLD!
var text3 = text1.toLowerCase(); // hello world!
```

#### 문자열 합치기
1.
```
var text1 = "Hello";
var text2 = "World";
var text3 = text1.concat("",text2); //HelloWorld
```
2.
```
var text1 = "Hello" + "" +"World!";
var text2 = "Hello".concat("","World!");
```

#### 문자열 찾기
```
var str = "HELLO WORLD";
str.charAt(0); // H
str.charCodeAt(0); // 72
str[0] // 첫번째 인덱스를 찾는다.
```


## Number
1.
```
var x = 999999999999999; // 999999999999999
var y = 9999999999999999; // 10000000000000000
var z = 0.2 + 0.1; // 0.30000000000000004
var z2 = (0.2 * 10 + 0.1 * 10)/10; // 0.3
```

2.
```
var x = "1000"; // type == string
var y = "10"
var z = x/y; // type == number
```
```
var x = 100 / "Apple"; // NaN
typeof NaN; // Number , 즉 NaN의 type은 number 이다.
```

3. 숫자 문자열 전환
```
var x = 123;
x.toString(); // "123"
var x2 = 0XFF; // 255
```
```
var myNumber = 128;
myNumber.toString(16);
myNumber.toString(8);
myNumber.toString(2);
```
4.
```
var x = 9.656;
x.toExponential(2); // 9.66e + 0
x.toExponential(4); // 9.6560e + 0
```
```
var x = 9.656;
x.toPrecision(); // 9.656
x.toPrecision(2); // 9.7
x.toPrecision(4); // 9.656
x.toPrecision(6); // 9.65600
```

## Array
1.
```
var fruits = ["Banana","Orange","Apple","Mango"];
fruits.toString(); // Banana,Orange,Apple,Mango
fruits.join("*"); // Banana*Orange*Apple*Mango
fruits.pop(); // 후입선출, "Mango" => ["Banana","Orange","Apple"]
x = fruits.push("Kiwi"); // ["Banana","Orange","Apple","Kiwi"], x = 4; x에는 총 개수가 들어감
fruits.shift(); // 선입선출, "Banana" => ["Orange","Apple","Kiwi"]
x = fruits.unshit("Lemon"); // ["Lemon","Orange","Apple","Kiwi"], x = 4;
fruits[fruits.length] = "Banana"; // 가장 마지막에 값이 들어감, ["Lemon","Orange","Apple","Kiwi","Banana"]
```

2.
```
var fruits = ["Banana","Orange","Apple","Mango"];
fruits.splice(2,0,"Lemon","Kiwi"); // 처음 지울 인덱스, 몇개 지울건지
// Banana,Orange,Lemon,Kiwi,Apple,Mango
fruits.splice(0,1); // Orange,Lemon,Kiwi,Apple,Mango
fruits.slice(1,3); // 자른 부분을 가져옴
// Lemon,Kiwi
```

3.
```
var fruits = ["Banana","Orange","Apple","Mango"];
fruits.sort(); // Apple,Banana,Mango,Orange
fruits.reverse(); // Orange,Mango,Banana,Apple
```

4.
```
var points = [40,100,1,5,25,10];
points.sort(); // 1,10,100,25,40,5 --> 문자열기준 sort
points.sort(function(a,b){return a-b}); // 1,5,10,25,40,100
points.sort(function(a,b){return b-a}); // 100,40,25,10,5,1
points.sort(function(a, b){return 0.5 - Math.random()}); // 25,5,100,10,1,40 (random)
```



