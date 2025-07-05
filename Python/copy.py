# print("hello world")

# print(3+4)
# print(3-4)
# print(3*4)
# print(3/4)
# print(3%4)
# print(3**4)
# print(3//4)

# num = 3 
# print(num)

# name = "hello"
# print(name)

# # 5 = 4
# # @@ = 454
# # ^ = 454
# # & = 454
# # ! = 54

# # num  = 10 
# # # print(print)
# # print(num)

# Age = 22 
# # print(Age)


# Age = 35
# print(Age)


# AGE = 10
# print(AGE)

# # 
# a =input("enter you number ")
# print(a)


# a = 10
# b = 20
# print(a+b)
# print(a-b)
# print(a*b)
# print(a/b)
# print(a%b)
# print(a**b)
# print(a//b)


# int 
# float
# str
# bool
# None
# complex
# tuple
# list 
# dict 
# set 


# name = "upflairs pvt ldt "
# print(name)
# print("type of str:-",type(name))  # data type check rkne ke liye 
# print("len  of str:-",len(name)) ## length of string



# name = "upflairs"
# last = "PVT LDT"
# print("len of string :-",len(name))
# print("type of string :- ",type(name))
# print("uppercase:-",name.upper())
# print("lower case :-",last.lower()) 
# print("title:-",name.title()) # 
# print("capitalize string:-",name.capitalize())
# print("swapcase:-",name.swapcase())
# print(last.swapcase())
# print("count of a :-",name.count('a')) 
# #
# print(name[5])
# print(name[0:5])


# print("my company name is",name)
# first = "Ritik"
# last = "Kumar"
# print(f"my first name{first} and my last name is {last}" )
# print(first+" "+last)
# print(name*last)
# print(name/last)

# ctrl + /?



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..list <<<<<<<<<<<<<<<<<<<<<<<<<


# lst  = [1,2,3,5,5,5,6, "Ritik", 2.5]
# print("len of list:-",len(lst))
# print("type of list :- ",type(lst))
# # # indexing 
# print(lst[0])
# print(lst[7])

# # name = "ritik"
# # print(type(name))

# # array or list 
# ### slicing 
# print(lst[0:5])

# lst.append(500)
# print(lst)
# lst.pop()
# print(lst)
# lst.pop(3)
# print(lst)

# lst.insert(2, 1000)
# print(lst)
# lst.remove(2)
# print(lst)
# # lst.clear()
# # print(lst )

# lst.reverse()
# print(lst)

# print(lst.count(2))
# lst.sort()
# print(lst)


# deep copy 
# copy 


# >>>>>>>>>>>>>>>>>>>>>>>>>>>tuple >>>>>>>>>>>>>>>>>>>>>>>

# tpl = (1,23,4,4,5,5,"Rohit", 2.25)
# print("type of tuple:-",type(tpl))
# print("len of tuple",len(tpl))


# # indexing 
# print(tpl[0])
# print(tpl[5])


# # # slicing 
# print(tpl[0:5]) # 0 str point : 5 ending point  
# print(tpl[::-1])

# print(2 in tpl)
# print(1 in tpl)

# tpl1 = (1,2,3,4,5,5,6,6,67,7,87,8)
# print(max(tpl1))
# print(min(tpl1))
# print(sum(tpl1))


# a = 1,2,3,4,5,5,6,6,7,7,7,7
# print(type(a))
# print(a)
# print(len(a))
# a =int(input("enter you number1 "))
# b =int(input("enter you number2 "))

# print(type(a))
# print(type(b))

# print(a*b)

# abc = (1,2,3)
# a ,b, c= abc
# print(a)
# print(b)
# print(c)


# tpl1 = (1,2,3,4,5,6,7)
# tpl2 = (1,2,3,4,5,6,7)
# print(tpl1+tpl2)
# print(tpl2*tpl1)
# print(tpl1*3)


# tast 2 ::----->>  tple = (1,2,3,5,4,8,8,[1,2,7,8])


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Dict<<<<<<<<<<<<<<<<<<<<<<<
# dct = {
#     "name" : "ritik",
#     "age" : 22,
#     "phone" : 1234567890}  ## name , age and phone are keys ritik , 22 , 1234567890 value 

# print(dct)
# print("type of dict :-",type(dct))



# print(dct["name"])
# print(dct['age'])
# print(dct['phone'])

# print(dct.get("name"))

# dct['address']="Jaipur"
# print(dct)

# # tast 3 dict value usko update kese kroge 


# dct['age']=50
# print(dct)

# # variablename.update(indexvalue:value)

# # del dct['phone']
# # print(dct)

# dct.pop("phone")
# print(dct)


# # dict method

# print(dct.keys())
# print(dct.values())
# print(dct.items())


# print("name" in dct)
# print("hello" in dct)


# dct1 = {}
# print(dct1)
# print(type(dct1))





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>operator<<<<<<<<<<<<<<<<<<<<<<
# 1. Arithmetic Operators
# a = 10
# b = 3
#
# print("Arithmetic Operators:")
# print("a + b =", a + b)    # 13
# print("a - b =", a - b)    # 7
# print("a * b =", a * b)    # 30
# print("a / b =", a / b)    # 3.333...
# print("a % b =", a % b)    # 1
# print("a // b =", a // b)  # 3
# print("a ** b =", a ** b)  # 1000
# print()

# # 2. Comparison Operators
# print("Comparison Operators:")
# print("a == b:", a == b)   # False
# print("a != b:", a != b)   # True
# print("a > b:", a > b)     # True
# print("a < b:", a < b)     # False
# print("a >= b:", a >= b)   # True
# print("a <= b:", a <= b)   # False
# print()

# # 3. Logical Operators
# x = True
# y = False

# print("Logical Operators:")
# print("x and y:", x and y)  # False
# print("x or y:", x or y)    # True
# print("not x:", not x)      # False
# print()

# # 4. Assignment Operators
# print("Assignment Operators:")
# c = 5
# print("c =", c)
# c += 2
# print("c += 2 ->", c)
# c *= 3
# print("c *= 3 ->", c)
# c -= 4
# print("c -= 4 ->", c)
# c //= 2
# print("c //= 2 ->", c)
# c **= 2
# print("c **= 2 ->", c)
# print()

# # 5. Bitwise Operators
# print("Bitwise Operators:")
# p = 5       # 0101
# q = 3       # 0011
# print("p & q =", p & q)     # 0001 -> 1
# print("p | q =", p | q)     # 0111 -> 7
# print("p ^ q =", p ^ q)     # 0110 -> 6
# print("~p =", ~p)           # -(p+1) -> -6
# print("p << 1 =", p << 1)   # 1010 -> 10
# print("p >> 1 =", p >> 1)   # 0010 -> 2
# print()

# # 6. Membership Operators
# print("Membership Operators:")
# list1 = [1, 2, 3, 4]
# print("2 in list1:", 2 in list1)        # True
# print("5 not in list1:", 5 not in list1)  # True
# print()

# # 7. Identity Operators
# print("Identity Operators:")
# m = [1, 2, 3]
# n = m
# o = [1, 2, 3]
# print("m is n:", m is n)         # True
# print("m is o:", m is o)         # False
# print("m == o:", m == o)         # True (values are equal)
