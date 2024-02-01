x = 3
def func(x = x):
    print(x)

func()
func(x = 4)

d = {
    "alice":"this is alice",
    "bob":"this is bob"
}

intro = d.get("bob","alice")
print(intro)